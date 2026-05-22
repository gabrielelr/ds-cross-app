# Handoff — `ds-cross-app`

> Sei nuovo? **Inizia da qui.**
> Se sei un LLM, leggi anche [`CLAUDE.md`](CLAUDE.md) (viene caricato automaticamente all'apertura della repo e contiene tutte le regole vincolanti).

---

## Articoli su cui si basa questo approccio

Questo setup (metadata strutturati per componenti + page-pattern + agente AI-driven + governance encoded) è ispirato a una serie di articoli del *Design Systems Collective*. Letti in ordine, danno il quadro completo del perché la repo è strutturata così:

1. [Building an AI-Ready Design System](https://www.designsystemscollective.com/building-an-ai-ready-design-system-35e709f54edf) — il punto di partenza: cosa significa rendere un DS leggibile da un'AI
2. [Towards an Agentic Design System](https://www.designsystemscollective.com/towards-an-agentic-design-system-c7e0a6469bb1) — la visione: un DS che lavora attivamente con agenti AI, non solo come riferimento passivo
3. [Design System Documentation as Structured Metadata](https://www.designsystemscollective.com/design-system-documentation-as-structured-metadata-315f62c6eab1) — perché la documentazione deve essere **strutturata** (metadata.json) e non solo prosa
4. [Codebase Indexing for Design Systems Agents](https://medium.com/design-systems-collective/codebase-indexing-for-design-systems-agents-c0f6b563a39e) — come l'index del codebase abilita gli agenti (qui esiste lo skill `codebase-index`, da usare nell'app consumer)
5. [Agent Orchestration for Design Systems](https://medium.com/design-systems-collective/agent-orchestration-for-design-systems-da0f6a5f24fb) — come si compongono più agenti specializzati (compose / review / Q&A) sopra alla stessa knowledge base
6. [Encoding Governance on Agentic Design Systems](https://medium.com/@crmorales.achiardi/encoding-governance-on-agentic-design-systems-1a8c70420fec) — come tradurre le regole UX (oggi sparse nelle teste/mockup) in regole **machine-binding** (`composition.json`, `CLAUDE.md` R1–R10, page-pattern anti-pattern)

In pratica questa repo è un'implementazione concreta di quei principi sul DS Cross-App.

---

## In due righe

Questa repo è la **knowledge base scritta** del Design System Cross App. Non c'è codice: ci sono `.json` e `.md` che descrivono **i componenti** del DS e **i pattern di pagina** dell'app. L'obiettivo è far sì che un LLM (Claude, ChatGPT, …) possa **comporre, recensire e spiegare** schermate dell'app rispettando le regole del DS, senza inventare.

## Cosa puoi fare qui

1. **Documentare un componente nuovo** (es. è uscita una nuova `Card Tutorial` in Figma → la documenti qui)
2. **Comporre una schermata nuova** seguendo i pattern (es. devi proporre una pagina settings → leggi il pattern, applichi le regole, generi su Figma)
3. **Recensire una schermata esistente** (es. arriva un mockup da review → verifichi cosa è conforme e cosa no rispetto al DS)

---

## Mappa della repo

```
ds-cross-app/
├── CLAUDE.md            ← tutte le regole + processo (auto-caricato dall'LLM)
├── HANDOFF.md           ← questo file (per umani che arrivano nuovi)
├── README.md            ← one-liner
├── SCHEMA.md            ← schema del metadata.json di ogni componente
│
├── components/          ← 60 componenti del DS (Button, Card, Header, …)
│   └── <slug>/docs/
│       ├── metadata.json    ← cosa è il componente, varianti, slot, anti-pattern
│       └── changelog.md     ← storico delle modifiche
│
├── page-patterns/       ← macro-pattern per tipologia di pagina (home, detail, form, …)
│   ├── SCHEMA-PATTERN.md
│   ├── README.md
│   └── <slug>/
│       ├── pattern.md       ← descrizione UX in linguaggio naturale (CRITICO)
│       ├── composition.json ← slot strutturati machine-readable
│       └── changelog.md
│
└── skills/              ← skill Claude Code (codebase-index, ai-component-metadata)
```

---

## I due pilastri della repo

Quando lavori con questa repo, ti muovi sempre fra **due tipi di documenti**:

### 1. Componenti (`components/<slug>/`)
Ogni componente del DS ha un `metadata.json` che descrive **cosa fa quel pezzo**: le sue varianti, i suoi slot, i token che usa, gli stati, gli anti-pattern interni, l'accessibility. Risponde a: *"come si usa il Button?"*, *"quante varianti ha il Card Detail?"*,.

### 2. Page-pattern (`page-patterns/<slug>/`)
Ogni tipologia di pagina dell'app ha un pattern che descrive **come si assemblano i componenti per formare una pagina coerente**: gli slot obbligatori, quelli vietati, le regole quantitative, gli anti-pattern di composizione. Risponde a: *"come deve essere fatta una pagina dettaglio gioco?"*, *"il menu unico cosa contiene?"*, *"un form come si struttura?"*.

**Page-pattern viene PRIMA dei componenti.** Quando devi comporre una schermata, parti sempre dal page-pattern, e solo dopo scegli i componenti specifici.

---

## ⚠️ Perché i page-pattern devono essere **descritti** narrativamente

Un page-pattern ha due file: `composition.json` (struttura) e `pattern.md` (descrizione).

**Entrambi sono obbligatori.** Lo `composition.json` da solo non basta — un LLM che legge solo i vincoli quantitativi tende ad **allucinare** il contesto: riempie i buchi con assunzioni plausibili ma sbagliate.

Il `pattern.md` racconta:
- **Quando usare** il pattern (use case concreti)
- **Quando NON usarlo** (page-type alternative)
- **Perché ogni slot esiste** (razionale UX, non solo "esiste")
- **Perché le regole sono come sono** (motivazione, vincoli storici, lezioni imparate)
- **Esempi reali** con Figma node ID

Senza questo contesto narrative, l'LLM ti darà schermate "tecnicamente conformi" ma semanticamente sbagliate. Per esempio: rispetta tutti i vincoli quantitativi ma usa un componente nel contesto sbagliato perché "non sapeva" cosa rappresenta nella vertical.

**Quando crei o aggiorni un page-pattern, scrivi prima `pattern.md`, poi `composition.json`. Mai il contrario.**

---

## Task comuni con esempi

### 🟢 Voglio documentare un componente nuovo

1. Apri Figma sul componente, copia URL con node-id
2. Fetcha i dati via Figma MCP (`get_metadata`, `get_design_context`, `get_variable_defs`, `get_screenshot`)
3. Crea `components/<slug>/docs/metadata.json` seguendo lo schema in [`SCHEMA.md`](SCHEMA.md). Lo schema è definito dalla skill **`ai-component-metadata`** in `skills/` — usa il suo template (`skills/ai-component-metadata/assets/metadata-template.tsx`) come punto di partenza. Se il componente esiste anche in codice (`.tsx`), la skill può generare automaticamente un primo draft.
4. Regole: token names (mai hex), solo quello che è in Figma (no invenzioni), `rationale.designDecisions=""` finché non hai motivazioni reali
5. Aggiorna `changelog.md`
6. Valida JSON + grep no hex

Vedi `CLAUDE.md` → "Processo: documentare un nuovo componente" per la versione formale.

### 🟢 Voglio comporre una schermata nuova

1. **Identifica la page-type** (dettaglio gioco? form di valutazione? menu? listing?)
2. Apri `page-patterns/<slug>/pattern.md` e leggi narrative + use cases + anti-pattern
3. Apri `page-patterns/<slug>/composition.json` per la slot map strutturata
4. **Se il pattern non esiste**: fermati, crea il pattern prima (vedi sotto), POI componi
5. Per ogni slot, scegli il componente concreto guardando in `components/`
6. Verifica regole (max 1 Primary, max 1 Card Highlight, ecc.) e anti-pattern
7. Genera su Figma via `use_figma` MCP
8. Pre-flight finale (checklist in `CLAUDE.md`)

**Esempio concreto** (già fatto): pagina dettaglio gioco "Premium Roulette European" → ho letto `page-patterns/detail-product-game/`, ho composto seguendo gli slot canonici (Status Bar + Hero + Card Detail + TextBox + Banner + Card Informative + Card+TextBox nested + Button Group sticky), risultato su [Figma 8774:914](https://www.figma.com/design/QWM2EhgZmv2KKcqI0315fx/?node-id=8774-914).

### 🟢 Voglio controllare una schermata esistente

1. Apri la schermata su Figma → fetcha struttura + screenshot
2. Identifica la page-type
3. Apri `page-patterns/<slug>/composition.json`
4. Verifica slot per slot: presente se `required`, assente se `forbidden`, componente corretto
5. Verifica regole quantitative del pattern
6. Verifica regole core (R1–R10 in `CLAUDE.md`)
7. Produci report: ✅ conforme / ❌ violazioni / ⚠️ da verificare / 📚 discrepanze doc

### 🟢 Voglio creare un page-pattern nuovo (è ciò che chiediamo all'UX team)

1. `cp -r page-patterns/detail-product-game page-patterns/<new-slug>` come template
2. Aggiorna `slug`, `name`, `status: "scaffold"` in `composition.json`
3. **Scrivi prima `pattern.md`** — è la parte più importante. Racconta:
   - Cosa è questa page-type, quando si usa, quando NO
   - Perché esistono questi slot e cosa rappresentano
   - Quali sono gli anti-pattern reali (non quelli teorici)
   - Esempi Figma canonici se disponibili
4. **Poi compila `composition.json`** sulla base della narrative
5. Status `scaffold → draft` quando hai una versione iterabile
6. Status `draft → full` quando l'UX team valida
7. Aggiorna l'indice in `page-patterns/README.md`

---

## Skill installate (`skills/`)

| Skill | A cosa serve | Usabile su questa repo? |
|---|---|---|
| `ai-component-metadata` | **Definisce lo schema** del `metadata.json` dei componenti DS e genera il file partendo da un componente `.tsx` (oppure da un template da compilare a mano). | ✅ Sì — è la fonte dello schema dei nostri 60 metadata.json. Quando aggiungi un componente nuovo, parti dal template di questa skill. |
| `codebase-index` | Mappa dipendenze fra componenti di un codebase (React/Vue/Astro/…) e produce un file di relazioni `.toon`/`.json`. | ❌ No qui — questa repo non ha codice runtime. La skill è destinata all'**app consumer** del DS (repo del codebase mobile Sisal/Snai/Pokerstars). Lasciata installata per portabilità. |

Vedi `SCHEMA.md` — la nostra estensione dello schema base di `ai-component-metadata` (aggiunge `figmaNodeIds`, `lastUpdated`, `platforms`, `status`, ecc.).

---

## Lavoro ancora da fare

I task aperti sono pensati per arrivare ai 3 obiettivi (comporre / Q&A / recensire). Sono ordinati per impatto.

### 🔴 Validare i page-pattern esistenti + aggiungere quelli mancanti (UX team)

Questo è **il blocker numero uno** per tutti e 3 gli obiettivi.

Stato oggi: 5 page-pattern creati come `draft` migrando i template che vivevano in vecchi file di regole. Sono `detail-product-game` (completo, reference) + `form-data-collection` + `menu-unico` + `homepage` + `bottom-sheet-modal`. L'UX team deve:

1. **Validare i 5 esistenti** scorrendo `pattern.md` e `composition.json`: slot mancanti? regole sbagliate? anti-pattern reali? — promuovere `status: draft → full`
2. **Aggiungere i pattern mancanti** elencati in [`page-patterns/README.md`](page-patterns/README.md): settings, listing-products, login, signup, deposit, withdrawal, error-page, empty-state, ecc.
3. **Compilare `rationale`** dove possibile (oggi vuoto, in attesa di razionali UX consolidati)
4. **Aggiungere `compositionExamples`** Figma reali (oggi alcuni vuoti) — servono come few-shot per AI e come test corpus per lo scorer di review

### 🟡 Index aggregato di tutti i metadata

Oggi un LLM che apre la repo deve leggere 60 metadata.json individualmente (~200k+ token) per avere il quadro. Serve uno script che li aggrega in un singolo `INDEX.toon` (~5–10k token): lista componenti, anti-pattern aggregati, dependency graph, useCases.

### 🟡 Scorer automatico per review schermate

Uno script Python che, dato un `fileKey + nodeId` Figma, legge la struttura via API, identifica la page-type, carica il `composition.json` del pattern corrispondente, ed emette pass/fail per ogni regola. **Dipende dal task precedente**: serve che i pattern siano in `status: full` per avere un oracle affidabile.

### 🟡 POC test (10 brief, di cui 5 adversarial)

Quando i pattern sono in `full` e lo scorer è pronto: definire 10 brief che testano la composizione (es. "homepage con 3 card highlight" → adversarial, deve scattare la regola max 1) e usarli come test di regressione del DS doc.


### 🟢 Mapping Code Connect (link Figma → app consumer)

Aggiungere nei `metadata.json` un campo opzionale `codeConnectKey` o `codeRepoPath` che punta al componente reale nell'app consumer. Sblocca uso del `codebase-index` skill dall'app consumer mappando ↔ metadata.

### 🟢 Validation script

`scripts/validate_metadata.py` che scorre tutti i metadata e tutti i `composition.json` e verifica: JSON valido, no hex literals, `figmaNodeIds` non vuoti se `status="full"`, `type` ∈ enum, slug del folder matcha quello del file. Run in pre-commit / CI.

### 🟢 CI/CD

GitHub Action: validation + rigenerazione INDEX.toon ad ogni push. Fail PR se invalid.

---

## Memorie attive (cross-conversation)

Le regole personali che Claude ricorda fra una sessione e l'altra (oggi salvate in `~/.claude/projects/.../memory/`) sono **consolidate** in [`CLAUDE.md`](CLAUDE.md). Le memorie esterne restano valide come backup, ma `CLAUDE.md` è la fonte canonica per qualsiasi LLM (anche non-Claude) che apre questa repo.

Le memorie cross-conversation continuano a essere salvate via memory system standard quando emergono regole nuove — vanno **anche** trasferite in `CLAUDE.md` se rilevanti per il progetto.

---

## TL;DR per chi parte adesso

1. Leggi questo file (5 min)
2. Leggi [`CLAUDE.md`](CLAUDE.md) (10 min) — le regole vincolanti
3. Per documentare un componente → vedi sezione "Task comuni"
4. Per comporre una schermata → leggi prima il `page-patterns/<slug>/`, poi i componenti
5. Per recensire una schermata → identifica page-type, apri `composition.json` del pattern, verifica
6. Niente codice in questa repo — il codice vive nell'app consumer
7. La priorità #1 oggi è **validare i page-pattern esistenti e aggiungere i mancanti** (UX team)
