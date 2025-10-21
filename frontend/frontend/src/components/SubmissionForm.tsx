import React, { useState } from 'react';
import { apiClient, SubmissionResponse } from '../services/api';

const SubmissionForm: React.FC = () => {
  const [formData, setFormData] = useState({
    contentHash: '',
    uri: '',
    mimeType: 'image/png'
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SubmissionResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await apiClient.submitSubmission(
        formData.contentHash,
        formData.uri,
        formData.mimeType
      );
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit');
    } finally {
      setLoading(false);
    }
  };

  const generateSampleData = () => {
    const timestamp = Date.now();
    setFormData({
      contentHash: `QmX${timestamp}abcdef...`,
      uri: `ipfs://QmX${timestamp}abcdef...`,
      mimeType: 'image/png'
    });
  };

  return (
    <div>
      <h2>Submit Content</h2>
      <p>Register a new submission on the blockchain with content hash and metadata.</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="contentHash">Content Hash:</label>
          <input
            type="text"
            id="contentHash"
            name="contentHash"
            value={formData.contentHash}
            onChange={handleInputChange}
            placeholder="QmX123abcdef... (IPFS hash or other content hash)"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="uri">URI:</label>
          <input
            type="text"
            id="uri"
            name="uri"
            value={formData.uri}
            onChange={handleInputChange}
            placeholder="ipfs://QmX123abcdef... or https://example.com/content"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="mimeType">MIME Type:</label>
          <select
            id="mimeType"
            name="mimeType"
            value={formData.mimeType}
            onChange={handleInputChange}
            required
          >
            <option value="image/png">image/png</option>
            <option value="image/jpeg">image/jpeg</option>
            <option value="image/gif">image/gif</option>
            <option value="video/mp4">video/mp4</option>
            <option value="application/pdf">application/pdf</option>
            <option value="text/plain">text/plain</option>
            <option value="application/json">application/json</option>
          </select>
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
          <button type="submit" className="btn" disabled={loading}>
            {loading ? <span className="loading"></span> : 'Submit Content'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={generateSampleData}>
            Generate Sample Data
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result-section">
          <h3>✅ Submission Successful!</h3>
          <p><strong>Submission ID:</strong> {result.submission_id}</p>
          <p><strong>Transaction Hash:</strong>
            <code style={{ wordBreak: 'break-all', marginLeft: '0.5rem' }}>
              {result.transaction_hash}
            </code>
          </p>
          <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
            <p><strong>Next Steps:</strong></p>
            <ol>
              <li>Go to the "Verify Submissions" tab to accept/reject this submission</li>
              <li>If accepted, go to "Fund Bounties" to add funds to the bounty pool</li>
              <li>Mark the submission as claimable and claim the payout</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
};

export default SubmissionForm;