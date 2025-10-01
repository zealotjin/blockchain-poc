import os
from dotenv import load_dotenv

load_dotenv()

class BlockchainConfig:
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    RPC_URL = os.getenv("RPC_URL")
    NETWORK = os.getenv("NETWORK", "sepolia")
    CHAIN_ID = int(os.getenv("CHAIN_ID", "11155111"))

    # Contract addresses (updated after deployment)
    SUBMISSION_REGISTRY_ADDRESS = os.getenv("SUBMISSION_REGISTRY_ADDRESS")
    VERIFICATION_MANAGER_ADDRESS = os.getenv("VERIFICATION_MANAGER_ADDRESS")
    BOUNTY_POOL_ADDRESS = os.getenv("BOUNTY_POOL_ADDRESS")
    STABLECOIN_ADDRESS = os.getenv("STABLECOIN_ADDRESS")

    # FastAPI config
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    @classmethod
    def validate(cls):
        required_fields = ["PRIVATE_KEY", "RPC_URL"]
        missing = [field for field in required_fields if not getattr(cls, field)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
        return True