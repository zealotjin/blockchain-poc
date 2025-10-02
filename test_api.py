#!/usr/bin/env python3
"""
Test script for the FastAPI server
Demonstrates the complete submission workflow via API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_workflow():
    """Test the complete API workflow"""
    print("🚀 Testing Blockchain Submission API\n")

    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ API healthy - Network: {health_data.get('network')}")
            print(f"   Account: {health_data.get('account')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to API. Make sure the server is running.")
        return False

    # Test 2: Fund bounty first
    print("\n2. Funding bounty pool...")
    bounty_data = {
        "bounty_id": 1,
        "amount": 100000000  # 100 USDT (6 decimals)
    }

    response = requests.post(f"{BASE_URL}/bounties/fund", json=bounty_data)
    if response.status_code == 200:
        fund_result = response.json()
        print(f"   ✅ Bounty funded: {fund_result['amount_usdt']} USDT")
        print(f"   Transaction: {fund_result['transaction_hash']}")
    else:
        print(f"   ❌ Bounty funding failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

    # Test 3: Create submission
    print("\n3. Creating submission...")
    submission_data = {
        "content_hash": "QmX123abcdef456789",
        "uri": "ipfs://QmX123abcdef456789",
        "mime_type": "image/png"
    }

    response = requests.post(f"{BASE_URL}/submissions", json=submission_data)
    if response.status_code == 200:
        submission_result = response.json()
        submission_id = submission_result["submission_id"]
        print(f"   ✅ Submission created with ID: {submission_id}")
        print(f"   Submitter: {submission_result['submitter']}")
        print(f"   Content Hash: {submission_result['content_hash']}")
        print(f"   Transaction: {submission_result['transaction_hash']}")
    else:
        print(f"   ❌ Submission creation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

    # Test 4: Get submission details
    print(f"\n4. Retrieving submission {submission_id}...")
    response = requests.get(f"{BASE_URL}/submissions/{submission_id}")
    if response.status_code == 200:
        submission_details = response.json()
        print(f"   ✅ Retrieved submission details")
        print(f"   URI: {submission_details['uri']}")
        print(f"   MIME: {submission_details['mime_type']}")
        print(f"   Timestamp: {submission_details['timestamp']}")
    else:
        print(f"   ❌ Failed to retrieve submission: {response.status_code}")

    # Test 5: Verify submission (accept)
    print(f"\n5. Verifying submission {submission_id}...")
    verification_data = {
        "submission_id": submission_id,
        "accepted": True,
        "reason_code": 0
    }

    response = requests.post(f"{BASE_URL}/verifications", json=verification_data)
    if response.status_code == 200:
        verification_result = response.json()
        print(f"   ✅ Submission verified as ACCEPTED")
        print(f"   Verifier: {verification_result['verifier']}")
        print(f"   Transaction: {verification_result['transaction_hash']}")
    else:
        print(f"   ❌ Verification failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

    # Test 6: Get verification details
    print(f"\n6. Retrieving verification for submission {submission_id}...")
    response = requests.get(f"{BASE_URL}/verifications/{submission_id}")
    if response.status_code == 200:
        verification_details = response.json()
        print(f"   ✅ Retrieved verification details")
        print(f"   Accepted: {verification_details['accepted']}")
        print(f"   Reason Code: {verification_details['reason_code']}")
    else:
        print(f"   ❌ Failed to retrieve verification: {response.status_code}")

    # Test 7: Mark as claimable
    print(f"\n7. Marking submission {submission_id} as claimable...")
    claimable_data = {
        "submission_id": submission_id,
        "recipient": submission_result["submitter"],  # Same as submitter
        "amount": 50000000  # 50 USDT payout
    }

    response = requests.post(f"{BASE_URL}/payouts/mark-claimable", json=claimable_data)
    if response.status_code == 200:
        claimable_result = response.json()
        print(f"   ✅ Marked as claimable: {claimable_result['amount_usdt']} USDT")
        print(f"   Recipient: {claimable_result['recipient']}")
        print(f"   Transaction: {claimable_result['transaction_hash']}")
    else:
        print(f"   ❌ Mark claimable failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

    # Test 8: Claim payout
    print(f"\n8. Claiming payout for submission {submission_id}...")
    claim_data = {
        "submission_id": submission_id,
        "recipient": submission_result["submitter"]
    }

    response = requests.post(f"{BASE_URL}/payouts/claim", json=claim_data)
    if response.status_code == 200:
        claim_result = response.json()
        print(f"   ✅ Payout claimed: {claim_result['amount_usdt']} USDT")
        print(f"   Transaction: {claim_result['transaction_hash']}")
    else:
        print(f"   ❌ Claim payout failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

    # Test 9: Get final payout status
    print(f"\n9. Checking final payout status for submission {submission_id}...")
    response = requests.get(f"{BASE_URL}/payouts/{submission_id}")
    if response.status_code == 200:
        payout_details = response.json()
        print(f"   ✅ Final payout status")
        print(f"   Amount: {payout_details['amount_usdt']} USDT")
        print(f"   Claimed: {payout_details['claimed']}")
    else:
        print(f"   ❌ Failed to retrieve payout status: {response.status_code}")

    print("\n🎉 API WORKFLOW COMPLETE! 🎉")
    print("✅ Submission → Verification → Funding → Claiming all worked via API!")
    return True

def test_error_cases():
    """Test error handling"""
    print("\n🧪 Testing error cases...")

    # Test invalid submission ID
    print("\n1. Testing invalid submission ID...")
    response = requests.get(f"{BASE_URL}/submissions/999999")
    if response.status_code == 404:
        print("   ✅ Correctly returned 404 for invalid submission")
    else:
        print(f"   ❌ Expected 404, got {response.status_code}")

    # Test invalid verification
    print("\n2. Testing invalid verification...")
    invalid_verification = {
        "submission_id": 999999,
        "accepted": True,
        "reason_code": 0
    }
    response = requests.post(f"{BASE_URL}/verifications", json=invalid_verification)
    if response.status_code == 500:
        print("   ✅ Correctly returned error for invalid verification")
    else:
        print(f"   ❌ Expected error, got {response.status_code}")

def main():
    """Main test function"""
    print("=" * 60)
    print("  BLOCKCHAIN SUBMISSION API TEST SUITE")
    print("=" * 60)

    # Run main workflow test
    success = test_api_workflow()

    if success:
        # Run error case tests
        test_error_cases()

        print("\n" + "=" * 60)
        print("  ALL TESTS COMPLETED")
        print("=" * 60)
        print("\n📖 API Documentation available at: http://localhost:8000/docs")
        print("🔧 Interactive API testing at: http://localhost:8000/redoc")
    else:
        print("\n❌ Workflow test failed. Check the error messages above.")

if __name__ == "__main__":
    main()