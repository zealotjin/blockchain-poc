import { createConfig, http } from 'wagmi';
import { defineChain } from 'viem';
import { injected } from 'wagmi/connectors';

// Define localhost chain for Hardhat
const localhost = defineChain({
  id: 31337,
  name: 'Localhost',
  nativeCurrency: {
    decimals: 18,
    name: 'Ether',
    symbol: 'ETH',
  },
  rpcUrls: {
    default: {
      http: ['http://127.0.0.1:8545'],
    },
  },
  blockExplorers: {
    default: {
      name: 'Local Explorer',
      url: 'http://localhost:8545',
    },
  },
  testnet: true,
});

export const config = createConfig({
  chains: [localhost],
  connectors: [
    injected(), // Only use injected connector (MetaMask)
  ],
  transports: {
    [localhost.id]: http(),
  },
});

// Contract addresses (from deployments/addresses.json)
export const CONTRACT_ADDRESSES = {
  mockUSDT: '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0',
  submissionRegistry: '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9',
  verificationManager: '0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9',
  bountyPool: '0x5FC8d32690cc91D4c39d9d3abcBD16989F875707',
};