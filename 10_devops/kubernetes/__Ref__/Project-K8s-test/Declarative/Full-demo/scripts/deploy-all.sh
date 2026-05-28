#!/bin/bash

# Script deploy tất cả resources K8s

set -e  # Exit nếu có lỗi

echo "=========================================="
echo "🚀 K8s Full Demo - Deploy All Resources"
echo "=========================================="

# Kiểm tra minikube
echo "📋 Checking minikube status..."
if ! minikube status > /dev/null 2>&1; then
    echo "❌ Minikube is not running!"
    echo "💡 Start minikube với: minikube start --driver=docker"
    exit 1
fi

echo "✅ Minikube is running"

# Apply tất cả YAML files
echo ""
echo "📦 Deploying YAML manifests..."
kubectl apply -f yaml-manifests/

# Wait cho pods ready
echo ""
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod --all --timeout=120s

# Hiển thị status
echo ""
echo "📊 Deployment Status:"
echo "===================="
kubectl get all

echo ""
echo "✅ All resources deployed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Xem pods: kubectl get pods -o wide"
echo "2. Xem service: kubectl get svc curl-app-service"
echo "3. Test app: ./scripts/test-app.sh"
echo "4. Xem chi tiết: kubectl describe <resource> <name>"
echo ""
echo "💡 Cleanup: ./scripts/cleanup.sh"
