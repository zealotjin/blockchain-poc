import React from 'react';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { useAccount, useBalance, useChainId } from 'wagmi';

const WalletConnection: React.FC = () => {
  const { address, isConnected, status } = useAccount();
  const chainId = useChainId();
  const { data: ethBalance, isLoading: balanceLoading } = useBalance({
    address: address,
  });

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '1rem',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      marginBottom: '2rem'
    }}>
      <div>
        <h3 style={{ margin: 0, marginBottom: '0.5rem' }}>🔗 Wallet Connection</h3>
        {isConnected && status === 'connected' ? (
          <div>
            <p style={{ margin: 0, fontSize: '0.9rem', color: '#666' }}>
              <strong>Network:</strong> {chainId === 31337 ? 'Localhost (Hardhat)' : `Chain ${chainId}`}
            </p>
            <p style={{ margin: 0, fontSize: '0.9rem', color: '#666' }}>
              <strong>ETH Balance:</strong> {
                balanceLoading ? 'Loading...' :
                ethBalance ? `${Number(ethBalance.value) / 1e18} ETH` : 'Error loading balance'
              }
            </p>
            <p style={{ margin: 0, fontSize: '0.9rem', color: '#666' }}>
              <strong>Address:</strong> <code style={{ fontSize: '0.8rem' }}>{address}</code>
            </p>
          </div>
        ) : (
          <p style={{ margin: 0, fontSize: '0.9rem', color: '#666' }}>
            Connect your wallet to interact with the blockchain
          </p>
        )}
      </div>

      <div>
        <ConnectButton />
      </div>
    </div>
  );
};

export default WalletConnection;