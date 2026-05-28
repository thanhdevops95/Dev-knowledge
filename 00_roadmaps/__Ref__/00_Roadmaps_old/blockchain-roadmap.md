# ⛓️ Lộ trình Blockchain Developer

> `[BEGINNER → ADVANCED]` — Xem trước [Tổng quan Lộ trình](./00-overview.md)

---

## Tại sao Blockchain?

Blockchain giống như một "sổ cái công khai" mà không ai có thể giả mạo — mọi giao dịch đều minh bạch và không thể thay đổi. Từ tiền mã hóa đến supply chain, digital identity, và DeFi, công nghệ này đang tạo ra một hệ thống tài chính và ứng dụng phi tập trung hoàn toàn mới.

Blockchain developer không chỉ viết code — bạn đang thiết kế **hệ thống tin cậy** (trustless systems). Mỗi dòng code trong smart contract đều có thể quản lý hàng triệu đô, nên security là ưu tiên số một.

---

## Sơ đồ lộ trình

```
Blockchain Fundamentals
    │
    ▼
Solidity & Smart Contracts
    │
    ├──► Smart Contracts Advanced (Patterns, Gas, Upgradeable)
    │
    ├──► Web3 Frontend (ethers.js, wagmi)
    │
    ├──► DeFi Concepts (AMM, Lending, Yield)
    │
    ▼
Testing & Security (Hardhat, Foundry, Auditing)
    │
    ▼
Full dApp Development & Deployment
```

---

## Giai đoạn 1 — Blockchain Fundamentals

- [ ] Blockchain là gì? Consensus, Mining, Nodes → [../18-Blockchain/01-blockchain-fundamentals.md](../18-Blockchain/01-blockchain-fundamentals.md)
- [ ] Bitcoin vs Ethereum — sự khác biệt
- [ ] Wallets, Transactions, Gas fees
- [ ] Decentralization, Immutability, Transparency

---

## Giai đoạn 2 — Solidity cơ bản

- [ ] Solidity syntax & types → [../18-Blockchain/ethereum/01-solidity-basics.md](../18-Blockchain/ethereum/01-solidity-basics.md)
- [ ] Functions, Modifiers, Events
- [ ] Storage vs Memory vs Calldata
- [ ] ERC-20, ERC-721 (NFT), ERC-1155 standards

---

## Giai đoạn 3 — Smart Contracts nâng cao

- [ ] Design patterns (Factory, Proxy, Diamond) → [../18-Blockchain/ethereum/02-smart-contracts-advanced.md](../18-Blockchain/ethereum/02-smart-contracts-advanced.md)
- [ ] Gas optimization techniques
- [ ] Upgradeable contracts (UUPS, Transparent Proxy)
- [ ] Reentrancy, Integer overflow, Access control vulnerabilities

---

## Giai đoạn 4 — Web3 Frontend

- [ ] ethers.js / viem cơ bản → [../18-Blockchain/web3/01-web3js-ethers-basics.md](../18-Blockchain/web3/01-web3js-ethers-basics.md)
- [ ] wagmi + RainbowKit (React hooks cho Web3)
- [ ] Kết nối wallet (MetaMask, WalletConnect)
- [ ] Đọc/ghi data từ smart contract

---

## Giai đoạn 5 — DeFi Concepts

- [ ] DeFi fundamentals → [../18-Blockchain/defi/01-defi-fundamentals.md](../18-Blockchain/defi/01-defi-fundamentals.md)
- [ ] AMM (Automated Market Maker) — Uniswap
- [ ] Lending/Borrowing — Aave, Compound
- [ ] Yield farming, Liquidity pools
- [ ] Flash loans & MEV

---

## Giai đoạn 6 — Testing & Security

- [ ] Hardhat — local blockchain, testing, deployment
- [ ] Foundry (Forge) — fast Solidity testing framework
- [ ] Smart contract auditing methodology
- [ ] Common vulnerabilities (SWC Registry)
- [ ] Formal verification basics

---

## 📦 Project thực hành

| Giai đoạn | Project |
|---|---|
| Sau Solidity | Token ERC-20 + deploy lên testnet |
| Sau Web3 | dApp với wallet connect + đọc/ghi contract |
| Sau DeFi | Clone Uniswap đơn giản (token swap) |
| Sau Security | Hoàn thành Ethernaut challenges (all levels) |
| Nâng cao | Full DeFi protocol: Lending + Governance + Frontend |

---

## 📚 Tài nguyên

- [CryptoZombies](https://cryptozombies.io/) — Học Solidity qua game, miễn phí
- [Ethernaut](https://ethernaut.openzeppelin.com/) — Smart contract security challenges
- [Buildspace](https://buildspace.so/) — Build Web3 projects từ đầu
- [Patrick Collins — Blockchain Course](https://www.youtube.com/watch?v=gyMwXuJrbJQ) — Khóa học miễn phí 32h trên YouTube
- [Solidity by Example](https://solidity-by-example.org/) — Học Solidity qua ví dụ thực tế
