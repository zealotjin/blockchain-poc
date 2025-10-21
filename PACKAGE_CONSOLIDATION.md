# Package Consolidation Guide

This document consolidates all key packages and dependencies for the blockchain-poc project, organized by component for easy migration to a new repository.

## Project Overview
- **Type**: Blockchain Proof of Concept
- **Stack**: Solidity Smart Contracts + Python Backend + React Frontend
- **Blockchain Tools**: Hardhat (development), Web3.py (Python), Wagmi/Viem (Frontend)

---

## 1. Smart Contract Development (Hardhat + Solidity)

### Core Configuration
- **Solidity Version**: `0.8.20`
- **Networks**: Sepolia, Base Sepolia

### Node.js Dependencies

#### Root `package.json`
```json
{
  "devDependencies": {
    "@nomicfoundation/hardhat-toolbox": "^6.1.0",
    "@openzeppelin/contracts": "^5.4.0",
    "hardhat": "^2.26.3"
  },
  "dependencies": {
    "dotenv": "^17.2.3"
  }
}
```

**Key Packages:**
- `hardhat` (^2.26.3) - Ethereum development environment
- `@nomicfoundation/hardhat-toolbox` (^6.1.0) - Bundle of Hardhat plugins
- `@openzeppelin/contracts` (^5.4.0) - Secure smart contract library
- `dotenv` (^17.2.3) - Environment variable management

---

## 2. Python Backend (FastAPI + Web3)

### Python Dependencies

#### `requirements.txt`
```
web3==6.11.0
python-dotenv==1.0.0
fastapi==0.104.1
uvicorn[standard]==0.24.0
pytest==7.4.3
eth-account==0.9.0
requests==2.31.0
```

**Key Packages:**
- `web3` (6.11.0) - Python library for Ethereum interaction
- `fastapi` (0.104.1) - Modern web framework for building APIs
- `uvicorn` (0.24.0) - ASGI server for FastAPI
- `eth-account` (0.9.0) - Ethereum account management
- `python-dotenv` (1.0.0) - Environment variable management
- `pytest` (7.4.3) - Testing framework
- `requests` (2.31.0) - HTTP library

---

## 3. React Frontend (TypeScript + Wagmi)

### Frontend Dependencies

#### `frontend/frontend/package.json`

**Production Dependencies:**
```json
{
  "@rainbow-me/rainbowkit": "^2.2.8",
  "@tanstack/react-query": "^5.90.2",
  "react": "^19.2.0",
  "react-dom": "^19.2.0",
  "react-scripts": "5.0.1",
  "typescript": "^5.9.3",
  "viem": "^2.37.11",
  "wagmi": "^2.17.5",
  "web-vitals": "^2.1.4",
  "openapi-fetch": "^0.14.0"
}
```

**Testing Dependencies:**
```json
{
  "@testing-library/dom": "^10.4.1",
  "@testing-library/jest-dom": "^6.9.1",
  "@testing-library/react": "^16.3.0",
  "@testing-library/user-event": "^13.5.0",
  "@types/jest": "^27.5.2",
  "@types/node": "^16.18.126",
  "@types/react": "^19.2.0",
  "@types/react-dom": "^19.2.0"
}
```

**Build & Polyfill Dependencies (DevDependencies):**
```json
{
  "@craco/craco": "^7.1.0",
  "react-app-rewired": "^2.2.1",
  "assert": "^2.1.0",
  "buffer": "^6.0.3",
  "crypto-browserify": "^3.12.1",
  "https-browserify": "^1.0.0",
  "os-browserify": "^0.3.0",
  "path-browserify": "^1.0.1",
  "process": "^0.11.10",
  "stream-browserify": "^3.0.0",
  "stream-http": "^3.2.0",
  "url": "^0.11.4",
  "vm-browserify": "^1.1.2"
}
```

**Key Packages:**
- `wagmi` (^2.17.5) - React hooks for Ethereum
- `viem` (^2.37.11) - TypeScript library for Ethereum
- `@rainbow-me/rainbowkit` (^2.2.8) - Wallet connection UI
- `@tanstack/react-query` (^5.90.2) - Data fetching/caching
- `react` (^19.2.0) - UI framework
- `typescript` (^5.9.3) - Type safety
- `react-app-rewired` (^2.2.1) - Override create-react-app config
- Node.js polyfills for browser compatibility

---

## 4. Smart Contracts Deployed

The project includes these Solidity contracts:
- `BountyPool.sol` - Manages bounty funds and payouts
- `SubmissionRegistry.sol` - Records submissions
- `VerificationManager.sol` - Handles verification logic
- `MockUSDT.sol` - Test ERC20 token

---

## 5. Minimum Setup Commands for New Repository

### Initial Setup
```bash
# 1. Install Node.js dependencies (Hardhat)
npm install

# 2. Install Python dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Install Frontend dependencies
cd frontend/frontend
npm install
cd ../..
```

### Environment Variables Required
Create `.env` file with:
```
PRIVATE_KEY=your_private_key_here
RPC_URL=your_rpc_url_here
```

### Compile & Deploy
```bash
# Compile contracts
npx hardhat compile

# Deploy contracts
npx hardhat run scripts/deploy.js --network sepolia
```

### Run Backend
```bash
source venv/bin/activate
python main.py
```

### Run Frontend
```bash
cd frontend/frontend
npm start
```

---

## 6. Critical Files to Include in Migration

### Configuration Files
- `hardhat.config.js` - Hardhat network configuration
- `package.json` - Root Node.js dependencies
- `requirements.txt` - Python dependencies
- `frontend/frontend/package.json` - Frontend dependencies
- `frontend/frontend/config-overrides.js` - Webpack config overrides
- `frontend/frontend/tsconfig.json` - TypeScript configuration

### Smart Contracts
- All `.sol` files in `/contracts/`

### Python Backend
- `main.py` - FastAPI server
- `config/blockchain_config.py` - Blockchain configuration
- Scripts in `/scripts/` directory

### Frontend Source
- All files in `frontend/frontend/src/`
- Public assets in `frontend/frontend/public/`

### Documentation
- `README.md` - Project documentation
- `NOTES.md` - Additional notes

---

## 7. Architecture Summary

```
blockchain-poc/
├── Smart Contracts (Solidity)
│   └── Hardhat + OpenZeppelin
├── Backend (Python)
│   └── FastAPI + Web3.py
└── Frontend (React/TypeScript)
    └── Wagmi + RainbowKit + Viem
```

**Blockchain Integration Flow:**
1. Smart contracts deployed via Hardhat
2. Python backend interacts with contracts via Web3.py
3. Frontend connects to blockchain via Wagmi/Viem
4. Users connect wallets via RainbowKit

---

## 8. Version Compatibility Notes

- **Node.js**: Recommended v16+ (tested with latest LTS)
- **Python**: Requires Python 3.9+ (venv uses python3.9)
- **Solidity**: 0.8.20
- **React**: Version 19.2.0 (latest)
- **TypeScript**: 5.9.3

---

## 9. Network Configuration

The project is configured for:
- **Sepolia Testnet**: Ethereum testnet
- **Base Sepolia**: Base Layer 2 testnet

Both require RPC URLs and a funded wallet private key in `.env`

---

## Quick Migration Checklist

- [ ] Copy all `/contracts/*.sol` files
- [ ] Copy `hardhat.config.js`, root `package.json`
- [ ] Copy `requirements.txt`, `main.py`, `/config/`, `/scripts/`
- [ ] Copy entire `/frontend/frontend/` directory
- [ ] Copy `.env` file (or create new with keys)
- [ ] Run `npm install` in root
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `npm install` in `frontend/frontend/`
- [ ] Compile contracts: `npx hardhat compile`
- [ ] Deploy and test

---

**Document Generated**: October 10, 2025
**Project**: blockchain-poc

