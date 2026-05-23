# Kubernetes Commands Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Commonly used Kubernetes commands for quick reference -- Các lệnh Kubernetes thường dùng để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [Cluster Info](#cluster-info) -- Thông tin Cluster
- [Kubectl Basics](#kubectl-basics) -- Kubectl Cơ bản
- [Pods](#pods) -- Pods
- [Deployments](#deployments) -- Deployments
- [Services](#services) -- Services
- [ConfigMaps & Secrets](#configmaps--secrets) -- ConfigMaps và Secrets
- [Namespaces](#namespaces) -- Namespaces
- [Logs & Debugging](#logs--debugging) -- Logs và Debug
- [Resource Management](#resource-management) -- Quản lý Resources
- [Context & Config](#context--config) -- Context và Cấu hình

## <a id="cluster-info"></a> Cluster Info -- Thông tin Cluster

```bash
# Cluster information -- Thông tin cluster
kubectl cluster-info                    # Display cluster info -- Hiển thị thông tin cluster
kubectl cluster-info dump               # Dump cluster state -- Xuất trạng thái cluster
kubectl version                         # Client and server version -- Phiên bản client và server
kubectl version --short                 # Short version -- Phiên bản ngắn gọn

# Nodes -- Các node
kubectl get nodes                       # List nodes -- Liệt kê nodes
kubectl get nodes -o wide              # Detailed node info -- Thông tin node chi tiết
kubectl describe node node_name         # Node details -- Chi tiết node
kubectl top nodes                       # Node resource usage -- Sử dụng tài nguyên node
kubectl cordon node_name               # Mark node unschedulable -- Đánh dấu node không lập lịch
kubectl uncordon node_name             # Mark node schedulable -- Đánh dấu node có thể lập lịch
kubectl drain node_name                # Drain node for maintenance -- Xả node để bảo trì
```

## <a id="kubectl-basics"></a> Kubectl Basics -- Kubectl Cơ bản

```bash
# Get resources -- Lấy resources
kubectl get all                         # Get all resources -- Lấy tất cả resources
kubectl get all -n namespace            # In specific namespace -- Trong namespace cụ thể
kubectl get pods,svc,deploy             # Multiple resource types -- Nhiều loại resource

# Output formats -- Các định dạng output
kubectl get pods -o wide               # Wide output -- Output rộng
kubectl get pods -o yaml               # YAML format -- Định dạng YAML
kubectl get pods -o json               # JSON format -- Định dạng JSON
kubectl get pods -o jsonpath='{.items[*].metadata.name}'  # JSONPath query -- Truy vấn JSONPath

# Apply & Delete -- Áp dụng và Xóa
kubectl apply -f manifest.yaml          # Apply from file -- Áp dụng từ file
kubectl apply -f ./                     # Apply all files in directory -- Áp dụng tất cả file trong thư mục
kubectl apply -f https://url/file.yaml  # Apply from URL -- Áp dụng từ URL
kubectl delete -f manifest.yaml         # Delete from file -- Xóa từ file
kubectl delete pod pod_name             # Delete specific resource -- Xóa resource cụ thể

# Create resources -- Tạo resources
kubectl create namespace dev            # Create namespace -- Tạo namespace
kubectl create deployment nginx --image=nginx  # Create deployment -- Tạo deployment
kubectl create service clusterip nginx --tcp=80:80  # Create service -- Tạo service
```

## <a id="pods"></a> Pods

```bash
# List pods -- Liệt kê pods
kubectl get pods                        # List pods in current namespace -- Liệt kê pods trong namespace hiện tại
kubectl get pods -A                     # List pods in all namespaces -- Liệt kê pods trong tất cả namespaces
kubectl get pods -n namespace           # List pods in specific namespace -- Liệt kê pods trong namespace cụ thể
kubectl get pods --show-labels          # Show labels -- Hiển thị labels
kubectl get pods -l app=nginx          # Filter by label -- Lọc theo label
kubectl get pods -w                     # Watch pods -- Theo dõi pods

# Pod details -- Chi tiết pod
kubectl describe pod pod_name           # Detailed pod info -- Thông tin pod chi tiết
kubectl get pod pod_name -o yaml       # Pod YAML definition -- Định nghĩa YAML của pod

# Run pod -- Chạy pod
kubectl run nginx --image=nginx         # Run a pod -- Chạy một pod
kubectl run nginx --image=nginx --port=80  # With port -- Với cổng
kubectl run -it busybox --image=busybox -- sh  # Interactive shell -- Shell tương tác
kubectl run nginx --image=nginx --dry-run=client -o yaml  # Generate YAML -- Tạo YAML

# Execute in pod -- Thực thi trong pod
kubectl exec pod_name -- ls /           # Run command -- Chạy lệnh
kubectl exec -it pod_name -- /bin/bash  # Interactive shell -- Shell tương tác
kubectl exec -it pod_name -c container_name -- /bin/bash  # Specific container -- Container cụ thể

# Copy files -- Sao chép files
kubectl cp pod_name:/path/file ./local  # From pod to local -- Từ pod đến local
kubectl cp ./local pod_name:/path       # From local to pod -- Từ local đến pod
```

## <a id="deployments"></a> Deployments

```bash
# List deployments -- Liệt kê deployments
kubectl get deployments                 # List deployments -- Liệt kê deployments
kubectl get deploy                      # Short form -- Dạng ngắn
kubectl get deploy -o wide              # Wide output -- Output rộng

# Create deployment -- Tạo deployment
kubectl create deployment nginx --image=nginx  # Create deployment -- Tạo deployment
kubectl create deployment nginx --image=nginx --replicas=3  # With replicas -- Với replicas

# Scale -- Mở rộng
kubectl scale deployment nginx --replicas=5  # Scale replicas -- Mở rộng replicas
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80  # Autoscale -- Tự động mở rộng

# Update -- Cập nhật
kubectl set image deployment/nginx nginx=nginx:1.21  # Update image -- Cập nhật image
kubectl rollout status deployment/nginx  # Check rollout status -- Kiểm tra trạng thái rollout
kubectl rollout history deployment/nginx  # Rollout history -- Lịch sử rollout

# Rollback -- Hoàn tác
kubectl rollout undo deployment/nginx   # Rollback to previous -- Hoàn tác về trước
kubectl rollout undo deployment/nginx --to-revision=2  # Rollback to specific -- Hoàn tác về phiên bản cụ thể

# Restart -- Khởi động lại
kubectl rollout restart deployment/nginx  # Restart deployment -- Khởi động lại deployment

# Delete -- Xóa
kubectl delete deployment nginx         # Delete deployment -- Xóa deployment
```

## <a id="services"></a> Services

```bash
# List services -- Liệt kê services
kubectl get services                    # List services -- Liệt kê services
kubectl get svc                         # Short form -- Dạng ngắn
kubectl get svc -o wide                 # Wide output -- Output rộng

# Create service -- Tạo service
kubectl expose deployment nginx --port=80  # Expose deployment -- Expose deployment
kubectl expose deployment nginx --port=80 --type=NodePort  # As NodePort -- Dạng NodePort
kubectl expose deployment nginx --port=80 --type=LoadBalancer  # As LoadBalancer -- Dạng LoadBalancer

# Service types -- Các loại service
# ClusterIP: Internal cluster access only -- Chỉ truy cập nội bộ cluster
# NodePort: Expose via node port (30000-32767) -- Expose qua cổng node
# LoadBalancer: Cloud provider load balancer -- Load balancer của cloud
# ExternalName: DNS alias -- Alias DNS

# Port forwarding -- Chuyển tiếp cổng
kubectl port-forward svc/nginx 8080:80  # Forward service port -- Chuyển tiếp cổng service
kubectl port-forward pod/nginx 8080:80  # Forward pod port -- Chuyển tiếp cổng pod

# Delete service -- Xóa service
kubectl delete svc nginx               # Delete service -- Xóa service
```

## <a id="configmaps--secrets"></a> ConfigMaps & Secrets -- ConfigMaps và Secrets

```bash
# ConfigMaps
kubectl get configmaps                  # List configmaps -- Liệt kê configmaps
kubectl get cm                          # Short form -- Dạng ngắn
kubectl create configmap my-config --from-literal=key=value  # From literal -- Từ literal
kubectl create configmap my-config --from-file=config.txt  # From file -- Từ file
kubectl create configmap my-config --from-env-file=.env  # From env file -- Từ file env
kubectl describe configmap my-config    # ConfigMap details -- Chi tiết configmap
kubectl get configmap my-config -o yaml  # Get YAML -- Lấy YAML

# Secrets
kubectl get secrets                     # List secrets -- Liệt kê secrets
kubectl create secret generic my-secret --from-literal=password=pass123  # From literal -- Từ literal
kubectl create secret generic my-secret --from-file=ssh-key=~/.ssh/id_rsa  # From file -- Từ file
kubectl create secret docker-registry regcred --docker-server=url --docker-username=user --docker-password=pass  # Docker registry -- Docker registry
kubectl describe secret my-secret       # Secret details -- Chi tiết secret
kubectl get secret my-secret -o jsonpath='{.data.password}' | base64 -d  # Decode secret -- Giải mã secret
```

## <a id="namespaces"></a> Namespaces

```bash
# List namespaces -- Liệt kê namespaces
kubectl get namespaces                  # List namespaces -- Liệt kê namespaces
kubectl get ns                          # Short form -- Dạng ngắn

# Create/Delete -- Tạo/Xóa
kubectl create namespace dev            # Create namespace -- Tạo namespace
kubectl delete namespace dev            # Delete namespace -- Xóa namespace

# Set default namespace -- Đặt namespace mặc định
kubectl config set-context --current --namespace=dev  # Set default -- Đặt mặc định
kubectl config view --minify | grep namespace  # View current -- Xem hiện tại

# Work with namespace -- Làm việc với namespace
kubectl get pods -n dev                 # Get pods in namespace -- Lấy pods trong namespace
kubectl apply -f file.yaml -n dev       # Apply to namespace -- Áp dụng vào namespace
```

## <a id="logs--debugging"></a> Logs & Debugging -- Logs và Debug

```bash
# Logs
kubectl logs pod_name                   # Pod logs -- Logs của pod
kubectl logs pod_name -c container_name # Container logs -- Logs của container
kubectl logs -f pod_name                # Follow logs -- Theo dõi logs
kubectl logs --tail=100 pod_name        # Last 100 lines -- 100 dòng cuối
kubectl logs --since=1h pod_name        # Last hour -- 1 giờ gần đây
kubectl logs -l app=nginx               # Logs by label -- Logs theo label
kubectl logs --previous pod_name        # Previous container logs -- Logs container trước

# Debugging -- Debug
kubectl describe pod pod_name           # Describe pod -- Mô tả pod
kubectl get events                      # Cluster events -- Sự kiện cluster
kubectl get events --sort-by='.lastTimestamp'  # Sorted events -- Sự kiện đã sắp xếp
kubectl get events -n namespace         # Namespace events -- Sự kiện namespace
kubectl top pods                        # Pod resource usage -- Sử dụng tài nguyên pod
kubectl top pods -n namespace           # In namespace -- Trong namespace

# Debug with temporary pod -- Debug với pod tạm thời
kubectl run debug --image=busybox --rm -it -- sh  # Debug pod -- Pod debug
kubectl run debug --image=nicolaka/netshoot --rm -it -- bash  # Network debug -- Debug mạng
```

## <a id="resource-management"></a> Resource Management -- Quản lý Resources

```bash
# Resource quotas -- Hạn mức resource
kubectl get resourcequotas             # List quotas -- Liệt kê quotas
kubectl describe resourcequota quota_name  # Quota details -- Chi tiết quota

# Limit ranges -- Giới hạn range
kubectl get limitranges                # List limit ranges -- Liệt kê limit ranges
kubectl describe limitrange limit_name  # Limit range details -- Chi tiết limit range

# Edit resources -- Chỉnh sửa resources
kubectl edit deployment nginx          # Edit deployment -- Chỉnh sửa deployment
kubectl patch deployment nginx -p '{"spec":{"replicas":5}}'  # Patch resource -- Patch resource

# Labels & Annotations -- Labels và Annotations
kubectl label pod pod_name env=prod    # Add label -- Thêm label
kubectl label pod pod_name env-        # Remove label -- Xóa label
kubectl annotate pod pod_name description="my pod"  # Add annotation -- Thêm annotation

# Dry run -- Chạy thử
kubectl apply -f file.yaml --dry-run=client  # Client-side dry run -- Chạy thử phía client
kubectl apply -f file.yaml --dry-run=server  # Server-side dry run -- Chạy thử phía server
kubectl diff -f file.yaml              # Show changes -- Hiển thị thay đổi
```

## <a id="context--config"></a> Context & Config -- Context và Cấu hình

```bash
# View config -- Xem cấu hình
kubectl config view                    # View kubeconfig -- Xem kubeconfig
kubectl config view --minify           # Current context only -- Chỉ context hiện tại
kubectl config current-context         # Show current context -- Hiển thị context hiện tại

# Contexts -- Các context
kubectl config get-contexts            # List contexts -- Liệt kê contexts
kubectl config use-context context_name  # Switch context -- Chuyển context
kubectl config set-context context_name --namespace=dev  # Modify context -- Sửa context
kubectl config delete-context context_name  # Delete context -- Xóa context

# Clusters -- Các cluster
kubectl config get-clusters            # List clusters -- Liệt kê clusters
kubectl config set-cluster cluster_name --server=https://url  # Set cluster -- Đặt cluster

# Credentials -- Thông tin đăng nhập
kubectl config set-credentials user --token=token  # Set user token -- Đặt token user
kubectl config set-credentials user --client-certificate=cert.crt --client-key=key.key  # Set certs -- Đặt certs
```

---
