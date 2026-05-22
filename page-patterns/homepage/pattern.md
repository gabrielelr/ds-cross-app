# Page Pattern — Homepage

> Owner: UX team · Status: `draft` · Last updated: 2026-05-22

Landing principale dell'app dopo splash/login. Brand identity, scorciatoie ai prodotti, surface di promo/contenuti raccomandati. Esiste in 2 macro-stati: logged-out e logged-in.

## When to use

- Schermata di **atterraggio iniziale** dell'app
- Serve mostrare il **brand**, dare accesso veloce alle **macro-sezioni** (Casinò, Scommesse, Bingo, …), e fare **surfacing** di promo/contenuti

## When NOT to use

- ❌ Pagina di **categoria specifica** (es. "tutti gli slot") → usa `listing-products`
- ❌ Pagina **dettaglio** di un prodotto → usa `detail-product-game`
- ❌ Pagina **account / settings** → usa `menu-unico` o `settings`

## Regole

- ✅ Header lvl Homepage (brand + Accedi/Balance + menu)
- ✅ **Max 1 Card Highlight** per pagina (rule R7 di CLAUDE.md)
- ✅ **Max 1 Card Entrypoint** per layout
- ✅ Per Card Product grid: usare **Grid Template di contesto** (Lotterie, Casinò, …), non Card Product flat
- ✅ Bottom Navbar SEMPRE presente

## Anti-pattern

| Scenario | Perché | Alternativa |
|---|---|---|
| Multiple Card Highlight | "One per page" — dilema quale promuovere | Una sola + altre in Card Promo Carousel |
| Card Product Grid generico | Perde metadata/size del contesto | Usa Grid Template - Lotterie / Casinò / ecc. |
| No Bottom Navbar | Perde orientamento app | Bottom Navbar sempre |

## TODO per UX team

- [ ] Aggiungere esempi canonici (Figma node IDs) di homepage Sisal logged-out e logged-in
- [ ] Specificare quali macro-sezioni vanno nella Quicklink Navigation (e in che ordine)
- [ ] Documentare come variano gli slot tra brand (Sisal/Snai/Pokerstars)
- [ ] Aggiungere il pattern per la sezione "Continua a giocare" (recent games carousel) — è uno slot opzionale?
