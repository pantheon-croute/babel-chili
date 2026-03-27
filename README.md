# 🌶️ Babel des Piments

> *Pourquoi "pepper" désigne-t-il à la fois le poivre noir et le piment rouge ? Pourquoi "paprika" est un légume dans certaines langues et une épice dans d'autres ? Pourquoi "chili", "chilli" et "chile" coexistent en anglais ?*

**Babel des Piments** est une encyclopédie interactive qui documente la confusion linguistique et botanique autour des piments à travers 24 langues et 22 variétés.

---

*[Français](#français) — [English](#english)*

---

## Français

### Présentation

Lorsque Christophe Colomb est rentré d'Amérique avec des *Capsicum*, il les a appelés "pepper" — le mot qu'il connaissait pour désigner une épice forte. Ce malentendu fondateur a contaminé toutes les langues européennes, et les 500 ans qui ont suivi n'ont fait qu'empirer les choses.

Ce projet cartographie les faux amis, les calques, les glissements sémantiques et les ambiguïtés botaniques qui font que demander "un piment" dans un restaurant peut donner des résultats très différents selon le pays.

### Fonctionnalités

- **22 variétés** de piments cataloguées, du poivron (0 SHU) au Carolina Reaper (2 200 000 SHU)
- **24 langues** : français, anglais, espagnol, allemand, japonais, chinois, arabe, thaï, hindi, swahili, nahuatl, créole et plus
- **Vue orbitale interactive** : cliquer sur un piment affiche ses noms dans toutes les langues sous forme de constellation
- **Niveau de confusion** par variété : CHAOS / HIGH / MED / LOW
- **Étymologies** et **faux amis** détaillés pour chaque entrée
- **Filtre par langue** : afficher uniquement les traductions qui vous intéressent
- **Données vérifiées** via Wiktionary, Wikipedia et la base USDA GRIN

### Stack technique

| Couche | Technologie |
|--------|-------------|
| Frontend | HTML5 · CSS3 · JavaScript vanilla |
| Données | `data.js` (source principale) · `data_verified.json` |
| Vérification | Python 3 (`requests`, `dukpy`) |
| Polices | Google Fonts — Fredoka One, Nunito |
| Déploiement | Fichiers statiques, aucun serveur requis |

### Structure du projet

```
babel-piments/
├── index.html              # Application principale (interface + logique)
├── data.js                 # Base de données des piments (22 entrées × 24 langues)
├── data_verified.json      # Données enrichies avec scores de vérification
├── extract_data.js         # Utilitaire Node.js d'extraction
├── agent_verify_sources.py # Script Python de vérification des sources
└── verification_report.md  # Rapport de vérification (sources, scores)
```

### Format d'une entrée

```js
{
  id: 'jalapeño',
  species: 'Capsicum annuum',
  shu_min: 2500,
  shu_max: 8000,
  confusion: 'MED',           // CHAOS | HIGH | MED | LOW
  translations: {
    fr: {
      name: 'Jalapeño',
      etymology: 'De Xalapa, ville du Mexique',
      false_friend: 'Devient "chipotle" une fois fumé et séché — même fruit, autre nom'
    },
    en: { ... },
    // 22 autres langues
  }
}
```

### Lancer en local

Aucune dépendance à installer. Ouvrir `index.html` dans un navigateur suffit.

```bash
# Ou via un serveur local pour éviter les restrictions CORS sur data.js :
npx serve .
# → http://localhost:3000
```

### Cas notables documentés

| Variété | Confusion | Exemple |
|---------|-----------|---------|
| Poivron | CHAOS | « Paprika » = légume (DE, HU) ou épice (EN, FR) |
| Piment générique | CHAOS | *Chili / Chilli / Chile* — trois orthographes anglaises |
| Sichuan pepper | CHAOS | N'est pas un *Capsicum* — c'est un *Zanthoxylum* (famille des Rutacées) |
| Poivron/Pepper | CHAOS | L'erreur de Colomb : *Piper nigrum* ≠ *Capsicum* |
| Banana pepper | HIGH | « Pepperoni » en Italie = poivron, pas la charcuterie |

---

## English

### Overview

When Columbus returned from the Americas with *Capsicum* plants, he called them "pepper" — the word he knew for a pungent spice. This founding mistake spread into every European language, and the 500 years that followed only made things worse.

This project maps the false friends, calques, semantic shifts, and botanical ambiguities that make ordering "a pepper" at a restaurant a wildly different experience depending on where you are.

### Features

- **22 pepper varieties** catalogued, from bell pepper (0 SHU) to Carolina Reaper (2,200,000 SHU)
- **24 languages**: French, English, Spanish, German, Japanese, Chinese, Arabic, Thai, Hindi, Swahili, Nahuatl, Creole, and more
- **Interactive orbital view**: click any pepper to display its names across all languages as a constellation
- **Confusion rating** per variety: CHAOS / HIGH / MED / LOW
- **Etymologies** and **false friends** detailed for each entry
- **Language filter**: show only the translations you care about
- **Verified data** via Wiktionary, Wikipedia, and the USDA GRIN database

### Tech stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5 · CSS3 · Vanilla JavaScript |
| Data | `data.js` (primary source) · `data_verified.json` |
| Verification | Python 3 (`requests`, `dukpy`) |
| Fonts | Google Fonts — Fredoka One, Nunito |
| Deployment | Static files, no server required |

### Project structure

```
babel-piments/
├── index.html              # Main application (UI + logic)
├── data.js                 # Pepper database (22 entries × 24 languages)
├── data_verified.json      # Enriched data with verification scores
├── extract_data.js         # Node.js extraction utility
├── agent_verify_sources.py # Python source-verification script
└── verification_report.md  # Verification report (sources, scores)
```

### Data entry format

```js
{
  id: 'jalapeño',
  species: 'Capsicum annuum',
  shu_min: 2500,
  shu_max: 8000,
  confusion: 'MED',           // CHAOS | HIGH | MED | LOW
  translations: {
    fr: {
      name: 'Jalapeño',
      etymology: 'From Xalapa, a city in Mexico',
      false_friend: 'Becomes "chipotle" once smoked and dried — same fruit, different name'
    },
    en: { ... },
    // 22 more languages
  }
}
```

### Running locally

No dependencies to install. Opening `index.html` in a browser is enough.

```bash
# Or via a local server to avoid CORS restrictions on data.js:
npx serve .
# → http://localhost:3000
```

### Notable documented cases

| Variety | Confusion | Example |
|---------|-----------|---------|
| Bell pepper | CHAOS | "Paprika" = vegetable (DE, HU) or spice (EN, FR) |
| Generic chili | CHAOS | *Chili / Chilli / Chile* — three English spellings, one plant |
| Sichuan pepper | CHAOS | Not a *Capsicum* at all — it's a *Zanthoxylum* (Rutaceae family) |
| Pepper (word) | CHAOS | Columbus's error: *Piper nigrum* ≠ *Capsicum* |
| Banana pepper | HIGH | "Pepperoni" in Italy = bell pepper, not the cured meat |

---

## License

Ce projet est distribué sous licence **MIT**.
This project is distributed under the **MIT** license.
