Got it 👍 — let’s strip away all code and keep only the functional + technical requirements for the blockchain-only POC. This will give you a checklist of what you need to deploy and test without backend/frontend.

⸻

📌 Blockchain-only POC: Functional & Technical Requirements

🎯 Objectives
	•	Be able to deploy simple contracts to a testnet or local node.
	•	Test the core flows:
	1.	Register a user(user → chain).
	2.	Verify/accept/reject a submission (verifier → chain).
	3.	Fund bounty pools in stablecoin (brand → chain).
	4.	Claim payout in stablecoin (user → chain).
	•	Keep everything minimal: minimal python scripts to test out setup of environment and functionalities.

⸻

🧩 Smart Contract Components

1. Submission Registry
	•	Purpose: Track submissions on-chain with minimal data.
	•	Functions:
	•	registerSubmission(contentHash, uri, mime) → record submission & emit event.
	•	getSubmission(id) → read details.
	•	Events: SubmissionRegistered(id, submitter, contentHash, uri, mime, timestamp).
	•	Notes: No file storage, just hash/URI references.

⸻

2. Verification Manager
	•	Purpose: Allow designated verifiers to accept/reject submissions.
	•	Functions:
	•	setVerification(submissionId, accepted, reasonCode) → record decision.
	•	getVerification(submissionId) → read decision.
	•	Roles:
	•	VERIFIER_ROLE (brands/reviewers).
	•	ADMIN_ROLE (setup roles).
	•	Events: SubmissionVerified(submissionId, verifier, accepted, reasonCode, timestamp).
	•	Notes: Could later integrate with EAS (Ethereum Attestation Service).

⸻

3. Bounty Pool
	•	Purpose: Manage bounty funds and payouts in stablecoin.
	•	Functions:
	•	fundBounty(bountyId, amount) → brand funds pool (requires ERC-20 approve).
	•	markClaimable(submissionId, recipient, amount) → mark accepted submissions as claimable.
	•	claim(submissionId, recipient) → user claims payout.
	•	Events:
	•	BountyFunded(bountyId, amount, funder)
	•	ClaimableSet(submissionId, recipient, amount)
	•	PayoutClaimed(submissionId, recipient, amount)
	•	Notes: Owner/admin sets claimable amounts for simplicity in POC.

⸻

⚙️ Technical Requirements

Environment
	•	Blockchain: EVM-compatible (Ethereum testnets, Base Sepolia, Optimism Sepolia, Polygon Amoy, Arbitrum Sepolia).
	•	Contracts: Solidity (≥0.8.18), OpenZeppelin libraries for AccessControl, Ownable, ERC-20 interface.
	•	Frameworks: Hardhat (JS/TS) or Brownie (Python) for compiling, deploying, and testing.
	•	Token: Testnet stablecoin (e.g. USDC/USDT faucet address) OR a mock ERC-20 for local testing.

Config & Setup
	•	.env variables: RPC URL, private key, stablecoin address.
	•	Deployment script that outputs all contract addresses (for later reference).
	•	Optional local blockchain for dry-run testing (Hardhat node, Ganache, or Anvil).

Interaction
	•	Ability to call contract functions via:
	•	Hardhat CLI / scripts (JS/TS).
	•	Web3.py (Python scripting).
	•	Ability to listen for events (Submissions, Verifications, Payouts).

Security / Ops (POC level)
	•	Contract ownership with a single deployer account (later → multisig Safe).
	•	Use AccessControl for verifier role.
	•	Minimal checks:
	•	Prevent double claims.
	•	Ensure fundBounty uses transferFrom with prior approval.
	•	Keep contracts upgrade-minimal (plain deploy, no proxy for POC).

⸻

✅ POC Test Flow (Happy Path)
	1.	Brand funds bounty
	•	Approves stablecoin.
	•	Calls fundBounty(bountyId, amount).
	2.	User submits
	•	Uploads file off-chain (manual step for now).
	•	Computes content hash.
	•	Calls registerSubmission(contentHash, uri, mime).
	3.	Verifier reviews
	•	Calls setVerification(submissionId, accepted=true, reasonCode=0).
	•	Admin marks payout via markClaimable(submissionId, recipient, amount).
	4.	User claims payout
	•	Calls claim(submissionId, wallet).
	•	Stablecoin transferred to user.

⸻

📊 Deliverables for POC
	•	Deployed contracts on a testnet with addresses.
	•	Checklist of calls: Submission → Verification → Fund → Claim.
	•	Event logs:
	•	SubmissionRegistered
	•	SubmissionVerified
	•	BountyFunded
	•	ClaimableSet
	•	PayoutClaimed
	•	Manual test run:
	•	Register at least one submission.
	•	Verify/accept it.
	•	Fund bounty pool and claim payout.

⸻

👉 This setup lets you learn the environment quickly: deploy, call, and track events — without backend or frontend.

Would you like me to make a step-by-step “Hello World” test script plan (e.g., exact sequence of contract calls with example parameters) so you can walk through one submission-to-payout cycle on a local node?