#!/usr/bin/env python3
"""
FastAPI server for blockchain submission POC
Integrates with deployed smart contracts via blockchain_client.py
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import sys

# Add scripts directory to path to import blockchain_client
sys.path.append('scripts')

try:
    from blockchain_client import BlockchainClient
    from config.blockchain_config import BlockchainConfig
except ImportError as e:
    print(f"Error importing blockchain modules: {e}")
    print("Make sure contracts are deployed and deployments/addresses.json exists")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Blockchain Submission POC API",
    description="API for managing submissions, verifications, and payouts on blockchain",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize blockchain client
try:
    blockchain_client = BlockchainClient()
    print("✅ Blockchain client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize blockchain client: {e}")
    blockchain_client = None

# Pydantic models for request/response
class SubmissionCreate(BaseModel):
    content_hash: str
    uri: str
    mime_type: str

class SubmissionResponse(BaseModel):
    submission_id: int
    transaction_hash: str
    submitter: str
    content_hash: str
    uri: str
    mime_type: str
    timestamp: int

class VerificationCreate(BaseModel):
    submission_id: int
    accepted: bool
    reason_code: int = 0

class VerificationResponse(BaseModel):
    submission_id: int
    transaction_hash: str
    verifier: str
    accepted: bool
    reason_code: int
    timestamp: int

class BountyFund(BaseModel):
    bounty_id: int
    amount: int  # Amount in token units (e.g., 100 * 10^6 for 100 USDT)

class ClaimableCreate(BaseModel):
    submission_id: int
    recipient: str
    amount: int

class ClaimPayout(BaseModel):
    submission_id: int
    recipient: str

@app.get("/")
async def root():
    return {
        "message": "Blockchain Submission POC API",
        "status": "running",
        "blockchain_connected": blockchain_client is not None
    }

@app.get("/health")
async def health_check():
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        # Test blockchain connection
        is_connected = blockchain_client.w3.is_connected()
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "blockchain_connected": is_connected,
            "network": BlockchainConfig.NETWORK,
            "account": blockchain_client.account.address
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Blockchain connection error: {str(e)}"
        )

@app.post("/submissions", response_model=SubmissionResponse)
async def create_submission(submission: SubmissionCreate):
    """Register a new submission on the blockchain"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        # Register submission on blockchain
        submission_id, receipt = blockchain_client.register_submission(
            submission.content_hash,
            submission.uri,
            submission.mime_type
        )

        # Get submission details for response
        submission_data = blockchain_client.get_submission(submission_id)

        return SubmissionResponse(
            submission_id=submission_id,
            transaction_hash=receipt.transactionHash.hex(),
            submitter=submission_data[0],
            content_hash=submission_data[1],
            uri=submission_data[2],
            mime_type=submission_data[3],
            timestamp=submission_data[4]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create submission: {str(e)}"
        )

@app.get("/submissions/{submission_id}")
async def get_submission(submission_id: int):
    """Get submission details by ID"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        submission_data = blockchain_client.get_submission(submission_id)

        return {
            "submission_id": submission_id,
            "submitter": submission_data[0],
            "content_hash": submission_data[1],
            "uri": submission_data[2],
            "mime_type": submission_data[3],
            "timestamp": submission_data[4]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission not found: {str(e)}"
        )

@app.post("/verifications", response_model=VerificationResponse)
async def create_verification(verification: VerificationCreate):
    """Verify a submission (accept/reject)"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        # Verify submission on blockchain
        receipt = blockchain_client.verify_submission(
            verification.submission_id,
            verification.accepted,
            verification.reason_code
        )

        # Get verification details for response
        verification_data = blockchain_client.get_verification(verification.submission_id)

        return VerificationResponse(
            submission_id=verification.submission_id,
            transaction_hash=receipt.transactionHash.hex(),
            verifier=verification_data[0],
            accepted=verification_data[1],
            reason_code=verification_data[2],
            timestamp=verification_data[3]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create verification: {str(e)}"
        )

@app.get("/verifications/{submission_id}")
async def get_verification(submission_id: int):
    """Get verification details for a submission"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        verification_data = blockchain_client.get_verification(submission_id)

        return {
            "submission_id": submission_id,
            "verifier": verification_data[0],
            "accepted": verification_data[1],
            "reason_code": verification_data[2],
            "timestamp": verification_data[3]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Verification not found: {str(e)}"
        )

@app.post("/bounties/fund")
async def fund_bounty(bounty_fund: BountyFund):
    """Fund a bounty pool"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        receipt = blockchain_client.fund_bounty(
            bounty_fund.bounty_id,
            bounty_fund.amount
        )

        return {
            "bounty_id": bounty_fund.bounty_id,
            "amount": bounty_fund.amount,
            "amount_usdt": bounty_fund.amount / 10**6,
            "transaction_hash": receipt.transactionHash.hex(),
            "status": "funded"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fund bounty: {str(e)}"
        )

@app.post("/payouts/mark-claimable")
async def mark_claimable(claimable: ClaimableCreate):
    """Mark a submission as claimable for payout"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        receipt = blockchain_client.mark_claimable(
            claimable.submission_id,
            claimable.recipient,
            claimable.amount
        )

        return {
            "submission_id": claimable.submission_id,
            "recipient": claimable.recipient,
            "amount": claimable.amount,
            "amount_usdt": claimable.amount / 10**6,
            "transaction_hash": receipt.transactionHash.hex(),
            "status": "claimable"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark claimable: {str(e)}"
        )

@app.post("/payouts/claim")
async def claim_payout(claim: ClaimPayout):
    """Claim payout for a submission"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        receipt = blockchain_client.claim_payout(
            claim.submission_id,
            claim.recipient
        )

        # Get claimable details
        claimable_data = blockchain_client.get_claimable(claim.submission_id)

        return {
            "submission_id": claim.submission_id,
            "recipient": claim.recipient,
            "amount": claimable_data[1],
            "amount_usdt": claimable_data[1] / 10**6,
            "transaction_hash": receipt.transactionHash.hex(),
            "status": "claimed"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to claim payout: {str(e)}"
        )

@app.get("/payouts/{submission_id}")
async def get_claimable(submission_id: int):
    """Get claimable payout details for a submission"""
    if not blockchain_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain client not available"
        )

    try:
        claimable_data = blockchain_client.get_claimable(submission_id)

        return {
            "submission_id": submission_id,
            "recipient": claimable_data[0],
            "amount": claimable_data[1],
            "amount_usdt": claimable_data[1] / 10**6,
            "claimed": claimable_data[2]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claimable payout not found: {str(e)}"
        )

if __name__ == "__main__":
    # Run server
    uvicorn.run(
        "main:app",
        host=BlockchainConfig.API_HOST,
        port=BlockchainConfig.API_PORT,
        reload=BlockchainConfig.DEBUG
    )