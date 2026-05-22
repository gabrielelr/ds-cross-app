---
component: Filter
figma_id: "6061:50191"
last_updated: 2026-05-22
---

## Changelog

- **2026-05-22** — Documentazione completa. Template Bottom Sheet di filtraggio modale (organism). Composto da Bottom Sheet + Drag Handle + Header sticky con close X + Body scrollabile con Hero h1 + N FilterSection (TextBox h3+p + FilterRow di Chip md multi-select) + Button Group sticky (secondary 'Delete filters' + primary 'See results (N)' con count live). Pattern: FAB Filter → sheet → multi-select Chip → conferma con count. Token `filterRow/size/gap` (4). Anti-pattern: fullscreen page, missing count in CTA, auto-apply on chip tap, single-select forced.
- **2026-05-14** — Scaffold iniziale.
