#!/bin/bash
set -e

echo "🚀 Starting Server Setup for Ubuntu 24.04..."

# 1. Update and Upgrade System
echo "🔄 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install Python 3 and Pip
echo "🐍 Installing Python and Pip..."
sudo apt-get install -y python3 python3-pip python3-venv
python3 --version
pip3 --version || echo "Pip3 installation check (some Ubuntu versions require python3-pip package explicitly)"

# 3. Install Kubernetes (k3s - lightweight and easy for single node)
if ! command -v kubectl &> /dev/null; then
    echo "☸️ Installing k3s (Kubernetes)..."
    curl -sfL https://get.k3s.io | sh -
    
    # Wait for nodes to be ready
    echo "⏳ Waiting for K3s to start..."
    sleep 10
    
    # Setup kubeconfig for the current user
    mkdir -p ~/.kube
    sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
    sudo chown $(id -u):$(id -g) ~/.kube/config
    chmod 600 ~/.kube/config
    
    echo "export KUBECONFIG=~/.kube/config" >> ~/.bashrc
else
    echo "✅ Kubernetes (kubectl) already installed."
fi

# 4. Install k9s
if ! command -v k9s &> /dev/null; then
    echo "🐶 Installing K9s..."
    K9S_VERSION=$(curl -s "https://api.github.com/repos/derailed/k9s/releases/latest" | grep -Po '"tag_name": "v\K[^"]*')
    curl -Lo k9s.tar.gz https://github.com/derailed/k9s/releases/download/v${K9S_VERSION}/k9s_Linux_amd64.tar.gz
    tar -xzf k9s.tar.gz k9s
    sudo mv k9s /usr/local/bin/
    rm k9s.tar.gz
    echo "✅ K9s installed."
else
    echo "✅ K9s already installed."
fi

echo "✨ Setup Complete!"
kubectl get nodes
