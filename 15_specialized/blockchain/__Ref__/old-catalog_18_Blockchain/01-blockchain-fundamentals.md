# ⛓️ Blockchain — Công nghệ chuỗi khối

> `[BEGINNER → INTERMEDIATE]` — Hiểu bản chất, không chỉ hype

---

## Blockchain là gì?

**Sổ cái phân tán** (distributed ledger) mà **không ai** có thể sửa dữ liệu đã ghi.

```
Block 0 (Genesis)     Block 1              Block 2
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│ Hash: 0000abc  │◄──│ Prev: 0000abc  │◄──│ Prev: 0000def  │
│ Prev: 000000   │   │ Hash: 0000def  │   │ Hash: 0000ghi  │
│ Data:          │   │ Data:          │   │ Data:          │
│  Genesis block │   │  An → Bình 5₿  │   │  Bình → Cường  │
│ Nonce: 42      │   │ Nonce: 1337    │   │   3₿           │
│ Timestamp      │   │ Timestamp      │   │ Nonce: 7890    │
└────────────────┘   └────────────────┘   └────────────────┘

Sửa Block 1 → Hash thay đổi → Block 2 invalid → Toàn bộ chain broken!
→ Tamper-proof (chống giả mạo)
```

---

## 1. Core Concepts

### Hash Function

```python
import hashlib

def calculate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

calculate_hash("Hello")
# "185f8db32271fe25f561a6fc938b2e26..."

calculate_hash("Hello!")  # Chỉ thêm "!" → hash hoàn toàn khác!
# "334d016f755cd6dc58c53a86e183882f..."

# Tính chất:
# 1. Deterministic: Cùng input → cùng output
# 2. One-way: Không thể từ hash → input
# 3. Avalanche: Thay đổi nhỏ → hash khác hoàn toàn
# 4. Fixed size: Luôn 256 bits (SHA-256)
```

### Proof of Work (Mining)

```python
import hashlib

def mine_block(data, difficulty=4):
    """Tìm nonce sao cho hash bắt đầu bằng '0' * difficulty"""
    nonce = 0
    prefix = '0' * difficulty

    while True:
        text = f"{data}{nonce}"
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        if hash_result.startswith(prefix):
            print(f"Nonce: {nonce}")
            print(f"Hash: {hash_result}")
            return nonce, hash_result
        nonce += 1

mine_block("Block 1: An sends 5 BTC to Binh", difficulty=4)
# Nonce: 54321
# Hash: 0000a3b2c1d0e9f8...
# → Máy phải thử hàng chục nghìn lần → tốn năng lượng → "proof of WORK"
```

### Consensus Mechanisms

```
Proof of Work (PoW):
  Miners cạnh tranh giải bài toán hash → tìm nonce
  ✅ Proven, secure (Bitcoin)
  ❌ Tốn điện khủng khiếp

Proof of Stake (PoS):
  Validators lock (stake) token → được chọn random xác nhận block
  ✅ Tiết kiệm 99.9% điện (Ethereum 2.0)
  ❌ "Rich get richer" → centralization risk

Delegated PoS (DPoS):
  Holders vote chọn validators
  ✅ Nhanh (Solana: 65,000 TPS)
  ❌ Ít validators → semi-centralized
```

---

## 2. Smart Contracts

```solidity
// Solidity — ngôn ngữ Ethereum Smart Contract
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleToken {
    string public name = "MyToken";
    string public symbol = "MTK";
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
    }

    function transfer(address _to, uint256 _amount) public returns (bool) {
        require(balanceOf[msg.sender] >= _amount, "Insufficient balance");
        require(_to != address(0), "Invalid address");

        balanceOf[msg.sender] -= _amount;
        balanceOf[_to] += _amount;

        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
}
```

```
Smart Contract = Code chạy trên blockchain

Đặc điểm:
✅ Immutable: Deploy rồi không sửa được code
✅ Transparent: Ai cũng đọc được code
✅ Trustless: Không cần trung gian (bank, lawyer)
✅ Automatic: Điều kiện thỏa → auto execute

Ứng dụng:
• DeFi: Lending, Swap, Staking → không cần bank
• NFT: Chứng nhận sở hữu digital assets
• DAO: Tổ chức quản trị phi tập trung
• Supply chain: Tracking hàng hóa từ gốc
```

---

## 3. Web3 Development

```javascript
// ethers.js — Tương tác Ethereum
import { ethers } from 'ethers';

// Connect wallet
const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();
const address = await signer.getAddress();

// Read blockchain
const balance = await provider.getBalance(address);
console.log(`Balance: ${ethers.formatEther(balance)} ETH`);

// Interact with smart contract
const contract = new ethers.Contract(contractAddress, abi, signer);
const name = await contract.name();              // Read (free)
const tx = await contract.transfer(to, amount);  // Write (gas fee)
await tx.wait();                                  // Đợi confirm
```

---

## 4. So sánh Blockchains

| | Bitcoin | Ethereum | Solana | Polygon |
|---|---|---|---|---|
| **Consensus** | PoW | PoS | PoH+PoS | PoS |
| **TPS** | 7 | 30 | 65,000 | 7,000 |
| **Gas fee** | $1-20 | $1-50 | $0.001 | $0.01 |
| **Smart Contracts** | Limited | ✅ Solidity | ✅ Rust | ✅ Solidity |
| **Use case** | Store of value | DeFi, NFT, DAO | High-speed DeFi | Scaling Ethereum |

---

## 5. DeFi — Tài chính phi tập trung

```
Traditional Finance:          DeFi:
Bank giữ tiền bạn         →  Bạn giữ tiền (wallet)
Bank cho vay, lấy lãi     →  Smart contract cho vay, chia lãi
Broker mua/bán chứng khoán→  DEX (Uniswap) swap token trực tiếp
Bảo hiểm qua công ty      →  Smart contract bảo hiểm tự động

Protocols phổ biến:
• Uniswap:  DEX (swap tokens)
• Aave:     Lending/Borrowing
• MakerDAO: Stablecoin (DAI)
• Lido:     Liquid staking
```

---

## Các lỗi thường gặp

```
❌ Sai: "Blockchain giải quyết mọi vấn đề"
✅ Đúng: Blockchain chậm, đắt → chỉ dùng khi CẦN trustless + immutable

❌ Sai: Smart contract deploy rồi không ai hack được
✅ Đúng: Code bugs → millions lost. PHẢI audit trước deploy!

❌ Sai: "Blockchain = Bitcoin = tiền ảo"
✅ Đúng: Blockchain là TECHNOLOGY, crypto là 1 ỨNG DỤNG của nó
```

---

## Bài tập thực hành

- [ ] Implement blockchain đơn giản bằng Python (Block, Chain, Mining)
- [ ] Deploy smart contract trên Ethereum testnet (Sepolia)
- [ ] Build DApp: connect wallet + read/write smart contract
- [ ] Tạo ERC-20 token và deploy lên testnet

---

## Tài nguyên thêm

- [CryptoZombies](https://cryptozombies.io/) — Learn Solidity by building game
- [Ethereum Docs](https://ethereum.org/developers) — Official
- [Blockchain Demo](https://andersbrownworth.com/blockchain/) — Visual demo
