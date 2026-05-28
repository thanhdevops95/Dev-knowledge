# Module 13: Security Scenarios

---

## 🚨 Scenario 1: "Secret committed to Git"

### 💡 Immediate Actions

1. **Revoke the secret** immediately
2. **Remove from history:**

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
git push --force --all
```

3. **Add to .gitignore**
4. **Audit access logs**

---

## 🚨 Scenario 2: "Container running as root"

### 💡 Fix Dockerfile

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

---

## 🚨 Scenario 3: "Vulnerable dependency found"

```bash
# Check severity
npm audit

# Auto-fix
npm audit fix

# If breaking changes
npm audit fix --force
# OR update manually
```

---

## 📋 Security Troubleshooting

| Issue | Action |
|-------|--------|
| Secret leaked | Rotate immediately |
| Vulnerable dep | Update/patch |
| Container root | Add non-root user |

👉 **[Module 14: Observability](../14_OBSERVABILITY/README.md)**
