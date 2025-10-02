#!/bin/bash

# Blockchain Submission POC - Server Runner
# This script sets up and runs the complete blockchain + API stack

set -e  # Exit on any error

echo "🚀 Starting Blockchain Submission POC"
echo "======================================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration before running again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating Python virtual environment..."
source venv/bin/activate

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to start Hardhat node
start_hardhat_node() {
    echo "🔗 Starting local blockchain (Hardhat node)..."

    if check_port 8545; then
        echo "   ✅ Blockchain already running on port 8545"
    else
        echo "   🔄 Starting new Hardhat node..."
        npx hardhat node > hardhat.log 2>&1 &
        HARDHAT_PID=$!
        echo $HARDHAT_PID > .hardhat_pid

        # Wait for Hardhat to start
        echo "   ⏳ Waiting for Hardhat node to start..."
        for i in {1..30}; do
            if check_port 8545; then
                echo "   ✅ Hardhat node started successfully"
                break
            fi
            sleep 1
        done

        if ! check_port 8545; then
            echo "   ❌ Failed to start Hardhat node"
            exit 1
        fi
    fi
}

# Function to deploy contracts
deploy_contracts() {
    echo "📋 Deploying smart contracts..."

    if [ -f "deployments/addresses.json" ]; then
        echo "   ⚠️  Contracts already deployed. Delete deployments/addresses.json to redeploy"
        echo "   ✅ Using existing deployment"
    else
        echo "   🔄 Deploying contracts to local network..."
        npx hardhat run scripts/deploy.js --network localhost

        if [ -f "deployments/addresses.json" ]; then
            echo "   ✅ Contracts deployed successfully"
        else
            echo "   ❌ Contract deployment failed"
            exit 1
        fi
    fi
}

# Function to start FastAPI server
start_api_server() {
    echo "🌐 Starting FastAPI server..."

    if check_port 8000; then
        echo "   ⚠️  Port 8000 already in use. Stopping existing server..."
        # Kill any existing server on port 8000
        lsof -ti:8000 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi

    echo "   🔄 Starting FastAPI server..."
    python main.py &
    API_PID=$!
    echo $API_PID > .api_pid

    # Wait for API to start
    echo "   ⏳ Waiting for API server to start..."
    for i in {1..30}; do
        if check_port 8000; then
            echo "   ✅ API server started successfully"
            break
        fi
        sleep 1
    done

    if ! check_port 8000; then
        echo "   ❌ Failed to start API server"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    if [ "$1" = "--test" ]; then
        echo "🧪 Running API tests..."
        sleep 3  # Give server time to fully initialize
        python test_api.py
    fi
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."

    # Kill API server
    if [ -f ".api_pid" ]; then
        API_PID=$(cat .api_pid)
        if kill -0 $API_PID 2>/dev/null; then
            echo "   🔸 Stopping API server (PID: $API_PID)..."
            kill $API_PID 2>/dev/null || true
        fi
        rm -f .api_pid
    fi

    # Kill Hardhat node (only if we started it)
    if [ -f ".hardhat_pid" ]; then
        HARDHAT_PID=$(cat .hardhat_pid)
        if kill -0 $HARDHAT_PID 2>/dev/null; then
            echo "   🔸 Stopping Hardhat node (PID: $HARDHAT_PID)..."
            kill $HARDHAT_PID 2>/dev/null || true
        fi
        rm -f .hardhat_pid
    fi

    echo "   ✅ Cleanup complete"
}

# Set up cleanup on script exit
trap cleanup EXIT INT TERM

# Main execution
main() {
    start_hardhat_node
    deploy_contracts
    start_api_server

    echo ""
    echo "🎉 Blockchain Submission POC is running!"
    echo "======================================="
    echo "🔗 Blockchain:     http://localhost:8545"
    echo "🌐 API Server:     http://localhost:8000"
    echo "📖 API Docs:       http://localhost:8000/docs"
    echo "🔧 Interactive:    http://localhost:8000/redoc"
    echo ""

    run_tests "$1"

    if [ "$1" != "--test" ]; then
        echo "💡 Tips:"
        echo "   - Visit http://localhost:8000/docs for API documentation"
        echo "   - Run 'python test_api.py' to test the complete workflow"
        echo "   - Press Ctrl+C to stop all services"
        echo ""
        echo "⏳ Server running... (Press Ctrl+C to stop)"

        # Keep script running
        while true; do
            sleep 1
        done
    fi
}

# Run main function with all arguments
main "$@"