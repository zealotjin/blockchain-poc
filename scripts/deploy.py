#!/usr/bin/env python3
"""
Python deployment script using Web3.py
Alternative to Hardhat deploy script for Python-first workflows
"""

import json
import os
from web3 import Web3
from eth_account import Account
from config.blockchain_config import BlockchainConfig
import sys

def compile_contracts():
    """Compile contracts using Hardhat and return ABI/bytecode"""
    os.system("npx hardhat compile")

    artifacts = {}
    contract_names = ["SubmissionRegistry", "VerificationManager", "BountyPool", "MockUSDC"]

    for name in contract_names:
        artifact_path = f"artifacts/contracts/{name}.sol/{name}.json"
        if os.path.exists(artifact_path):
            with open(artifact_path, 'r') as f:
                artifact = json.load(f)
                artifacts[name] = {
                    "abi": artifact["abi"],
                    "bytecode": artifact["bytecode"]
                }

    return artifacts

def deploy_contract(w3, account, contract_name, artifacts, constructor_args=None):
    """Deploy a single contract"""
    print(f"Deploying {contract_name}...")

    contract = w3.eth.contract(
        abi=artifacts[contract_name]["abi"],
        bytecode=artifacts[contract_name]["bytecode"]
    )

    # Build transaction
    if constructor_args:
        transaction = contract.constructor(*constructor_args).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 3000000,
            'gasPrice': w3.eth.gas_price
        })
    else:
        transaction = contract.constructor().build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 3000000,
            'gasPrice': w3.eth.gas_price
        })

    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, account.private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # Wait for transaction receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status == 1:
        print(f"{contract_name} deployed to: {receipt.contractAddress}")
        return receipt.contractAddress
    else:
        raise Exception(f"Failed to deploy {contract_name}")

def main():
    # Validate configuration
    try:
        BlockchainConfig.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    # Connect to blockchain
    w3 = Web3(Web3.HTTPProvider(BlockchainConfig.RPC_URL))
    if not w3.is_connected():
        print("Failed to connect to blockchain")
        sys.exit(1)

    print(f"Connected to {BlockchainConfig.NETWORK}")

    # Load account
    account = Account.from_key(BlockchainConfig.PRIVATE_KEY)
    print(f"Deploying from: {account.address}")

    # Compile contracts
    print("Compiling contracts...")
    artifacts = compile_contracts()

    # Deploy contracts
    deployed_addresses = {}

    # Deploy MockUSDC first
    deployed_addresses["mockUSDC"] = deploy_contract(w3, account, "MockUSDC", artifacts)

    # Deploy SubmissionRegistry
    deployed_addresses["submissionRegistry"] = deploy_contract(w3, account, "SubmissionRegistry", artifacts)

    # Deploy VerificationManager
    deployed_addresses["verificationManager"] = deploy_contract(w3, account, "VerificationManager", artifacts)

    # Deploy BountyPool with MockUSDC address
    deployed_addresses["bountyPool"] = deploy_contract(
        w3, account, "BountyPool", artifacts,
        constructor_args=[deployed_addresses["mockUSDC"]]
    )

    # Save deployment info
    deployment_info = {
        "network": BlockchainConfig.NETWORK,
        "chainId": BlockchainConfig.CHAIN_ID,
        "deployer": account.address,
        "addresses": deployed_addresses,
        "deployedAt": "2025-10-01"
    }

    os.makedirs("deployments", exist_ok=True)
    with open("deployments/addresses.json", "w") as f:
        json.dump(deployment_info, f, indent=2)

    print("\n=== Deployment Summary ===")
    print(f"Network: {deployment_info['network']}")
    for contract, address in deployed_addresses.items():
        print(f"{contract}: {address}")
    print("\nAddresses saved to deployments/addresses.json")

if __name__ == "__main__":
    main()