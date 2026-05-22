# `page-patterns/` — Macro-pattern per tipologia di schermata

Ogni cartella qui dentro è un **page-pattern**: un macro-pattern che definisce **come si compone una determinata tipologia di schermata** del DS Cross-App. I page-pattern sono **owned dall'UX team** e descrivono regole, slot obbligatori/vietati, e composizioni canoniche per quella tipologia.

A differenza dei componenti (in `components/`) che documentano i singoli pezzi, i page-pattern documentano **come si assemblano** in una schermata coerente.

---

## ⚠️ Critico: i page-pattern DEVONO essere descritti narrativamente

Ogni pattern ha due file di contenuto: `composition.json` (struttura) e `pattern.md` (descrizione).

**Entrambi sono obbligatori. Non saltare `pattern.md`.**

Lo `composition.json` da solo elenca i vincoli quantitativi, ma **un LLM che legge solo i vincoli senza contesto allucina**: riempie i buchi con assunzioni plausibili ma sbagliate. Per esempio: rispetta `maxPrimaryCTA: 1` ma usa il componente nel contesto sbagliato perché "non sapeva" cosa rappresenta nella vertical.

Il `pattern.md` deve raccontare:

- **Quando usare** il pattern (use case concreti)
- **Quando NON usarlo** (page-type alternative)
- **Perché ogni slot esiste** (razionale UX, non solo "esiste")
- **Perché certe regole sono come sono** (motivazione, vincoli storici, lezioni imparate)
- **Esempi reali** con Figma node ID

> **Workflow obbligato per chi crea/aggiorna un pattern**:
> 1. **Prima** scrivi `pattern.md` (la narrative)
> 2. **Poi** compila `composition.json` (la struttura derivata dalla narrative)
>
> Mai il contrario. Mai solo lo schema.

---

## Perché esistono

Senza page-pattern strutturati:
- Gli agenti AI inventano composizioni "ragionevoli" che però violano regole non scritte (es. due Primary in dettaglio, Header in pagina immersiva, ecc.)
- Le regole di pagina vivono solo nella testa dei designer e in mockup sparsi → non scalano
- Lo scorer automatico (review di schermate) non ha un oracle machine-readable contro cui verificare aderenza

Con page-pattern strutturati:
- L'UX team possiede regole esplicite versionabili
- Gli agenti AI leggono `composition.json` come oracle
- Lo scorer automatico verifica conformità senza hardcode

---

## Struttura di un pattern

```
page-patterns/<slug>/
├── pattern.md          # narrative UX: when-to-use, when-NOT-to-use, ratio
├── composition.json    # definizione strutturata (machine-readable)
├── changelog.md        # storico modifiche
└── examples/           # screenshot/notes degli esempi (opzionale)
```

Schema del `composition.json` documentato in [`SCHEMA-PATTERN.md`](SCHEMA-PATTERN.md).

---

## Lista pattern attuali

| Slug | Status | Ownership | Description |
|---|---|---|---|
| [detail-product-game](detail-product-game/) | draft | UX team | Pagina dettaglio prodotto/gioco/iniziativa (Hero immersivo, Card Detail/Informative, Button Group sticky) |
| [form-data-collection](form-data-collection/) | draft | UX team | Pagina form di raccolta dati (Header lvl 2/3/4+, sezioni Radio/Checkbox/TextField, Button Group submit) |
| [menu-unico](menu-unico/) | draft | UX team | Menu Unico (Header Menu/Webview, UserHeader, QuickActions, sezioni listing, Help card, Footer) |
| [homepage](homepage/) | draft | UX team | Homepage (Header lvl Homepage, Hero/Quicklink, Card Product grid, Card Highlight max 1, Bottom Navbar) |
| [bottom-sheet-modal](bottom-sheet-modal/) | draft | UX team | Modale Bottom Sheet (Drawer + Drag Handle + Header sticky + Body + Button Group sticky) |

I 5 pattern sopra sono **seed** migrati dai vecchi template di composizione. Status iniziale: `draft`. **L'UX team li valida e promuove a `full`** (o li corregge).

---

## Pattern da aggiungere (TODO)

Lista (non esaustiva) di page-type che servono al DS Cross-App ma **non sono ancora documentati**:

| Slug | Description | Priority |
|---|---|---|
| `settings` | Pagina settings/preferenze utente | ⭐⭐⭐ |
| `listing-products` | Listing 2-col Card Product con filtri (chip nav o FAB filter) | ⭐⭐⭐ |
| `listing-bonus` | Listing dei bonus utente | ⭐⭐ |
| `login` | Schermata login | ⭐⭐⭐ |
| `signup` | Schermata signup | ⭐⭐⭐ |
| `deposit` | Schermata ricarica saldo | ⭐⭐ |
| `withdrawal` | Schermata prelievo | ⭐⭐ |
| `transaction-history` | Storico movimenti conto | ⭐ |
| `splash-screen` | Splash di apertura app (già documentato come componente, manca il pattern come page) | ⭐ |
| `error-page` | Pagina di errore (404, network, generic) | ⭐⭐ |
| `empty-state` | Stato vuoto (no risultati, no contenuti) | ⭐⭐ |
| `webview-wrapper` | Webview con Header Menu/Webview | ⭐ |
| `dropdown-modal` | Modale dropdown (più semplice di Bottom Sheet) | ⭐ |

Per ogni pattern da aggiungere:
1. Crea `page-patterns/<slug>/` con `pattern.md` + `composition.json` + `changelog.md`
2. Status iniziale: `scaffold` (skeleton)
3. UX team compila → status `draft`
4. Approval → status `full`

---

## Come contribuire (UX team)

### Compilare un pattern esistente in `draft`

1. Apri `pattern.md` → scrivi razionale, when-to-use, when-NOT-to-use, anti-pattern reali (non quelli derivati per osservazione)
2. Apri `composition.json` → verifica slot, aggiungi `constraints`, completa `rules`, aggiungi `compositionExamples` reali con `figmaNodeId`
3. Compila `rationale` se hai un razionale UX consolidato
4. Aggiungi entry al `changelog.md` con la modifica
5. Promuovi `status` da `draft` a `full`

### Creare un pattern nuovo

1. `cp -r detail-product-game <new-slug>` come template di partenza
2. Aggiorna `slug`, `name`, `status: "scaffold"`, svuota i campi che non si applicano
3. Aggiungi alla tabella in questo README (sezione "Lista pattern attuali")
4. Procedi come sopra

---

## Come usano i pattern gli agenti AI

Quando un agente AI deve comporre una schermata:

1. Identifica la **page-type** richiesta (detail / form / menu / homepage / …)
2. Apre `page-patterns/<slug>/composition.json` e lo carica come context
3. Genera la composizione rispettando:
   - Ogni slot `required: true` → presente
   - Ogni slot `forbidden: true` → assente
   - Ogni vincolo in `rules` rispettato
   - I componenti dello slot sono quelli in `components[]`
4. Verifica contro `antiPatterns` del pattern + pre-flight checklist di `CLAUDE.md`

---

## Come usa i pattern lo scorer di review

Lo scorer (task aperto in `HANDOFF.md` — "Scorer automatico per review schermate") carica `composition.json` del pattern corrispondente alla page-type rilevata in una schermata Figma, e verifica per ogni regola pass/fail:

```python
# pseudo-code
pattern = json.load(f"page-patterns/{detected_page_type}/composition.json")
for slot_name, slot_def in pattern["slots"].items():
    if slot_def.get("required") and not screen_has_slot(slot_name):
        report.fail(f"Missing required slot: {slot_name}")
    if slot_def.get("forbidden") and screen_has_slot(slot_name):
        report.fail(f"Forbidden slot present: {slot_name} ({slot_def['reason']})")
for rule, expected in pattern["rules"].items():
    actual = screen_count_for_rule(rule)
    if not check_rule(rule, actual, expected):
        report.fail(f"Rule violation: {rule}, expected {expected}, got {actual}")
```

Zero hardcode dello scorer — tutta la logica è nei `composition.json`.

---

## Versionamento

Ogni `composition.json` cambia → entry obbligatoria in `changelog.md` con data + modifica + status flow. Stesso pattern dei componenti.

Es. `2026-05-22 — Aggiunto slot fab opzionale per FAB Filter (proposta B listing).`
