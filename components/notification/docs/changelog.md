---
component: Notification
figma_id: ""
last_updated: 2026-06-18
---

## 2026-06-18

- Rinominato il componente da `Badge Notification` a **Notification** (slug `notification`). Il componente non fa più parte della famiglia Badge: ora è specificamente un marker di notifica che segue le convenzioni native (iOS HIG + Material Design 3).
- Estesa la lista dei parent (`composition.commonPartners`): aggiunti `FAB` e `Banner Community` oltre agli host icona già esistenti (Header, Navbar, Tab Navigation, Menu Unico).
- Aggiornati `description`, `accessibility`, `aiHints` e `parentConstraints` per riflettere che l'host non è più limitato a un'icona 24×24, ma può essere qualsiasi element che ospiti un overflow visivo in corner top-right.
- Rinominato l'anti-pattern `badge-without-icon-host` in `notification-without-host` con linguaggio generalizzato.
- **Rimosso `Type=99+`** dal varianti set: non serviva. Componente ora 2 `Type` (`number`, `circle`) × 4 `Appearance` (`Alert`, `Neutral`, `Brand`, `Inverse`) = 8 combinazioni.
- Aggiunto asse `Appearance` con 4 valori semantici: Alert (rosso, urgente), Neutral (dark, bassa enfasi), Brand (brand-bound multi-brand, per contesti brandizzati), Inverse (bianco + text scuro, per host su superfici scure).
- Aggiornati `commonPatterns` (rimosso `overflow-count-99-plus`, ristrutturati gli altri per riflettere Type × Appearance, aggiunti `neutral-low-emphasis`, `brand-aligned-notification`, `inverse-on-dark-surface`).
- Aggiornati `antiPatterns` (rimosso `number-with-3-digit-count`, ridefinito `circle-when-count-is-meaningful`, aggiunto `wrong-appearance-for-context`).
- Sincronizzati `composition.slots.Badge`, `accessibility.screenReader` e `aiHints.context` con la nuova struttura.
