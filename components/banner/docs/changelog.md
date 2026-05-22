---
component: Banner (family)
figma_id: "5805:40527"
last_updated: 2026-05-21
---

# Banner family

Famiglia di componenti Banner del Design System Cross-App. Raggruppa il Banner base (`banner-template`) e i suoi template specifici (istanze strutturalmente distinte per use-case verticale).

## Membri della famiglia

| Slug | Cosa | Figma node |
|---|---|---|
| `banner-template` | Banner base — 3 `Text Type` (Title+Paragraph, Centered Text, Title Only) | 5805:40527 |
| `banner-ruota-bonus` | Template iniziativa Ruota dei Bonus (giro giornaliero Sisal) — strip 72h orizzontale | 6242:3633 |
| `banner-race` | Template race/tornei con classifica (Daily Quick Race) — split text+image | 6257:36597 |
| `banner-gioco-certificato` | Template compliance/gioco responsabile — text+Link+shield illustration | 6497:5048 |
| `banner-help-center` | Template entry-point al supporto — text + 1 Button outline (h2) | 6564:25055 |
| `banner-tipologia-giocatore` | Template self-assessment di gioco responsabile — text con 2 paragraph + 1 Button | 6395:3337 |
| `banner-community` | Template Community con tutor — avatar + handle + badge "Tutor", list-like | 6583:31741 |

## Changelog

- **2026-05-21** — Famiglia consolidata in `components/banner/`. Compilata documentazione completa per tutti i 7 banner (base + 6 template). Stabilita la convenzione: i template strutturalmente diversi dal base sono componenti dedicati, non commonPatterns.
- **2026-05-20** — Scaffold iniziale singolo `banner/`.
