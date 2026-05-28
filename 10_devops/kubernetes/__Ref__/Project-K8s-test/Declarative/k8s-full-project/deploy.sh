#!/bin/bash

# Kubernetes Learning Project - Quick Start Script
# Chạy script này từ thư mục k8s-full-project

set -e  # Exit nếu có lỗi

echo "=========================================="
echo "K8s Learning Project - Deployment Script"
echo "=========================================="
echo ""

# Kiểm tra kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl không tìm thấy. Cài đặt kubectl trước."
    exit 1
fi

# Kiểm tra cluster
echo "1. Kiểm tra cluster..."
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Không kết nối được cluster. Kiểm tra:"
    echo "   - Minikube: minikube start"
    echo "   - Docker Desktop: Enable Kubernetes"
    echo "   - Kind: kind create cluster"
    exit 1
fi
echo "✅ Cluster đang chạy"
echo ""

# Kiểm tra nodes
echo "2. Nodes trong cluster:"
kubectl get nodes
echo ""

# Apply ConfigMaps trước
echo "3. Applying ConfigMaps..."
kubectl apply -f configmaps/
echo "✅ ConfigMaps đã được apply"
echo ""

# Apply Pods
echo "4. Applying Pods..."
kubectl apply -f pods/
echo "✅ Pods đã được apply"
echo ""

# Apply Deployments
echo "5. Applying Deployments..."
kubectl apply -f deployments/
echo "✅ Deployments đã được apply"
echo ""

# Apply Services
echo "6. Applying Services..."
kubectl apply -f services/
echo "✅ Services đã được apply"
echo ""

# Wait for pods to be ready
echo "7. Đợi các Pods chạy (30 giây)..."
sleep 30

# Kiểm tra trạng thái
echo "8. Kiểm tra trạng thái..."
echo ""
echo "Pods:"
kubectl get pods -o wide
echo ""
echo "Deployments:"
kubectl get deployments
echo ""
echo "Services:"
kubectl get services
echo ""
echo "Nodes:"
kubectl get nodes -o wide
echo ""

# Kiểm tra endpoints
echo "9. Service endpoints:"
kubectl get endpoints curl-service
echo ""

echo "=========================================="
echo "✅ Deployment hoàn tất!"
echo "=========================================="
echo ""
echo "Các bước tiếp theo:"
echo ""
echo "📋 XEM TRẠNG THÁI:"
echo "   kubectl get all"
echo "   kubectl get pods -o wide"
echo ""
echo "🔍 XEM LOGS:"
echo "   kubectl logs curl-pod"
echo "   kubectl logs -l app=curl-app"
echo ""
echo "🚀 TEST ỨNG DỤNG:"
echo ""
echo "   Method 1 - Port-forward (không cần NodePort):"
echo "   kubectl port-forward service/curl-service 8080:80"
echo "   → Mở http://localhost:8080 trong browser"
echo ""
echo "   Method 2 - Sử dụng NodePort:"
echo "   NODE_IP=\$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type==\"InternalIP\")].address}')"
echo "   curl http://\$NODE_IP:30080"
echo ""
echo "   Method 3 - Minikube:"
echo "   minikube service curl-service"
echo ""
echo "   Method 4 - Exec vào Pod và test từ trong cluster:"
echo "   kubectl exec -it curl-pod -- sh"
echo "   # Trong Pod: curl http://curl-service:80"
echo ""
echo "🐛 DEBUG:"
echo "   kubectl describe pod curl-pod"
echo "   kubectl describe service curl-service"
echo "   kubectl get events --sort-by='.lastTimestamp'"
echo ""
echo "🧪 TEST LABELS & SELECTORS:"
echo "   kubectl get pods -l app=curl-app"
echo "   kubectl get pods -l tier=backend"
echo "   kubectl get pods --show-labels"
echo ""
echo "🔧 SCALE DEPLOYMENT:"
echo "   kubectl scale deployment curl-deployment --replicas=5"
echo ""
echo "🗑️  XÓA TẤT CẢ:"
echo "   kubectl delete -f ."
echo "   hoặc:"
echo "   kubectl delete -f services/"
echo "   kubectl delete -f deployments/"
echo "   kubectl delete -f pods/"
echo "   kubectl delete -f configmaps/"
echo ""
echo "=========================================="
echo "📚 Xem file KUBERNETES-EXPLAINED.md để học chi tiết"
echo "=========================================="
