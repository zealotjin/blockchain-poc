# Blockchain POC Development Notes

## How to Run the POC

### 1. Environment Setup
```bash
cp .env.example .env
# Edit .env with your private key and RPC URL
```

### 2. Local Testing (Recommended First)
```bash
# Terminal 1: Start local blockchain
npx hardhat node

# Terminal 2: Deploy contracts
npx hardhat run scripts/deploy.js --network localhost

# Terminal 3: Run complete test
source venv/bin/activate
python scripts/test_flow.py
```

### 3. Testnet Deployment
```bash
# Deploy to Base Sepolia (cheaper, faster)
npx hardhat run scripts/deploy.js --network base-sepolia

# Or deploy to Ethereum Sepolia
npx hardhat run scripts/deploy.js --network sepolia
```

### 4. Test the Flow
```bash
# Run complete submission→payout test
python scripts/test_flow.py

# Monitor events in real-time
python scripts/listen_events.py
```

**Required:** Get testnet ETH from faucets for gas fees

---

## 2025-10-01

### Q: Step-by-step setup for blockchain POC project
**A:** Created comprehensive setup guide covering:
- Environment setup (Hardhat/Foundry frameworks)
- Contract development (SubmissionRegistry, VerificationManager, BountyPool)
- Testing & deployment workflow
- Complete submission-to-payout test flow

### Q: What is Hardhat and Foundry used for?
**A:** Both are Ethereum development frameworks:
- **Hardhat**: JS/TS ecosystem, beginner-friendly, extensive tooling
- **Foundry**: Rust-based, faster compilation, Solidity-native testing
- Recommended Hardhat for this POC due to easier interaction scripts

### Q: Does the plan include POC with Layer 2?
**A:** Yes, README specifies L2 testnet support:
- Base Sepolia, Optimism Sepolia, Polygon Amoy, Arbitrum Sepolia
- Same setup works on L2 with updated RPC URLs and L2 stablecoin addresses
- Benefits: lower gas fees, faster confirmations

### Q: Additional work for bridging stablecoins in L2 and L1?
**A:** No additional work needed for POC:
- L2 testnets have native USDC faucets
- No bridging implementation required
- Production users would use existing bridges (Base Bridge, Arbitrum Bridge, etc.)
- Alternative: Deploy MockUSDC contract for pure testing