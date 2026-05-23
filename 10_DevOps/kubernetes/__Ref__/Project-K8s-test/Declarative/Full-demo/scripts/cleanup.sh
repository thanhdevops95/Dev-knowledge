#!/bin/bash

# Script cleanup tất cả resources

echo "=========================================="
echo "🧹 K8s Full Demo - Cleanup Resources"
echo "=========================================="

# Xóa tất cả resources trong yaml-manifests
echo "🗑️  Deleting YAML manifests..."
kubectl delete -f yaml-manifests/ 2>/dev/null || true

# Hoặc xóa tất cả resources có label app=curl-app
echo ""
echo "🗑️  Deleting resources by label..."
kubectl delete all -l app=curl-app 2>/dev/null || true

# Xóa tất cả pods, services, deployments, replicasets còn sót lại
echo ""
echo "🧹 Force cleanup remaining resources..."
kubectl delete pod,service,deployment,replicaset --all 2>/dev/null || true

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Current resources:"
kubectl get all
