#!/bin/bash

# Script test ứng dụng sau khi deploy

set -e

echo "=========================================="
echo "🧪 K8s Full Demo - Test Application"
echo "=========================================="

# Lấy NodePort của service
NODE_PORT=$(kubectl get svc curl-app-service -o jsonpath='{.spec.ports[0].nodePort}')
MINIKUBE_IP=$(minikube ip)

echo ""
echo "🌐 Service Information:"
echo "======================"
kubectl get svc curl-app-service -o wide

echo ""
echo "📍 Minikube IP: $MINIKUBE_IP"
echo "🔓 NodePort: $NODE_PORT"
echo "🌍 Access URL: http://$MINIKUBE_IP:$NODE_PORT"
echo ""

# Test từ trong cluster (exec vào pod)
echo "🧪 Test 1: Access từ trong cluster"
echo "==================================="
POD_NAME=$(kubectl get pods -l app=curl-app -o jsonpath='{.items[0].metadata.name}')
echo "📦 Pod name: $POD_NAME"
echo ""

echo "Exec vào pod và test curl đến service..."
kubectl exec -it $POD_NAME -- /bin/sh -c "echo 'Testing curl to service...' && curl -s http://curl-app-service:8080 || echo 'Service not responding (expected - no HTTP server)'"

echo ""
echo "🧪 Test 2: Check Pod IP"
echo "======================="
kubectl get pod $POD_NAME -o wide

echo ""
echo "🧪 Test 3: Curl từ pod đến pod khác"
POD2_NAME=$(kubectl get pods -l app=curl-app -o jsonpath='{.items[1].metadata.name}')
if [ ! -z "$POD2_NAME" ] && [ "$POD_NAME" != "$POD2_NAME" ]; then
    echo "Pods trong same deployment:"
    kubectl get pods -l app=curl-app -o custom-columns=NAME:.metadata.name,IP:.status.podIP
    echo ""
    echo "Exec vào $POD_NAME và ping đến $POD2_NAME..."
    kubectl exec -it $POD_NAME -- /bin/sh -c "ping -c 2 $POD2_NAME || echo 'ping failed (expected if no ping)'"
fi

echo ""
echo "🧪 Test 4: Xem endpoints của service"
echo "====================================="
kubectl get endpoints curl-app-service

echo ""
echo "🧪 Test 5: Service Port forwarding (nếu không có NodePort)"
echo "========================================================="
echo "Port forward command (alternative to NodePort):"
echo "kubectl port-forward svc/curl-app-service 8080:8080"
echo "Then access: http://localhost:8080"

echo ""
echo "✅ Testing complete!"
echo ""
echo "📚 More commands to try:"
echo "- kubectl logs <pod-name>              # Xem logs"
echo "- kubectl describe pod <pod-name>     # Xem chi tiết pod"
echo "- kubectl exec -it <pod-name> -- bash # Vào shell pod"
echo "- kubectl get replicaset              # Xem replicaset"
echo "- kubectl describe deployment curl-app-deployment  # Xem deployment"
