#!/bin/bash

# Blockchain Submission POC - Setup Script
# This script sets up the development environment

set -e  # Exit on any error

echo "🔧 Setting up Blockchain Submission POC"
echo "========================================"

# Check Python version
echo "🐍 Checking Python version..."
python3 --version || {
    echo "❌ Python 3 is required but not installed"
    exit 1
}

# Check Node.js version
echo "📦 Checking Node.js version..."
node --version || {
    echo "❌ Node.js is required but not installed"
    exit 1
}

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔧 Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please review and update .env with your configuration"
else
    echo "✅ .env file already exists"
fi

# Create deployments directory
mkdir -p deployments

echo ""
echo "🎉 Setup complete!"
echo "=================="
echo "📝 Next steps:"
echo "   1. Review .env configuration"
echo "   2. Run: ./run_server.sh"
echo "   3. Visit: http://localhost:8000/docs"
echo ""
echo "🧪 To run with tests: ./run_server.sh --test"