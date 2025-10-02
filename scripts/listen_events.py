#!/usr/bin/env python3
"""
Event listener for monitoring blockchain events
Useful for debugging and monitoring the POC
"""

import time
from blockchain_client import BlockchainClient

def listen_to_events():
    """Listen to all contract events"""
    print("🎧 Starting event listener...")

    client = BlockchainClient()

    # Create event filters
    submission_filter = client.contracts["submission_registry"].events.SubmissionRegistered.create_filter(fromBlock="latest")
    verification_filter = client.contracts["verification_manager"].events.SubmissionVerified.create_filter(fromBlock="latest")
    bounty_funded_filter = client.contracts["bounty_pool"].events.BountyFunded.create_filter(fromBlock="latest")
    claimable_filter = client.contracts["bounty_pool"].events.ClaimableSet.create_filter(fromBlock="latest")
    payout_filter = client.contracts["bounty_pool"].events.PayoutClaimed.create_filter(fromBlock="latest")

    print("Listening for events... (Press Ctrl+C to stop)")

    try:
        while True:
            # Check for new submission events
            for event in submission_filter.get_new_entries():
                print(f"\n📝 NEW SUBMISSION:")
                print(f"  ID: {event['args']['id']}")
                print(f"  Submitter: {event['args']['submitter']}")
                print(f"  Content Hash: {event['args']['contentHash']}")
                print(f"  URI: {event['args']['uri']}")
                print(f"  MIME: {event['args']['mime']}")
                print(f"  Block: {event['blockNumber']}")

            # Check for verification events
            for event in verification_filter.get_new_entries():
                status = "✅ ACCEPTED" if event['args']['accepted'] else "❌ REJECTED"
                print(f"\n🔍 SUBMISSION VERIFIED:")
                print(f"  Submission ID: {event['args']['submissionId']}")
                print(f"  Status: {status}")
                print(f"  Verifier: {event['args']['verifier']}")
                print(f"  Reason Code: {event['args']['reasonCode']}")
                print(f"  Block: {event['blockNumber']}")

            # Check for bounty funding events
            for event in bounty_funded_filter.get_new_entries():
                print(f"\n💰 BOUNTY FUNDED:")
                print(f"  Bounty ID: {event['args']['bountyId']}")
                print(f"  Amount: {event['args']['amount'] / 10**6} USDT")
                print(f"  Funder: {event['args']['funder']}")
                print(f"  Block: {event['blockNumber']}")

            # Check for claimable events
            for event in claimable_filter.get_new_entries():
                print(f"\n🎯 CLAIMABLE SET:")
                print(f"  Submission ID: {event['args']['submissionId']}")
                print(f"  Recipient: {event['args']['recipient']}")
                print(f"  Amount: {event['args']['amount'] / 10**6} USDT")
                print(f"  Block: {event['blockNumber']}")

            # Check for payout events
            for event in payout_filter.get_new_entries():
                print(f"\n💸 PAYOUT CLAIMED:")
                print(f"  Submission ID: {event['args']['submissionId']}")
                print(f"  Recipient: {event['args']['recipient']}")
                print(f"  Amount: {event['args']['amount'] / 10**6} USDT")
                print(f"  Block: {event['blockNumber']}")

            time.sleep(2)  # Poll every 2 seconds

    except KeyboardInterrupt:
        print("\n👋 Event listener stopped")

if __name__ == "__main__":
    listen_to_events()