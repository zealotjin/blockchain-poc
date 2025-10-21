import React, { useState } from 'react';
import { apiClient, Submission, Verification } from '../services/api';

const VerificationInterface: React.FC = () => {
  const [submissionId, setSubmissionId] = useState<string>('');
  const [submission, setSubmission] = useState<Submission | null>(null);
  const [verification, setVerification] = useState<Verification | null>(null);
  const [loading, setLoading] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [error, setError] = useState<string>('');
  const [verificationResult, setVerificationResult] = useState<string>('');

  const fetchSubmission = async () => {
    if (!submissionId) return;

    setLoading(true);
    setError('');
    setSubmission(null);
    setVerification(null);

    try {
      const submissionData = await apiClient.getSubmission(parseInt(submissionId));
      setSubmission(submissionData);

      try {
        const verificationData = await apiClient.getVerification(parseInt(submissionId));
        setVerification(verificationData);
      } catch {
        // Verification might not exist yet, that's okay
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch submission');
    } finally {
      setLoading(false);
    }
  };

  const handleVerification = async (accepted: boolean, reasonCode: number = 0) => {
    if (!submissionId) return;

    setVerifying(true);
    setError('');
    setVerificationResult('');

    try {
      const response = await apiClient.verifySubmission(
        parseInt(submissionId),
        accepted,
        reasonCode
      );
      setVerificationResult(`Verification ${accepted ? 'accepted' : 'rejected'}! Tx: ${response.transaction_hash}`);

      // Refresh verification data
      setTimeout(() => {
        fetchSubmission();
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to verify submission');
    } finally {
      setVerifying(false);
    }
  };

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  return (
    <div>
      <h2>Verify Submissions</h2>
      <p>Review and accept/reject submissions. Only verified submissions can receive payouts.</p>

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
            className="btn"
            onClick={fetchSubmission}
            disabled={loading || !submissionId}
          >
            {loading ? <span className="loading"></span> : 'Fetch Submission'}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {submission && (
        <div className="result-section">
          <h3>📄 Submission Details</h3>
          <div className="two-column">
            <div>
              <p><strong>Submitter:</strong> <code>{submission.submitter}</code></p>
              <p><strong>Content Hash:</strong> <code>{submission.content_hash}</code></p>
              <p><strong>URI:</strong> <code>{submission.uri}</code></p>
            </div>
            <div>
              <p><strong>MIME Type:</strong> {submission.mime_type}</p>
              <p><strong>Submitted:</strong> {formatTimestamp(submission.timestamp)}</p>
            </div>
          </div>

          {verification ? (
            <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: verification.accepted ? '#d4edda' : '#f8d7da', borderRadius: '4px' }}>
              <h4>✅ Already Verified</h4>
              <p><strong>Status:</strong> {verification.accepted ? '✅ ACCEPTED' : '❌ REJECTED'}</p>
              <p><strong>Verifier:</strong> <code>{verification.verifier}</code></p>
              <p><strong>Reason Code:</strong> {verification.reason_code}</p>
              <p><strong>Verified:</strong> {formatTimestamp(verification.timestamp)}</p>
            </div>
          ) : (
            <div style={{ marginTop: '1rem' }}>
              <h4>⏳ Pending Verification</h4>
              <p>This submission has not been verified yet. Choose an action:</p>

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                <button
                  className="btn btn-success"
                  onClick={() => handleVerification(true, 0)}
                  disabled={verifying}
                >
                  {verifying ? <span className="loading"></span> : '✅ Accept'}
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => handleVerification(false, 1)}
                  disabled={verifying}
                >
                  {verifying ? <span className="loading"></span> : '❌ Reject (Quality)'}
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => handleVerification(false, 2)}
                  disabled={verifying}
                >
                  {verifying ? <span className="loading"></span> : '❌ Reject (Policy)'}
                </button>
              </div>

              <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
                <p><strong>Reason Codes:</strong></p>
                <ul>
                  <li>0: Accepted</li>
                  <li>1: Rejected - Quality issues</li>
                  <li>2: Rejected - Policy violation</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {verificationResult && (
        <div className="success-message">
          {verificationResult}
        </div>
      )}

      {!submission && !loading && submissionId && (
        <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#fff3cd', borderRadius: '4px' }}>
          <p>💡 <strong>Tip:</strong> Submit some content first using the "Submit Content" tab, then come back here with the submission ID to verify it.</p>
        </div>
      )}
    </div>
  );
};

export default VerificationInterface;