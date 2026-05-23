# 🔧 Troubleshooting Guide (Hướng dẫn xử lý sự cố)

> **Common issues and solutions for DevOps Tools Setup.**
>
> *Các lỗi thường gặp và giải pháp khi cài đặt công cụ DevOps.*

---

## 📋 Table of Contents

1. [General Issues (Lỗi chung)](#general-issues)
2. [WSL2 & Windows](#wsl2--windows)
3. [Docker Issues](#docker-issues)
4. [Kubernetes (Minikube/Kubectl)](#kubernetes-minikubekubectl)
5. [Network Issues](#network-issues)

---

## General Issues

### "Command not found" acts strange

> **Problem:** You installed a tool but typing the command gives usually `command not found`.
>
> **Reason:** The tool's installation directory is not in your system `PATH`.
>
> **Fix:**
> - **Windows:** System Properties -> Environment Variables -> Path -> Edit -> Add path.
> - **Mac/Linux:** Add to `~/.zshrc` or `~/.bashrc`: `export PATH=$PATH:/path/to/tool`

---

## WSL2 & Windows

### Virtualization Error

> ⚠️ **Error:** `Please enable the Virtual Machine Platform Windows feature and ensure virtualization is enabled in the BIOS.`
>
> **Fix:**
> 1. Enable **Virtualization** in BIOS settings (F2/Del on startup).
> 2. Enable **Virtual Machine Platform** in "Turn Windows features on or off".
> 3. Run: `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`

---

## Docker Issues

### Permission Denied (Linux)

> ⚠️ **Error:** `Got permission denied while trying to connect to the Docker daemon socket`
>
> **Fix:**
> ```bash
> sudo usermod -aG docker $USER
> # Then log out and log back in!
> ```

### "No space left on device"

> ⚠️ **Error:** Pulling images fails with disk space error.
>
> **Fix:** Clean up unused images/containers.
> ```bash
> docker system prune -a
> ```

---

## Kubernetes (Minikube/Kubectl)

### Minikube fails to start

> ⚠️ **Error:** `Exiting due to GUEST_PROVISION` or stuck at `Starting control plane node`.
>
> **Fix:**
> 1. Update minikube: `minikube update-check`
> 2. Delete and restart:
>    ```bash
>    minikube delete
>    minikube start --driver=docker
>    ```

---

## 🔗 Navigation

[⬅️ TOOLS OVERVIEW](./TOOLS_OVERVIEW.md)
