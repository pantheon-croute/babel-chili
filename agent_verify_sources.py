#!/usr/bin/env python3
"""
agent_verify_sources.py
pip install requests dukpy
python agent_verify_sources.py --input data.js --limit 3
"""

import json, time, argparse, sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("pip install requests"); sys.exit(1)

WIKTIONARY_LANGS = {
    'FR':'fr','EN':'en','DE':'de','ES':'es','PT':'pt','IT':'it','NL':'nl',
    'JP':'ja','ZH':'zh','TH':'th','HI':'hi','SW':'sw','AR':'ar','TR':'tr',
    'VI':'vi','FA':'fa','HU':'hu','KO':'ko','NAH':'nah','CR':'ht'
}
DELAY = 0.5

def parse_data_js(filepath):
    try:
        import dukpy
    except ImportError:
        print("pip install dukpy"); sys.exit(1)
    content = Path(filepath).read_text(encoding='utf-8')
    result = dukpy.evaljs(content + "\nJSON.stringify(peppers);")
    return json.loads(result)

def query_wiktionary(word, lang_code):
    wl = WIKTIONARY_LANGS.get(lang_code, lang_code.lower())
    url = f"https://{wl}.wiktionary.org/api/rest_v1/page/summary/{requests.utils.quote(word)}"
    try:
        r = requests.get(url, timeout=8, headers={'User-Agent':'BabelIngredients/1.0'})
        if r.status_code == 200:
            d = r.json()
            return {'found':True,'extract':d.get('extract','')[:200],
                    'source_url':d.get('content_urls',{}).get('desktop',{}).get('page',''),
                    'source_name':f"Wiktionary {wl.upper()}"}
    except: pass
    return {'found':False}

def query_wikipedia(query, lang='en'):
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query)}"
    try:
        r = requests.get(url, timeout=8, headers={'User-Agent':'BabelIngredients/1.0'})
        if r.status_code == 200:
            d = r.json()
            return {'found':True,'extract':d.get('extract','')[:200],
                    'source_url':d.get('content_urls',{}).get('desktop',{}).get('page','')}
    except: pass
    return {'found':False}

def query_usda_grin(species):
    url = f"https://npgsweb.ars-grin.gov/gringlobal/rest/taxon?name={requests.utils.quote(species)}&limit=1"
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent':'BabelIngredients/1.0'})
        if r.status_code == 200:
            d = r.json()
            if d:
                t = d[0]
                return {'found':True,'accepted_name':t.get('name'),
                        'source_url':f"https://npgsweb.ars-grin.gov/gringlobal/taxon/taxonomydetail?id={t.get('id')}"}
    except: pass
    return {'found':False}

def verify_pepper(pepper):
    pid = pepper.get('id','?')
    print(f"\n🌶  {pid}")
    sources = {}

    species = pepper.get('species','')
    if species:
        print(f"  → USDA GRIN : {species}")
        u = query_usda_grin(species)
        sources['_species'] = {'verified':u['found'],'source_url':u.get('source_url',''),'source_name':'USDA GRIN','note':u.get('accepted_name','')}
        time.sleep(DELAY)

    en_name = pepper.get('translations',{}).get('EN',{}).get('name', pid)
    print(f"  → Wikipedia EN : {en_name}")
    w = query_wikipedia(en_name)
    sources['_wikipedia_en'] = {'verified':w['found'],'source_url':w.get('source_url',''),'extract':w.get('extract','')[:150]}
    time.sleep(DELAY)

    for lang_code in WIKTIONARY_LANGS:
        trans = pepper.get('translations',{}).get(lang_code,{})
        word = (trans.get('name') or '').strip()
        if not word: continue
        print(f"  → Wiktionary {lang_code} : {word}")
        res = query_wiktionary(word, lang_code)
        sources[lang_code] = {'verified':res['found'],'source_url':res.get('source_url',''),'source_name':res.get('source_name','')}
        time.sleep(DELAY)

    return sources

def generate_report(peppers_verified, output_path):
    lines = [f"# Babel Pimiento — Vérification\n\n{len(peppers_verified)} entrées\n\n---\n\n"]
    for p in peppers_verified:
        sources = p.get('sources',{})
        score = p.get('verification_score',0)
        lines.append(f"## {p.get('id')} — *{p.get('species')}* — {score}%\n\n")
        lines.append("| Langue | Nom | OK | Source |\n|--------|-----|----|--------|\n")
        for lc, trans in p.get('translations',{}).items():
            src = sources.get(lc,{})
            ok = "✅" if src.get('verified') else "❌"
            url = src.get('source_url','')
            link = f"[lien]({url})" if url else "—"
            lines.append(f"| {lc} | {trans.get('name','')} | {ok} | {link} |\n")
        lines.append("\n")
    Path(output_path).write_text("".join(lines), encoding='utf-8')
    print(f"\n📄 Rapport : {output_path}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input',  default='data.js')
    p.add_argument('--output', default='data_verified.json')
    p.add_argument('--report', default='verification_report.md')
    p.add_argument('--limit',  type=int, default=None)
    args = p.parse_args()

    print(f"📖 Lecture de {args.input}...")
    peppers = parse_data_js(args.input)
    print(f"✅ {len(peppers)} piments")
    if args.limit: peppers = peppers[:args.limit]

    results = []
    for i, pepper in enumerate(peppers):
        print(f"\n[{i+1}/{len(peppers)}]", end='')
        sources = verify_pepper(pepper)
        total = len(sources)
        verified = sum(1 for s in sources.values() if s.get('verified'))
        score = round(verified/total*100) if total else 0
        results.append({**pepper, 'sources':sources, 'verification_score':score})

    Path(args.output).write_text(
        json.dumps({'peppers':results,'total':len(results)}, ensure_ascii=False, indent=2),
        encoding='utf-8')
    print(f"\n✅ {args.output}")
    generate_report(results, args.report)

    scores = [p['verification_score'] for p in results]
    avg = sum(scores)/len(scores) if scores else 0
    print(f"\nScore moyen : {avg:.0f}% | ≥70% : {sum(1 for s in scores if s>=70)}/{len(results)} | <30% : {sum(1 for s in scores if s<30)}/{len(results)}")

if __name__ == '__main__':
    main()
