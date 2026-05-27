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

## ⚙️ Setup GitHub Actions (una tantum, importante)

Due workflow attivi nella repo:

- **`.github/workflows/generate-index.yml`** — rigenera `index.toon` ad ogni push su `components/**/metadata.json` e lo committa automaticamente.
- **`.github/workflows/weekly-report.yml`** — venerdì mattina alle 9:00 CET aggrega tutti i changelog modificati nella settimana e li manda su Slack come report + post per componente.

### Permessi al GITHUB_TOKEN (entrambi i workflow)

GitHub di default può creare repo con il `GITHUB_TOKEN` in **read-only**, e in quel caso entrambi i workflow falliscono allo step di `git push` con un **403**. Il `permissions: contents: write` nel YAML è necessario ma non sufficiente — serve anche l'opt-in a livello repo.

**Da fare una volta:**

`Settings → Actions → General → Workflow permissions → "Read and write permissions" → Save`

Sintomi se non è settato: vedi il workflow rosso in Actions, e nello step "Commit / Push" appare `remote: Permission to ... denied to github-actions[bot]` o `error: 403`.

### Secrets per il weekly report

`generate-index.yml` non richiede secret. Il `weekly-report.yml` richiede invece due Repository secrets in `Settings → Secrets and variables → Actions → New repository secret`:

| Secret | Valore | Dove prenderlo |
|---|---|---|
| `ANTHROPIC_API_KEY` | API key Anthropic | console.anthropic.com → API Keys |
| `SLACK_WEBHOOK_URL` | Incoming webhook URL | api.slack.com/apps → la tua app → Incoming Webhooks |

Senza questi due, il workflow parte ma fallisce subito a `os.environ["ANTHROPIC_API_KEY"]`.

### Verifica veloce

Dopo aver settato permessi + secret, lancia manualmente:

- `Actions → Generate index → Run workflow` → deve completare verde e (se ci sono cambi non riflessi) committare un `chore: rigenera index.toon`.
- `Actions → Weekly DS Report → Run workflow` → deve completare verde e mandare 1 messaggio Block Kit + N post su Slack (se ci sono changelog modificati dall'ultimo tag `report-*`).

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

### 🟢 I designer mi hanno consegnato un frame Figma con la spec scritta — come la trasformo in JSON?

Capita spesso che i designer documentino un nuovo componente o un nuovo page-pattern direttamente su un frame Figma, con sezioni testuali pre-divise (es. "Quando usarlo", "Anti-pattern", "Slot", "Razionale UX", "Stati"). In questo caso non bisogna riscrivere niente a mano — basta dare il frame in pasto all'agente AI e lasciare che mappi i paragrafi sui campi giusti dello schema.

**Procedura:**

1. **Verifica che il frame abbia il `node-id` nell'URL**. In Figma: tasto destro sul frame → `Copy/Paste as` → `Copy link to selection`. Se l'URL non contiene `?node-id=...`, l'agente non può aprire il singolo frame.
2. **Decidi cosa stai documentando.** Le due opzioni sono mutuamente esclusive:
   - **Un componente** → l'output finirà in `components/<slug>/docs/metadata.json`, lo schema è in [`SCHEMA.md`](SCHEMA.md)
   - **Un page-pattern** → l'output finirà in `page-patterns/<slug>/composition.json` + `pattern.md`, lo schema è in [`page-patterns/SCHEMA-PATTERN.md`](page-patterns/SCHEMA-PATTERN.md)
3. **Dai all'agente AI un prompt completo**, qualcosa tipo:

   > "Apri questo frame Figma e estrai la spec testuale per popolare il `metadata.json` del componente `<slug>` — segui lo schema in `SCHEMA.md`: `<link Figma con node-id>`"
   >
   > oppure:
   >
   > "Apri questo frame Figma e estrai la spec per popolare il `composition.json` + `pattern.md` del page-pattern `<slug>` — segui lo schema in `page-patterns/SCHEMA-PATTERN.md`: `<link Figma con node-id>`"

4. **L'agente fa il giro:**
   - Apre il frame via Figma MCP, legge screenshot + testo dei paragrafi
   - Mappa ogni sezione del frame al campo corrispondente dello schema (es. "Quando usarlo" → `usage.useCases`; "Anti-pattern" → `usage.antiPatterns[]` con `scenario`/`reason`/`alternative`; "Razionale" → `rationale.designDecisions`)
   - Ti mostra il JSON proposto per **review prima di scrivere su disco**
5. **Tu valida e committi.** L'agente deve sempre fermarsi a mostrare il risultato prima di salvare — se vede paragrafi che non sa mappare (campi non previsti dallo schema, contenuti ambigui), te li segnala invece di inventare un campo nuovo.

**Mapping di riferimento** — i designer Cross-App usano due template ricorrenti, `Purpose & Usage` e `Behavior`. L'agente può fidarsi di questa tabella:

| Frame template designer | Sezione | Campo target nel `metadata.json` |
|---|---|---|
| **Purpose & Usage** | Header *"Component name / variant"* | `component.name` + slug della cartella |
| **Purpose & Usage** | **1.1 How and when to use it (Do ✅)** — descrizione 2-3 frasi | `usage.commonPatterns[].when` |
| **Purpose & Usage** | 1.1 — "In which component / template / flow is it used?" | `usage.commonPatterns[].composition` (o `composition.commonPartners[]` se sono solo nomi di altri componenti) |
| **Purpose & Usage** | 1.1 — screenshot Do | riferimento `figmaNodeIds` (link al frame esemplificativo) |
| **Purpose & Usage** | **1.2 Anti-pattern (Don't ❌)** — *Rule* | `usage.antiPatterns[].scenario` |
| **Purpose & Usage** | 1.2 — *Why it's wrong* | `usage.antiPatterns[].reason` |
| **Purpose & Usage** | 1.2 — *Use instead* | `usage.antiPatterns[].alternative` |
| **Purpose & Usage** | 1.2 — screenshot Don't | riferimento `figmaNodeIds` o note |
| **Behavior** | Interactive elements (cosa è tappabile e cosa succede) | `behavior.interactions` |
| **Behavior** | Position (dove appare nel layout) | `composition.parentConstraints[]` |
| **Behavior** | Animation (tipo + durata) | `behavior.interactions` (nota descrittiva) |
| **Behavior** | Size (min/max + touch target) | `behavior.responsive.*` — chiavi `ios/android/ios-liquid-glass` per componenti app, `mobile/desktop` per componenti web (vedi sotto) — o `parentConstraints` (touch target) |
| **Behavior** | Conditional logic | `behavior.interactions` (chiavi tipo `if:formInvalid → button.disabled`) |
| **Behavior** | **Copy & truncation** | `content` (`maxLines` / `characterLimits` / `overflow` / `rules`) |
| **Behavior** | Do / Don't / Note locali (Mobile / Desktop) | confluiscono in `usage.commonPatterns[]` / `usage.antiPatterns[]` / `rationale.designDecisions` |

L'intera sezione **1.1** del Purpose tipicamente diventa **una entry** in `usage.commonPatterns[]`. Se i designer ne aggiungono più (1.1.A, 1.1.B), una entry per ciascuna. Stesso per **1.2** in `usage.antiPatterns[]`.

**Il template Behavior è multi-DS: riconoscere `app` vs `web` prima di mappare.** Lo stesso template Figma viene usato dai designer per documentare componenti di due Design System diversi, e cambia le colonne in base al contesto:

- **Componente del DS Cross-App (mobile-native)** → il template ha **tre colonne `iOS` / `Android` / `iOS Liquid Glass`** allineate alle `platforms` del DS. Mapping 1:1: ogni colonna va sulla chiave omonima di `behavior.responsive` (`responsive.ios`, `responsive.android`, `responsive.ios-liquid-glass`). Se una colonna è vuota, l'agente lascia la chiave vuota e segnala il gap (non inventa).
- **Componente del DS Web** → il template ha **due colonne `Mobile` / `Desktop`** (responsive web). Mapping 1:1 su `responsive.mobile` / `responsive.desktop`.

L'agente identifica il contesto dalle intestazioni di colonna **prima** di mappare. Se vede `iOS / Android / iOS Liquid Glass` → componente app, va in questa repo. Se vede `Mobile / Desktop` → componente web, **non** va in questa repo (il DS Web è una repo separata) e l'agente lo segnala come scope mismatch a livello di repo, non a livello di campo.

**Altri punti d'attenzione:**

- **Tag "FOR DEVELOPER / FOR DESIGNER"** in cima ai frame — è semantica del workflow Figma, non va nel JSON.
- **Screenshot Do/Don't vuoti** (solo etichetta, niente immagine) = template non compilato → l'agente si ferma e segnala, non inventa contenuto per riempire.

**Convenzioni utili da concordare coi designer** (rendono il processo molto più affidabile):

- Sezioni nominate in modo coerente con lo schema, dove possibile: `Use cases` / `When to use` / `When NOT to use` / `Slot` / `Anti-pattern` / `Stati e interazioni` / `Accessibilità` / `Razionale UX`.
- Per gli anti-pattern, una struttura ricorrente *Scenario → Perché è sbagliato → Alternativa* — è ciò che lo schema si aspetta come triplo `scenario` / `reason` / `alternative`.
- Per i page-pattern, indicare per ogni slot se è `required` / `forbidden` / `optional` e quali componenti sono ammessi.
- Se la spec elenca esempi canonici, includere il link Figma di ognuno → l'agente li mappa in `figmaNodeIds` (per i componenti) o `compositionExamples[]` (per i pattern).

**Cosa NON va fatto automaticamente:**

- L'agente **non promuove status da `scaffold`/`draft` a `full`** solo perché ha estratto la spec. La promozione resta una decisione esplicita dell'UX team (vedi sopra le regole di status).
- Se la spec è frammentata o incompleta, lasciare i campi non coperti **vuoti** invece di completarli per inferenza — questo è coerente con la regola R3 di `CLAUDE.md` (non inventare `designDecisions`, qui esteso a tutti i campi non documentati esplicitamente nel frame).
- Se i designer scrivono hex literals (`#5fa747`), l'agente deve **chiedere il nome del token** invece di accettarli — regola R2.

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

### 🟢 Scorer automatico per review schermate — v1 implementata

**v1 implementata** in [`scripts/score_screen.py`](scripts/score_screen.py). Prende in input un JSON neutro che descrive la schermata (pageType, slot occupati, componenti usati) e produce un report pass/fail con exit code (0 conforme, 1 violazioni). Standalone Python 3, zero dipendenze.

#### Come testare una schermata Figma reale (procedura pratica)

Il modo più semplice per testare lo scorer su una schermata Figma è chiedere a un **agente AI** (Claude Code, ChatGPT con Figma MCP, …) di fare il giro completo al posto tuo. Non serve scrivere codice né conoscere il formato JSON dello scorer — l'agente fa tutto se gli dai due cose: il link Figma e il page-pattern di riferimento.

**Cosa ti serve avere pronto:**
1. Il link Figma del **singolo nodo** che vuoi analizzare (es. una pagina dettaglio specifica), copiato con `Copy link to selection` da Figma — l'URL deve contenere `?node-id=...`. Non un link al file intero.
2. L'**accesso Figma MCP** configurato nell'agente AI (se l'agente te lo chiede al primo uso, fai il flow OAuth — è una volta sola).

**Cosa chiedere all'agente:**

> "Analizza questa pagina e fammi uno score: `<link Figma>`"

L'agente:
1. Apre il nodo Figma via MCP, scarica screenshot + metadata
2. Identifica la page-type (te la chiede se non è ovvia)
3. Ricostruisce la composizione in formato neutro (quali componenti DS riconosce, in quali slot)
4. Passa il tutto allo scorer `python3 scripts/score_screen.py`
5. Ti riporta il risultato in linguaggio naturale

**Cosa aspettarti come output:**

L'agente ti dà un riassunto strutturato così:

- ✅ **Pass** — i controlli automatici superati (slot required presenti, slot forbidden assenti, regole quantitative rispettate come `maxPrimaryCTA: 1/1`)
- ⚠️ **Warning** — verifiche che lo scorer non sa fare da solo, segnalate come "verifica manuale": gli antiPattern semantici del pattern e le customRules narrative
- ❌ **Fail** — violazioni concrete (es. "Header presente in una detail page", "2 Card Highlight invece di 0 ammessa")
- **Verdetto finale** — conforme (0 fail) o non conforme (≥1 fail)

#### Esempio concreto già fatto

Una sessione di analisi reale: la schermata `Page=Info` del file CSK-UI-KIT (un dettaglio del gioco Mega Fire Blaze Roulette) → **risultato: 7 pass / 9 warn / 0 fail → CONFORME al pattern `detail-product-game`**.

L'agente ha riconosciuto: Status Bar OS, Hero Detail con chip Promo/Jackpot, TextBox descrittivi, Banner "Gioco certificato", Card Informative del payout effettivo, Card+TextBox per il payout certificato 94.54%, carosello cross-selling "Suggeriti per te", sticky footer con un solo Primary "Gioca". Niente Header (correttamente sostituito da una X overlay). Nessun antiPattern attivo. La fixture neutra prodotta dall'agente è in [`tests/fixtures/screen_figma_mega_fire_blaze.json`](tests/fixtures/screen_figma_mega_fire_blaze.json) come reference della procedura.

#### Uso diretto da terminale (per chi è già pratico)

Se hai già un JSON neutro pronto puoi saltare l'agente AI e chiamare lo scorer a mano:

```bash
# Schermata conforme → exit 0
python3 scripts/score_screen.py --screen tests/fixtures/screen_detail_ok.json

# Schermata con violazioni intenzionali → exit 1
python3 scripts/score_screen.py --screen tests/fixtures/screen_detail_violations.json

# Override del pageType (se vuoi testare la stessa screen contro un pattern diverso)
python3 scripts/score_screen.py --screen mia-screen.json --page-type homepage
```

#### Cosa controlla oggi (v1)

- **Slot required** → fallisce se mancano nella screen.
- **Slot forbidden** → fallisce se presenti (es. `header` in `detail-product-game`).
- **Componenti dello slot** → fallisce se uno slot contiene un componente non ammesso dal `composition.json`.
- **Regole quantitative**: `maxPrimaryCTA`, `maxCardHighlight`, `maxCardEntrypoint` (conta i `componentsUsed[]` con `slug + props.hierarchy`).
- **Slot non noti** → warning.
- **customRules + antiPatterns del composition** → segnalati come warning ("verifica manuale") — non automatizzabili senza semantica più ricca.

Se il pattern è in `status: draft`, lo scorer lo segnala chiaramente come "risultato indicativo" finché l'UX team non promuove a `full`.

#### Input format (JSON neutro)

```json
{
  "pageType": "detail-product-game",
  "slots": {
    "statusBar": ["Status Bar OS"],
    "hero": ["Hero Detail"],
    "characteristics": ["Card Detail"],
    "stickyFooter": ["Button Group"]
  },
  "componentsUsed": [
    {"slug": "button", "props": {"hierarchy": "primary"}},
    {"slug": "hero-detail", "props": {}}
  ]
}
```

Due fixture di test in [`tests/fixtures/`](tests/fixtures/) — una conforme, una con violazioni — vivono come golden reference: se modifichi un `composition.json`, rilancia lo scorer su entrambe e verifica che continuino a dare exit 0 / 1 rispettivamente.

#### Cosa manca (estensioni future)

- **Adapter Figma diretto**: oggi il JSON neutro deve essere costruito a mano (o da un agente AI che legge la screen Figma). Una v2 potrebbe accettare `--figma-node "fileKey:nodeId"` + token e fare la conversione internamente via Figma REST API.
- **Auto-detect pageType**: oggi va dichiarato. Un classifier euristico (basato sui componenti presenti) potrebbe inferirlo.
- **Check semantici degli antiPattern**: oggi vengono solo elencati come warning. Pattern-by-pattern si possono scrivere check ad-hoc (es. "card-highlight-in-detail" = scorer già lo cattura via `maxCardHighlight: 0`, ma altri richiedono logica custom).
- **Promozione dei pattern a `full`** (dipendenza dal task UX): finché i 5 pattern sono `draft` il risultato dello scorer è indicativo.

### 🟡 POC test (10 brief, di cui 5 adversarial)

Quando i pattern sono in `full` e lo scorer è pronto: definire 10 brief che testano la composizione (es. "homepage con 3 card highlight" → adversarial, deve scattare la regola max 1) e usarli come test di regressione del DS doc.


### 🟢 Mapping Code Connect (link Figma → app consumer)

Aggiungere nei `metadata.json` un campo opzionale `codeConnectKey` o `codeRepoPath` che punta al componente reale nell'app consumer. Sblocca uso del `codebase-index` skill dall'app consumer mappando ↔ metadata.

### 🟢 Validation script

`scripts/validate_metadata.py` che scorre tutti i metadata e tutti i `composition.json` e verifica: JSON valido, no hex literals, `figmaNodeIds` non vuoti se `status="full"`, `type` ∈ enum, slug del folder matcha quello del file. Run in pre-commit / CI.

### 🟢 CI/CD

GitHub Action di validation: estendere [`.github/workflows/generate-index.yml`](.github/workflows/generate-index.yml) (oggi solo build) con uno step di validazione che fa fail della PR se uno dei `metadata.json` è invalido (JSON parse, hex literals, type ∉ enum). La rigenerazione di `index.toon` è già auto-committata.

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
