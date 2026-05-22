# Page Pattern — Pagina Form / Raccolta Dati

> Owner: UX team · Status: `draft` · Last updated: 2026-05-22

Pagina dedicata alla raccolta di dati strutturati dall'utente: form di valutazione, signup multi-step, modifica profilo, configurazione preferenze, ticket di supporto.

## When to use

- L'utente deve **inserire dati** in più campi prima di proseguire
- Le domande/campi sono **multipli e di tipo misto** (single-select, multi-select, testo libero)
- Serve un **submit unico** che valida tutti i campi insieme

## When NOT to use

- ❌ **Singolo campo** (es. sola ricerca) → usa SearchBar inline o un dropdown modale
- ❌ **Configurazione binaria** (toggle on/off) → settings page con Toggle, non form dedicato
- ❌ **Modale veloce** (conferma azione, dropdown choice) → usa `bottom-sheet-modal`

## Anatomia (top-down)

1. **Status Bar OS**
2. **Header** lvl 2/3/4+ con back + title nome form (o lvl Menu/Webview con close X se modale)
3. **Hero text** opzionale (TextBox Block, h1 + paragraph) — spiega cosa fa il form
4. **N sezioni domanda**: TextBox h3 (titolo domanda) + input (Radio | Checkbox | TextField) in lista verticale
5. **Button Group sticky** con UN Primary = submit + opzionale Secondary = "Annulla"

## Regole

- ✅ **Radio** per single-select, **Checkbox** per multi-select, **TextField** per testo libero
- ✅ **Input sempre in lista verticale** (vedi componenti radio/checkbox)
- ✅ **UN solo Primary** = il submit
- ✅ **Primary a destra** in Button Group Inline

## Esempi

- [Form Valutazione Gioco — 8751:1427](https://www.figma.com/design/QWM2EhgZmv2KKcqI0315fx/?node-id=8751-1427)

## TODO per UX team

- [ ] Validare slot e regole, promuovere a `full`
- [ ] Aggiungere `rationale`
- [ ] Documentare il pattern multi-step form (wizard) se è una variante di questo o un pattern separato
- [ ] Aggiungere esempi di signup, modifica profilo, supporto
