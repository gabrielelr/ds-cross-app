# Page Pattern — Bottom Sheet modale

> Owner: UX team · Status: `draft` · Last updated: 2026-05-22

Layer modale che si presenta dal basso sopra una pagina sottostante (mantenuta visibile via backdrop scuro). Usato per filter, dropdown choice, conferma azione, dettagli rapidi.

## When to use

- Serve **modificare uno stato della pagina sotto** senza dismetterla (filter, sort, conferma)
- Lo user task è **breve** (configurazione 1-2 step + conferma)
- Si vuole **preservare contesto visivo** della pagina sottostante

## When NOT to use

- ❌ Task **lungo e complesso** (multi-step form) → page dedicata `form-data-collection`
- ❌ Navigazione a **un'altra sezione dell'app** → page navigation, non modal
- ❌ **Single text alert / notifica** → toast / inline feedback, non Bottom Sheet

## Regole

- ✅ Backdrop scuro 80% — tap chiude senza applicare
- ✅ Drag Handle sempre presente (iOS detente, Android swipe-dismiss)
- ✅ Header dedicato del sheet (NON Top Navigation Header)
- ✅ Button Group sticky bottom con max 1 Primary
- ✅ Per filter: count live nel CTA primary 'See results (N)' — niente apply-on-tap

## Esempi

- [Filter Bottom Sheet — 6061:50191](https://www.figma.com/design/QWM2EhgZmv2KKcqI0315fx/?node-id=6061-50191)

## TODO per UX team

- [ ] Documentare i detente iOS (medium / large) e le size canoniche del drawer
- [ ] Pattern per dropdown choice modale (è la stessa cosa di un filter modale o ha pattern diverso?)
- [ ] Pattern per "confirm action" modale (delete account, logout, ecc.) — Button Group con Primary "Annulla" (safe) o "Conferma" (destructive)?
