# Page Pattern — Pagina Dettaglio Prodotto / Gioco / Iniziativa

> Owner: UX team · Status: `draft` · Last updated: 2026-05-22

Pagina dettaglio immersiva per un singolo prodotto del DS Cross-App: gioco (slot, roulette, blackjack, live), lotteria (estrazione, biglietto), bonus, iniziativa promozionale. È una delle page-type più ricorrenti dell'app — l'utente arriva qui dalla home/listing e decide se procedere all'azione principale (giocare, partecipare, riscattare).

## When to use

- L'utente atterra su un **singolo prodotto/gioco identificato** (non un elenco)
- Serve esporre **caratteristiche tecniche** del prodotto (RTP, jackpot, regole, payout)
- L'azione principale della pagina è **una sola** (es. Gioca) — eventualmente affiancata da una secondaria (Prova/Demo)
- Si vuole un'esperienza **immersiva**, brand-pieno, mobile-native

## When NOT to use

- ❌ Pagina con **più prodotti** → usa `listing-products`
- ❌ Pagina di **categoria** senza prodotto specifico in primo piano → usa `homepage` o `listing-*`
- ❌ Pagina di **settings/account** → usa `settings`
- ❌ Pagina **form** di raccolta dati → usa `form-data-collection`

## Anatomia (top-down)

1. **Status Bar OS** (52h iOS / equivalente Android) — chrome di sistema
2. **(no Header)** — vedi anti-pattern `header-in-detail`. La navigazione back è opzionale come overlay floating sul Hero
3. **Hero Detail** — immagine prodotto, nome, partner/provider, chip overlay (Promo, Jackpot, Default), eventuale player button
4. **Card Detail** (variant `caratteristiche di gioco` | `bonus` | `custom`) — caratteristiche fondamentali con accordion "Più info"
5. **TextBox sezioni** (opzionali) — descrizione, come si gioca, regole
6. **Banner** (opzionale) — Gioco certificato / Tipologia di giocatore (trust, no marketing CTA)
7. **Card Informative** (opzionale) — payout effettivo per mese, breakdown numerico drill-down
8. **Card + TextBox nested** (opzionale) — metriche certificate puntuali (es. "Payout certificato 94,54%") — **mai TextBox flat senza container**
9. **Nudge cards** (opzionale) — Feedback o Banner secondari con CTA `Secondary` o `Ghost` (mai Primary)
10. **Button Group sticky** (obbligatorio) — UNA sola Primary = azione principale (Gioca/Acquista/Partecipa) + eventuale Secondary

## Regole non negoziabili

- ✅ **UN solo Primary CTA visibile** in tutta la pagina (lo stickyFooter)
- ❌ **Niente Header** (Top Navigation chrome bordato) — usa Status Bar + Hero immersivo
- ❌ **Niente Card Highlight** — riservato a landing/homepage
- ❌ **Niente Card Entrypoint** — riservato a contesti single-product highlight in homepage/listing
- ✅ **Card Detail e Card Informative possono apparire SOLO qui** (uso esclusivo della page-type)
- ✅ **Container del riferimento → container DS**, mai flatten in display (regola R8 di CLAUDE.md)
- ✅ **Hero Detail occupa la top area** (no chrome bordato sopra)

## Anti-pattern principali

| Scenario | Perché è sbagliato | Alternativa |
|---|---|---|
| `header-in-detail` | Doppia top bar (Header + Hero), riduce immersività, spreca verticale | Status Bar + Hero. Back-arrow come overlay floating ghost sul Hero |
| `multiple-primary-cta-on-detail` | Più Primary verdi confondono la gerarchia visiva | UNA Primary nel sticky. Altre azioni → Secondary o Ghost |
| `card-highlight-in-detail` | Compete col Hero immersivo + sticky Primary | Card Highlight resta in landing/homepage |
| `flatten-container-into-display` | Sostituire Card del riferimento con TextBox solo perde la struttura | Card base + TextBox nested se non c'è una Card specifica DS |

## Esempi

- **Recreated v2** (canonical): [Figma 8774:914](https://www.figma.com/design/QWM2EhgZmv2KKcqI0315fx/?node-id=8774-914) — implementazione iOS Liquid Glass con tutti gli slot canonici
- **Legacy reference** (da rifare): [Figma 8766:8886](https://www.figma.com/design/QWM2EhgZmv2KKcqI0315fx/?node-id=8766-8886) — usa componenti legacy `ready-to-use/*`, NON DS Cross-App

## Composizione canonica (slot map)

Vedi [`composition.json`](composition.json) per la versione machine-readable.

## TODO per UX team

- [ ] Validare l'elenco degli slot e promuovere status a `full`
- [ ] Aggiungere `rationale` con il razionale UX consolidato
- [ ] Confermare la regola "back-arrow come overlay floating ghost" o documentare il pattern esatto
- [ ] Verificare se serve uno slot dedicato per chip overlay sul Hero (oggi parte di Hero Detail)
- [ ] Aggiungere altri esempi canonici (es. dettaglio lotteria, dettaglio bonus) con `figmaNodeId` reali
