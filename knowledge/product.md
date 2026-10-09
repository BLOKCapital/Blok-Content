# Product Deep-Dive

Sources: blokcapital.io, docs.blokcapital.io (snapshot in `snapshots/`). Last verified 2026-10-09.

## One-liners (pick by context)
- **Plain:** BLOK Capital lets anyone grow their crypto like a wealth manager would, without handing over their keys.
- **Investor:** Plant a Garden, pick an index, let it rebalance itself. Your keys never leave your wallet.
- **Anti-TradFi:** Wealth management without the 2-and-20, the minimums, or the quarterly PDF.
- **Builder:** An open-source, EIP-2535 Diamond-based asset-management protocol on Arbitrum. Compose with Gardens.
- **Gardener:** Publish your strategy, take clients, and build a track record nobody can fake.

## The problem
- Traditional wealth management is gated: minimums, accreditation, geography.
- It's opaque: off-chain decisions, delayed reporting, "trust us" quarterly PDFs.
- It's expensive: "2-and-20" fees to buy the same few assets.
- It's custodial: you hand over your assets (and we've all seen how custodial crypto can end).
- Crypto itself is built for traders: charts, leverage, noise. Normal people with jobs get wrecked or give up.

## The solution
| Problem | BLOK answer |
|---|---|
| Gatekeeping | From 10 USDC, no accreditation, no geo restrictions, no KYC at protocol layer |
| Opacity | Every position and transaction on-chain: receipts, not reports |
| Fees | Gasless; no platform fees today; future fees set by DAO vote |
| Custody risk | Non-custodial smart wallet; nobody can withdraw but you |
| Complexity | Google sign-in, no seed phrase; curated Indices rebalance automatically |
| Trust in managers | Gardeners' track records are on-chain in soulbound badges; they can trade but never withdraw |

## How it works
1. **Sign in with Google**, which creates an ERC-4337 smart wallet (Web3Auth MPC + ZeroDev/Pimlico). No seed phrase.
2. **Referral → soulbound pass** (Builder / Baddie / Angel, etc.). Each pass unlocks one Garden in a collection.
3. **Create a Garden**, a personal Diamond (EIP-2535) contract deployed by the GardenFactory. Up to 10 per user.
4. **Fund it** (Transak on-ramp available; from 10 USDC).
5. **Choose mode:**
   - **Index Garden:** connects to an Index (e.g. market-cap weighted). The Rebalancer Network
     rebalances all connected Gardens in batched transactions. Two-step intent → execute on a later
     block (anti flash-loan), with a 0.5% max portfolio-value-drop check and 2% per-asset tolerance.
     Min 1 hour between rebalances. Chainlink price feeds.
   - **Self-managed Garden:** swap, lend, borrow yourself via integrated DeFi (Uniswap, Camelot, GMX, Aave, Pendle).
6. **Track:** portfolio value, P&L, allocation, rebalancing history, swaps, fees, approvals.
7. **Govern:** DAO tab; voting power = BLOKC held (Aragon OSx).

## Gardeners (coming soon)
Verified managers publish strategies and take clients. They can trade/swap inside a client's
Garden under smart-contract terms but **cannot transfer funds out**. Performance is recorded in a
non-transferable ERC-5484 reputation badge. Investors can switch Gardeners anytime.

## Architecture (for builder content)
- EIP-2535 Diamond per Garden; facets registered in a central Facet Registry; Base Module (Cut, Loupe, Ownership, Upgrade) in every Garden.
- EIP-1967 transparent proxies for factory and registries.
- EIP-7201 namespaced storage.
- Governance: Aragon OSx; Security Council Members tracked via ENS.
- Cross-chain USDC via Circle CCTP (roadmap).
- MIT licensed. Repo: github.com/BLOKCapital.

## Roadmap (forward-looking targets, not promises)
- Q2 2026: curated indices BLOKC2 / BLOKC5 / BLOKC10
- Q2 2027: $BLOKC IDO
- Q4 2027: cross-chain Gardens (Arbitrum, Base, more)
Confirm current status with the team before referencing any of these as live.

## Ecosystem / integrations
Uniswap · Camelot · GMX · Aave · Pendle · Chainlink · Web3Auth · ZeroDev · Pimlico · Transak · Aragon · QuickSwap (logo on site)
Security reviewers: CredShields · SolidityScan · Octane. Bug bounty: Immunefi (announced). Audit contests: Cantina, Code4rena (announced).
