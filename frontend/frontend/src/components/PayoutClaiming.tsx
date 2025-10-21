import React, { useState } from 'react';
import { apiClient, Claimable } from '../services/api';

const PayoutClaiming: React.FC = () => {
  const [submissionId, setSubmissionId] = useState<string>('');
  const [recipient, setRecipient] = useState<string>('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'); // Default Hardhat account
  const [amount, setAmount] = useState<string>('50');
  const [claimable, setClaimable] = useState<Claimable | null>(null);
  const [loading, setLoading] = useState(false);
  const [marking, setMarking] = useState(false);
  const [claiming, setClaiming] = useState(false);
  const [error, setError] = useState<string>('');
  const [result, setResult] = useState<string>('');

  const fetchClaimable = async () => {
    if (!submissionId) return;

    setLoading(true);
    setError('');
    setClaimable(null);

    try {
      const claimableData = await apiClient.getClaimable(parseInt(submissionId));
      setClaimable(claimableData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch claimable data');
    } finally {
      setLoading(false);
    }
  };

  const markAsClaimable = async () => {
    if (!submissionId || !recipient || !amount) return;

    setMarking(true);
    setError('');
    setResult('');

    try {
      const amountInTokens = parseFloat(amount) * 1e6; // Convert to 6 decimal USDT
      const response = await apiClient.markClaimable(
        parseInt(submissionId),
        recipient,
        amountInTokens
      );
      setResult(`✅ Marked as claimable! Transaction: ${response.transaction_hash}`);

      // Refresh claimable data
      setTimeout(() => {
        fetchClaimable();
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to mark as claimable');
    } finally {
      setMarking(false);
    }
  };

  const claimPayout = async () => {
    if (!submissionId || !recipient) return;

    setClaiming(true);
    setError('');
    setResult('');

    try {
      const response = await apiClient.claimPayout(
        parseInt(submissionId),
        recipient
      );
      setResult(`🎉 Payout claimed successfully! Transaction: ${response.transaction_hash}`);

      // Refresh claimable data
      setTimeout(() => {
        fetchClaimable();
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to claim payout');
    } finally {
      setClaiming(false);
    }
  };

  const useDefaultAccount = () => {
    setRecipient('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266');
  };

  return (
    <div>
      <h2>Claim Payouts</h2>
      <p>Mark verified submissions as claimable and allow recipients to claim their USDT rewards.</p>

      <div className="form-group">
        <label htmlFor="submissionId">Submission ID:</label>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="number"
            id="submissionId"
            value={submissionId}
            onChange={(e) => setSubmissionId(e.target.value)}
            placeholder="Enter submission ID (e.g., 1)"
            style={{ flex: 1 }}
          />
          <button
            type="button"
            className="btn btn-secondary"
            onClick={fetchClaimable}
            disabled={loading || !submissionId}
          >
            {loading ? <span className="loading"></span> : 'Check Status'}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {claimable ? (
        <div className="result-section">
          <h3>💰 Claimable Payout Details</h3>
          <div className="two-column">
            <div>
              <p><strong>Recipient:</strong> <code>{claimable.recipient}</code></p>
              <p><strong>Amount:</strong> {claimable.amount / 1e6} USDT</p>
            </div>
            <div>
              <p><strong>Status:</strong> {claimable.claimed ? '✅ Already Claimed' : '⏳ Available to Claim'}</p>
            </div>
          </div>

          {!claimable.claimed && (
            <div style={{ marginTop: '1rem' }}>
              <button
                className="btn btn-success"
                onClick={claimPayout}
                disabled={claiming}
                style={{ marginRight: '1rem' }}
              >
                {claiming ? <span className="loading"></span> : `🎉 Claim ${claimable.amount / 1e6} USDT`}
              </button>
            </div>
          )}
        </div>
      ) : (
        submissionId && !loading && (
          <div>
            <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#fff3cd', borderRadius: '4px' }}>
              <p>⚠️ <strong>No claimable payout found.</strong> This submission might not be marked as claimable yet.</p>
            </div>

            {/* Mark as Claimable Section */}
            <div style={{ marginTop: '2rem' }}>
              <h3>📋 Mark Submission as Claimable</h3>
              <p>If this submission was verified and accepted, you can mark it as claimable for payout.</p>

              <div className="form-group">
                <label htmlFor="recipient">Recipient Address:</label>
                <div style={{ display: 'flex', gap: '1rem' }}>
                  <input
                    type="text"
                    id="recipient"
                    value={recipient}
                    onChange={(e) => setRecipient(e.target.value)}
                    placeholder="0x..."
                    style={{ flex: 1 }}
                  />
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={useDefaultAccount}
                  >
                    Use Default
                  </button>
                </div>
                <small style={{ color: '#666', fontSize: '0.9rem' }}>
                  Ethereum address that will receive the payout
                </small>
              </div>

              <div className="form-group">
                <label htmlFor="amount">Payout Amount (USDT):</label>
                <input
                  type="number"
                  id="amount"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  placeholder="50"
                  step="0.01"
                  min="0.01"
                />
                <small style={{ color: '#666', fontSize: '0.9rem' }}>
                  Amount in USDT tokens to pay out for this submission
                </small>
              </div>

              <button
                className="btn"
                onClick={markAsClaimable}
                disabled={marking || !recipient || !amount}
              >
                {marking ? <span className="loading"></span> : `Mark Claimable for ${amount} USDT`}
              </button>
            </div>
          </div>
        )
      )}

      {result && (
        <div className="success-message">
          {result}
        </div>
      )}

      {!submissionId && (
        <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
          <p>💡 <strong>Workflow:</strong></p>
          <ol style={{ textAlign: 'left', marginBottom: 0 }}>
            <li>Submit content and get a submission ID</li>
            <li>Verify the submission as accepted</li>
            <li>Fund the bounty pool with USDT</li>
            <li>Mark the submission as claimable (admin action)</li>
            <li>Claim the payout (user action)</li>
          </ol>
        </div>
      )}

      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
        <h4>ℹ️ Payout Process</h4>
        <ul style={{ textAlign: 'left', marginBottom: 0 }}>
          <li><strong>Mark Claimable:</strong> Admin/verifier action to approve payouts</li>
          <li><strong>Claim:</strong> User action to receive USDT tokens</li>
          <li><strong>Security:</strong> Only marked submissions can be claimed, only once</li>
          <li><strong>Gas Fees:</strong> Claiming requires paying transaction gas fees</li>
        </ul>
      </div>
    </div>
  );
};

export default PayoutClaiming;