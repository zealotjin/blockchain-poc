const API_BASE_URL = 'http://localhost:8000';

export interface Submission {
  submitter: string;
  content_hash: string;
  uri: string;
  mime_type: string;
  timestamp: number;
}

export interface Verification {
  verifier: string;
  accepted: boolean;
  reason_code: number;
  timestamp: number;
}

export interface Claimable {
  recipient: string;
  amount: number;
  claimed: boolean;
}

export interface SubmissionResponse {
  submission_id: number;
  transaction_hash: string;
  submitter: string;
  content_hash: string;
  uri: string;
  mime_type: string;
  timestamp: number;
}

export interface TransactionResponse {
  transaction_hash: string;
}

export interface BountyBalanceResponse {
  balance: number;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API request failed: ${response.status} ${errorText}`);
    }

    return response.json();
  }

  // Submit new submission
  async submitSubmission(
    contentHash: string,
    uri: string,
    mimeType: string
  ): Promise<SubmissionResponse> {
    return this.request<SubmissionResponse>('/submissions', {
      method: 'POST',
      body: JSON.stringify({
        content_hash: contentHash,
        uri: uri,
        mime_type: mimeType,
      }),
    });
  }

  // Verify submission
  async verifySubmission(
    submissionId: number,
    accepted: boolean,
    reasonCode: number = 0
  ): Promise<TransactionResponse> {
    return this.request<TransactionResponse>('/verifications', {
      method: 'POST',
      body: JSON.stringify({
        submission_id: submissionId,
        accepted: accepted,
        reason_code: reasonCode,
      }),
    });
  }

  // Fund bounty
  async fundBounty(
    bountyId: number,
    amount: number
  ): Promise<TransactionResponse> {
    return this.request<TransactionResponse>('/bounties/fund', {
      method: 'POST',
      body: JSON.stringify({
        bounty_id: bountyId,
        amount: amount,
      }),
    });
  }

  // Mark submission claimable
  async markClaimable(
    submissionId: number,
    recipient: string,
    amount: number
  ): Promise<TransactionResponse> {
    return this.request<TransactionResponse>('/payouts/mark-claimable', {
      method: 'POST',
      body: JSON.stringify({
        submission_id: submissionId,
        recipient: recipient,
        amount: amount,
      }),
    });
  }

  // Claim payout
  async claimPayout(
    submissionId: number,
    recipient: string
  ): Promise<TransactionResponse> {
    return this.request<TransactionResponse>('/payouts/claim', {
      method: 'POST',
      body: JSON.stringify({
        submission_id: submissionId,
        recipient: recipient,
      }),
    });
  }

  // Get submission details
  async getSubmission(submissionId: number): Promise<Submission> {
    return this.request<Submission>(`/submissions/${submissionId}`);
  }

  // Get verification details
  async getVerification(submissionId: number): Promise<Verification> {
    return this.request<Verification>(`/verifications/${submissionId}`);
  }

  // Get claimable details
  async getClaimable(submissionId: number): Promise<Claimable> {
    return this.request<Claimable>(`/payouts/${submissionId}`);
  }

  // Get bounty balance
  async getBountyBalance(bountyId: number): Promise<BountyBalanceResponse> {
    return this.request<BountyBalanceResponse>(`/bounty/${bountyId}/balance`);
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>('/health');
  }
}

export const apiClient = new ApiClient();