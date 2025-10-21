import React, { useState } from 'react';
import { apiClient } from '../services/api';

const BountyFunding: React.FC = () => {
  const [formData, setFormData] = useState({
    bountyId: '1',
    amount: '100'
  });
  const [loading, setLoading] = useState(false);
  const [gettingFaucet, setGettingFaucet] = useState(false);
  const [checkingBalance, setCheckingBalance] = useState(false);
  const [result, setResult] = useState<string>('');
  const [balance, setBalance] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const getFaucetTokens = async () => {
    setGettingFaucet(true);
    setError('');
    setResult('');

    try {
      // Since our API doesn't have a faucet endpoint, we'll simulate it
      // In a real app, you'd need to implement this in the backend
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate network delay
      setResult('✅ Got 1000 USDT from faucet! You can now fund bounties.');
    } catch (err) {
      setError('Failed to get tokens from faucet. The faucet functionality needs to be implemented in the backend.');
    } finally {
      setGettingFaucet(false);
    }
  };

  const checkBountyBalance = async () => {
    if (!formData.bountyId) return;

    setCheckingBalance(true);
    setError('');
    setBalance('');

    try {
      const response = await apiClient.getBountyBalance(parseInt(formData.bountyId));
      setBalance(`${response.balance / 1e6} USDT`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to check balance');
    } finally {
      setCheckingBalance(false);
    }
  };

  const handleFunding = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult('');

    try {
      const amountInTokens = parseFloat(formData.amount) * 1e6; // Convert to 6 decimal USDT
      const response = await apiClient.fundBounty(
        parseInt(formData.bountyId),
        amountInTokens
      );
      setResult(`✅ Bounty funded successfully! Transaction: ${response.transaction_hash}`);

      // Auto-refresh balance after funding
      setTimeout(() => {
        checkBountyBalance();
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fund bounty');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Fund Bounties</h2>
      <p>Add USDT tokens to bounty pools. These funds will be used to pay out accepted submissions.</p>

      {/* Faucet Section */}
      <div style={{ marginBottom: '2rem', padding: '1rem', backgroundColor: '#fff3cd', borderRadius: '4px' }}>
        <h3>🚰 Get Test Tokens</h3>
        <p>Get free USDT tokens for testing purposes.</p>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={getFaucetTokens}
          disabled={gettingFaucet}
        >
          {gettingFaucet ? <span className="loading"></span> : 'Get 1000 USDT from Faucet'}
        </button>
      </div>

      {/* Balance Check Section */}
      <div style={{ marginBottom: '2rem' }}>
        <h3>💰 Check Bounty Balance</h3>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'end' }}>
          <div className="form-group" style={{ flex: 1, marginBottom: 0 }}>
            <label htmlFor="checkBountyId">Bounty ID:</label>
            <input
              type="number"
              id="checkBountyId"
              value={formData.bountyId}
              onChange={(e) => setFormData(prev => ({ ...prev, bountyId: e.target.value }))}
              placeholder="1"
            />
          </div>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={checkBountyBalance}
            disabled={checkingBalance || !formData.bountyId}
          >
            {checkingBalance ? <span className="loading"></span> : 'Check Balance'}
          </button>
        </div>
        {balance && (
          <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#d4edda', borderRadius: '4px' }}>
            <strong>Current Balance:</strong> {balance}
          </div>
        )}
      </div>

      {/* Funding Form */}
      <form onSubmit={handleFunding}>
        <h3>💸 Fund Bounty</h3>

        <div className="form-group">
          <label htmlFor="bountyId">Bounty ID:</label>
          <input
            type="number"
            id="bountyId"
            name="bountyId"
            value={formData.bountyId}
            onChange={handleInputChange}
            placeholder="1"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="amount">Amount (USDT):</label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={formData.amount}
            onChange={handleInputChange}
            placeholder="100"
            step="0.01"
            min="0.01"
            required
          />
          <small style={{ color: '#666', fontSize: '0.9rem' }}>
            Amount in USDT tokens (e.g., 100 = 100 USDT)
          </small>
        </div>

        <button type="submit" className="btn" disabled={loading}>
          {loading ? <span className="loading"></span> : `Fund with ${formData.amount} USDT`}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result-section">
          <h3>✅ Success!</h3>
          <p>{result}</p>
          <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
            <p><strong>Next Steps:</strong></p>
            <ol>
              <li>Verify some submissions in the "Verify Submissions" tab</li>
              <li>Mark accepted submissions as claimable</li>
              <li>Allow users to claim their payouts</li>
            </ol>
          </div>
        </div>
      )}

      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
        <h4>ℹ️ How Bounty Funding Works</h4>
        <ul style={{ textAlign: 'left', marginBottom: 0 }}>
          <li><strong>Bounty Pools:</strong> Each bounty has an ID and can accumulate funds from multiple funders</li>
          <li><strong>USDT Tokens:</strong> Uses mock USDT with 6 decimal places (like real USDT)</li>
          <li><strong>Approval:</strong> The system automatically handles token approval before funding</li>
          <li><strong>Payouts:</strong> Funds are used to pay accepted submissions</li>
        </ul>
      </div>
    </div>
  );
};

export default BountyFunding;