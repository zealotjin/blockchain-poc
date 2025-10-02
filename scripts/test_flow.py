#!/usr/bin/env python3
"""
Complete test flow: Submission → Verification → Fund → Claim
Tests the happy path described in README.md
"""

import sys
import time
from blockchain_client import BlockchainClient

def test_complete_flow():
    """Test the complete submission-to-payout workflow"""
    print("=== Starting Complete Blockchain POC Test Flow ===\n")

    # Initialize blockchain client
    try:
        client = BlockchainClient()
        print("✅ Connected to blockchain")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return False

    # Test parameters
    content_hash = "QmX123abcdef..."
    uri = "ipfs://QmX123abcdef..."
    mime_type = "image/png"
    bounty_id = 1
    bounty_amount = 100 * 10**6  # 100 USDT (6 decimals)
    payout_amount = 50 * 10**6   # 50 USDT payout

    try:
        # Step 1: Fund bounty pool first
        print("1. Funding bounty pool...")
        # Get some test USDT from faucet
        usdt_contract = client.contracts["mock_usdt"]
        faucet_tx = usdt_contract.functions.faucet(1000 * 10**6).build_transaction({
            'from': client.account.address,
            'nonce': client.w3.eth.get_transaction_count(client.account.address),
            'gas': 100000,
            'gasPrice': client.w3.eth.gas_price
        })
        signed_faucet = client.w3.eth.account.sign_transaction(faucet_tx, client.account.key)
        faucet_hash = client.w3.eth.send_raw_transaction(signed_faucet.rawTransaction)
        client.w3.eth.wait_for_transaction_receipt(faucet_hash)
        print("   ✅ Got test USDT from faucet")

        fund_receipt = client.fund_bounty(bounty_id, bounty_amount)
        print(f"   ✅ Bounty funded: {bounty_amount/10**6} USDT")
        print(f"   Transaction: {fund_receipt.transactionHash.hex()}")

        # Step 2: Register submission
        print("\n2. Registering submission...")
        submission_id, submit_receipt = client.register_submission(content_hash, uri, mime_type)
        print(f"   ✅ Submission registered with ID: {submission_id}")
        print(f"   Content Hash: {content_hash}")
        print(f"   Transaction: {submit_receipt.transactionHash.hex()}")

        # Step 3: Verify/accept submission
        print("\n3. Verifying submission...")
        verify_receipt = client.verify_submission(submission_id, accepted=True, reason_code=0)
        print(f"   ✅ Submission {submission_id} verified as ACCEPTED")
        print(f"   Transaction: {verify_receipt.transactionHash.hex()}")

        # Step 4: Mark submission as claimable
        print("\n4. Marking submission as claimable...")
        mark_receipt = client.mark_claimable(submission_id, client.account.address, payout_amount)
        print(f"   ✅ Submission {submission_id} marked claimable")
        print(f"   Payout Amount: {payout_amount/10**6} USDT")
        print(f"   Transaction: {mark_receipt.transactionHash.hex()}")

        # Step 5: Claim payout
        print("\n5. Claiming payout...")
        claim_receipt = client.claim_payout(submission_id, client.account.address)
        print(f"   ✅ Payout claimed successfully!")
        print(f"   Transaction: {claim_receipt.transactionHash.hex()}")

        # Verification: Check final states
        print("\n=== Verification ===")
        submission = client.get_submission(submission_id)
        verification = client.get_verification(submission_id)
        claimable = client.get_claimable(submission_id)

        print(f"Submission Details:")
        print(f"  - Submitter: {submission[0]}")
        print(f"  - Content Hash: {submission[1]}")
        print(f"  - URI: {submission[2]}")
        print(f"  - MIME: {submission[3]}")
        print(f"  - Timestamp: {submission[4]}")

        print(f"\nVerification Details:")
        print(f"  - Verifier: {verification[0]}")
        print(f"  - Accepted: {verification[1]}")
        print(f"  - Reason Code: {verification[2]}")
        print(f"  - Timestamp: {verification[3]}")

        print(f"\nClaimable Details:")
        print(f"  - Recipient: {claimable[0]}")
        print(f"  - Amount: {claimable[1]/10**6} USDT")
        print(f"  - Claimed: {claimable[2]}")

        print("\n🎉 COMPLETE FLOW SUCCESSFUL! 🎉")
        print("✅ Submission → Verification → Funding → Claiming all worked!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    sys.exit(0 if success else 1)