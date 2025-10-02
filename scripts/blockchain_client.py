"""
Web3.py client for interacting with deployed contracts
This will be used by FastAPI backend for blockchain operations
"""

import json
from web3 import Web3
from eth_account import Account
from config.blockchain_config import BlockchainConfig

class BlockchainClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(BlockchainConfig.RPC_URL))
        self.account = Account.from_key(BlockchainConfig.PRIVATE_KEY)
        self.contracts = {}
        self._load_contracts()

    def _load_contracts(self):
        """Load contract ABIs and addresses"""
        # Load deployment addresses
        with open("deployments/addresses.json", "r") as f:
            deployment = json.load(f)

        # Load contract ABIs
        contract_abis = {}
        for contract_name in ["SubmissionRegistry", "VerificationManager", "BountyPool", "MockUSDT"]:
            artifact_path = f"artifacts/contracts/{contract_name}.sol/{contract_name}.json"
            with open(artifact_path, "r") as f:
                artifact = json.load(f)
                contract_abis[contract_name] = artifact["abi"]

        # Initialize contract instances
        self.contracts = {
            "submission_registry": self.w3.eth.contract(
                address=deployment["submissionRegistry"],
                abi=contract_abis["SubmissionRegistry"]
            ),
            "verification_manager": self.w3.eth.contract(
                address=deployment["verificationManager"],
                abi=contract_abis["VerificationManager"]
            ),
            "bounty_pool": self.w3.eth.contract(
                address=deployment["bountyPool"],
                abi=contract_abis["BountyPool"]
            ),
            "mock_usdt": self.w3.eth.contract(
                address=deployment["mockUSDT"],
                abi=contract_abis["MockUSDT"]
            )
        }

    def register_submission(self, content_hash: str, uri: str, mime: str):
        """Register a new submission"""
        contract = self.contracts["submission_registry"]

        transaction = contract.functions.registerSubmission(
            content_hash, uri, mime
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        # Get submission ID from logs
        submission_id = receipt.logs[0]['topics'][1].hex()
        return int(submission_id, 16), receipt

    def verify_submission(self, submission_id: int, accepted: bool, reason_code: int = 0):
        """Verify a submission (accept/reject)"""
        contract = self.contracts["verification_manager"]

        transaction = contract.functions.setVerification(
            submission_id, accepted, reason_code
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def fund_bounty(self, bounty_id: int, amount: int):
        """Fund a bounty pool"""
        # First approve the amount
        mock_usdt = self.contracts["mock_usdt"]
        bounty_pool = self.contracts["bounty_pool"]

        # Approve transaction
        approve_tx = mock_usdt.functions.approve(
            bounty_pool.address, amount
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_approve = self.w3.eth.account.sign_transaction(approve_tx, self.account.key)
        approve_hash = self.w3.eth.send_raw_transaction(signed_approve.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(approve_hash)

        # Fund bounty transaction
        fund_tx = bounty_pool.functions.fundBounty(
            bounty_id, amount
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_fund = self.w3.eth.account.sign_transaction(fund_tx, self.account.key)
        fund_hash = self.w3.eth.send_raw_transaction(signed_fund.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(fund_hash)
        return receipt

    def mark_claimable(self, submission_id: int, recipient: str, amount: int):
        """Mark submission as claimable for payout"""
        contract = self.contracts["bounty_pool"]

        transaction = contract.functions.markClaimable(
            submission_id, recipient, amount
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def claim_payout(self, submission_id: int, recipient: str):
        """Claim payout for accepted submission"""
        contract = self.contracts["bounty_pool"]

        transaction = contract.functions.claim(
            submission_id, recipient
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def get_submission(self, submission_id: int):
        """Get submission details"""
        contract = self.contracts["submission_registry"]
        return contract.functions.getSubmission(submission_id).call()

    def get_verification(self, submission_id: int):
        """Get verification details"""
        contract = self.contracts["verification_manager"]
        return contract.functions.getVerification(submission_id).call()

    def get_claimable(self, submission_id: int):
        """Get claimable payout details"""
        contract = self.contracts["bounty_pool"]
        return contract.functions.getClaimable(submission_id).call()