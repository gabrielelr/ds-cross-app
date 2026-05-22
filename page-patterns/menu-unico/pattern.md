# Page Pattern — Menu Unico

> Owner: UX team · Status: `draft` · Last updated: 2026-05-22

Menu principale dell'app — **single entry point** per tutte le azioni account/settings/info dell'utente. Accessibile dal hamburger del Header o da tab bar. È una pagina dedicata, **non un drawer/sheet**.

## When to use

- L'utente cerca azioni account / settings / info / supporto
- Serve aggregare in un unico posto tutti gli ingressi non-gioco dell'app

## When NOT to use

- ❌ **Scorciatoie veloci in-page** → usa Square Button Group / Quicklink standalone, non duplicare il menu
- ❌ **Editing dati account** → ogni voce naviga a pagina dedicata, non editing inline
- ❌ **Promo / marketing** → homepage / listing, non menu

## Varianti

7 varianti per stato utente:

1. **No Log** — utente non autenticato (CTA Accedi/Registrati, niente saldo/bonus)
2. **Log** — utente autenticato pieno (UserHeader + QuickActions + Bonus list + Sisal Community + …)
3. **Sessione Pending** — sessione in attesa
4. **Autoesclusione GAD** — utente autoescluso (Ricarica DISABILITATA per compliance)
5. **Errore Bonus** — fallback Feedback al posto del bonus list
6. **Errore Saldo** — fallback Feedback al posto del balance
7. **Errore Saldo e Bonus** — entrambi i fallback

## Regole

- ✅ **UNA Primary CTA per pagina**: tipicamente **Ricarica** in variante Log, o **Registrati** in variante No Log
- ✅ **Single source of truth** — niente duplicazione in drawer/sheet
- ✅ **Niente editing inline** — drill-down a pagine dedicate
- ✅ **Niente marketing CTA** (eccezione: Card Loyalty Sisal Community)
- ✅ **QuickActions = Square Button Group** (NON Circle)

## Esempi

- [Menu Unico GAD — 8763:7618](https://www.figma.com/design/QWM2EhgZmv2KKcqI0315fx/?node-id=8763-7618) — reference esistente con 3 violazioni note (vedi `composition.json#compositionExamples`)

## TODO per UX team

- [ ] Promuovere status a `full`
- [ ] Riallinearsi sul componente QuickActions corretto (Square vs Circle): doc dice Square, Figma reference usa Circle. Decidere e aggiornare.
- [ ] Documentare quali slot devono essere disabilitati in variante Autoesclusione GAD (Ricarica? bonus tappabili?)
- [ ] Aggiungere esempio canonico Variant=Log completo (oggi abbiamo solo GAD con violazioni)
