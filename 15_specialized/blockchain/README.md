# ⛓️ Blockchain — Sổ cái phân tán, smart contract & Web3

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 22/06/2026

> 🎯 *Nền tảng blockchain cho lập trình viên: sổ cái phân tán (distributed ledger) là gì và khi nào KHÔNG nên dùng, cách block/hash/Merkle tree hoạt động, smart contract + EVM + gas (Solidity), cơ chế đồng thuận PoW vs PoS, và phát triển Web3 với ethers.js. CÓ code chạy được (Solidity ^0.8, ethers v6, Node crypto), nhiều sơ đồ + ví dụ Alice→Bob xuyên suốt.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu **blockchain = distributed ledger** bất biến, 3 trụ cột (decentralization/immutability/transparency) — và **khi nào KHÔNG nên dùng** (đa số case nên dùng DB thường)
- [x] Nắm cơ chế kỹ thuật: **block → hash → chain**, SHA-256, **Merkle tree**, vòng đời một transaction, 51% attack
- [x] Viết **smart contract** Solidity cơ bản, hiểu **EVM + gas**, token standard **ERC-20/ERC-721**
- [x] Phân biệt **PoW vs PoS**, finality, fork, crypto-economics (incentive)
- [x] Bắt đầu **Web3 dev**: wallet (MetaMask), **ethers.js v6**, testnet, và bẫy bảo mật (reentrancy, overflow)

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`Blockchain là gì?`](./lessons/01_basic/00_what-is-blockchain.md) | ✅ | Distributed ledger, block/hash/chain, vs DB tập trung, khi nào KHÔNG nên dùng. |
| **01** | [`Blockchain hoạt động thế nào?`](./lessons/01_basic/01_how-blockchain-works.md) | ✅ | Cấu trúc block, SHA-256, Merkle tree, vòng đời transaction, 51% attack. |
| **02** | [`Smart Contract & EVM`](./lessons/01_basic/02_smart-contracts-and-evm.md) | ✅ | EVM, gas, Solidity cơ bản, ERC-20/ERC-721, dApp. |
| **03** | [`Đồng thuận & Crypto-economics`](./lessons/01_basic/03_consensus-and-crypto-economics.md) | ✅ | PoW vs PoS, finality, fork, incentive/tokenomics. |
| **04** | [`Phát triển Web3`](./lessons/01_basic/04_web3-development.md) | ✅ | MetaMask, ethers.js v6, testnet, reentrancy, overflow. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04. Bài [00](./lessons/01_basic/00_what-is-blockchain.md) đặc biệt quan trọng vì nói rõ **khi nào blockchain KHÔNG phải lời giải** — đọc trước khi đầu tư thời gian. Người muốn code ngay: nắm [01](./lessons/01_basic/01_how-blockchain-works.md) (hash) rồi sang [02](./lessons/01_basic/02_smart-contracts-and-evm.md) (Solidity) và [04](./lessons/01_basic/04_web3-development.md) (ethers.js). Luôn thử trên **testnet** trước.

## 🔗 Liên kết cụm liên quan

- [12_security](../../12_security/) — bảo mật smart contract, mật mã (hash, chữ ký số).
- [06_databases](../../06_databases/) — đối chiếu blockchain vs database truyền thống.
- [07_web](../../07_web/) — frontend cho dApp (Web3 = web app + smart contract).

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (22/06/2026)** — Hoàn thiện cụm **Basic 5/5** (blockchain là gì + cách hoạt động + smart contract/EVM + đồng thuận/crypto-economics + Web3 dev).
