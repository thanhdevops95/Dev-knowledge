# CI/CD with GitHub Actions

> **Tags:** `cicd` `github-actions` `pipeline` `deployment` `testing` `docker`
> **Level:** Intermediate | **Prerequisite:** `git/01-git-basics.md`

---

## 1. Core Concepts

```
CI (Continuous Integration):    CD (Continuous Delivery/Deployment):
  - Push code                     - After CI passes:
  - Run tests automatically         - Build Docker image
  - Check code quality              - Push to registry
  - Build artifacts                 - Deploy to staging
  - Report results                  - (CD) Deploy to production automatically
                                    - (CDelivery) Manual approval for prod
```

### GitHub Actions Anatomy
```yaml
name: CI/CD Pipeline     # Workflow name (shown in UI)

on:                       # Triggers
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight
  workflow_dispatch:      # Manual trigger via UI

jobs:                     # One or more jobs (run in parallel by default)
  test:                   # Job name
    runs-on: ubuntu-22.04 # Runner OS (ubuntu-latest, windows-latest, macos-latest)
    timeout-minutes: 30   # Cancel if takes too long
    
    steps:                # Sequential steps within a job
      - name: Checkout code
        uses: actions/checkout@v4    # Use actions
        with:
          fetch-depth: 0  # Full git history
          
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'              # Cache node_modules
          
      - name: Install dependencies
        run: npm ci                 # Shell command
        
      - name: Run tests
        run: npm test
        env:
          NODE_ENV: test
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}  # Use secrets
```

---

## 2. Complete Node.js CI/CD

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ─── Job 1: Test & Lint ───────────────────────────────────────────
  test:
    name: Test & Lint
    runs-on: ubuntu-22.04
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Type check
        run: npm run typecheck
      
      - name: Unit tests
        run: npm run test:unit -- --coverage
      
      - name: Integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info

  # ─── Job 2: Security Scan ─────────────────────────────────────────
  security:
    name: Security Scan
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - name: Snyk vulnerability scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  # ─── Job 3: Build & Push Docker Image ─────────────────────────────
  build:
    name: Build & Push Image
    needs: [test, security]          # Wait for test + security to pass
    runs-on: ubuntu-22.04
    if: github.ref == 'refs/heads/main'   # Only on main branch
    permissions:
      contents: read
      packages: write
    
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}  # Automatically provided!
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=sha-
            type=ref,event=branch
            type=semver,pattern={{version}}
      
      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha      # Use GitHub Actions cache
          cache-to: type=gha,mode=max
      
      - name: Scan image for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }}
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  # ─── Job 4: Deploy to Staging ─────────────────────────────────────
  deploy-staging:
    name: Deploy to Staging
    needs: build
    runs-on: ubuntu-22.04
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'v1.29.0'
      
      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG_STAGING }}" | base64 -d > kubeconfig.yaml
          echo "KUBECONFIG=kubeconfig.yaml" >> $GITHUB_ENV
      
      - name: Deploy to staging
        run: |
          IMAGE="${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }}"
          kubectl set image deployment/api api="${IMAGE}" -n staging
          kubectl rollout status deployment/api -n staging --timeout=300s
      
      - name: Run smoke tests
        run: |
          sleep 10
          curl -f https://staging.example.com/health || exit 1

  # ─── Job 5: Deploy to Production (with approval) ──────────────────
  deploy-production:
    name: Deploy to Production
    needs: deploy-staging
    runs-on: ubuntu-22.04
    environment:
      name: production        # GitHub Environment with required reviewers!
      url: https://example.com
    
    steps:
      - name: Deploy to production
        run: |
          IMAGE="${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }}"
          # ... kubernetes deploy commands
      
      - name: Notify Slack
        if: always()    # Run even if previous step failed
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "${{ job.status == 'success' && '✅' || '❌' }} Production deploy: ${{ github.sha }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 3. Reusable Workflows

```yaml
# .github/workflows/deploy-service.yml (Reusable)
on:
  workflow_call:    # Can be called from other workflows
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
      service-name:
        required: true
        type: string
    secrets:
      kube-config:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-22.04
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy ${{ inputs.service-name }}
        run: |
          echo "${{ secrets.kube-config }}" | base64 -d > kubeconfig.yaml
          kubectl set image deployment/${{ inputs.service-name }} \
            ${{ inputs.service-name }}=${{ inputs.image-tag }} \
            -n ${{ inputs.environment }}

---
# .github/workflows/main.yml (Caller)
jobs:
  deploy-user-service:
    uses: ./.github/workflows/deploy-service.yml
    with:
      environment: production
      image-tag: ghcr.io/org/user-service:sha-abc123
      service-name: user-service
    secrets:
      kube-config: ${{ secrets.KUBE_CONFIG_PROD }}
```

---

## 4. Composite Actions

```yaml
# .github/actions/setup-python/action.yml
name: Setup Python & Dependencies
description: Setup Python environment with caching

inputs:
  python-version:
    description: Python version
    default: '3.12'

runs:
  using: composite
  steps:
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
    
    - name: Cache pip
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: pip-${{ hashFiles('**/requirements*.txt') }}
    
    - name: Install dependencies
      shell: bash
      run: pip install -r requirements.txt -r requirements-dev.txt

---
# Usage
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-python     # Local action!
    with:
      python-version: '3.12'
  - run: pytest
```

---

## 5. Matrix Strategy

```yaml
jobs:
  test:
    strategy:
      fail-fast: false     # Don't cancel other matrix jobs on failure
      matrix:
        os: [ubuntu-22.04, windows-latest, macos-latest]
        node: ['18', '20', '21']
        exclude:
          - os: macos-latest
            node: '18'     # Skip macOS + Node 18 combo
    
    runs-on: ${{ matrix.os }}
    name: Test on ${{ matrix.os }} / Node ${{ matrix.node }}
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci && npm test

  # Dynamic matrix from API or file
  test-services:
    strategy:
      matrix:
        service: ${{ fromJSON(needs.get-services.outputs.services) }}
    # ... 
```

---

## 6. Secrets & Environment Variables

```yaml
# Repository secrets → Settings → Secrets and variables → Actions
# Organization secrets → available to all repos

# Use secrets
steps:
  - name: Deploy
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    run: |
      echo "Deploying..."
      # Secrets are masked in logs: ***

# GitHub-provided secrets (no setup needed)
# ${{ secrets.GITHUB_TOKEN }} - GitHub API access, packages write, etc.
# ${{ github.sha }} - Current commit SHA
# ${{ github.ref }} - Branch/tag ref
# ${{ github.actor }} - Who triggered the workflow
# ${{ github.repository }} - owner/repo-name
# ${{ github.event.number }} - PR number

# Environment-specific secrets
environment: production    # Must review and approve in GitHub Environments UI
```

---

## 7. Caching

```yaml
# Cache node_modules (built into setup-node)
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'    # Or 'yarn', 'pnpm'

# Manual cache
- name: Cache
  uses: actions/cache@v4
  id: cache-deps
  with:
    path: |
      ~/.cache/pip
      .venv
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-    # Fallback to partial match

- name: Install (only if cache miss)
  if: steps.cache-deps.outputs.cache-hit != 'true'
  run: pip install -r requirements.txt

# Docker layer cache
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

---

## 8. Artifacts

```yaml
# Upload artifact
- name: Run tests with coverage
  run: npx jest --coverage

- name: Upload coverage report
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: coverage/
    retention-days: 30    # Delete after 30 days

- name: Upload build
  uses: actions/upload-artifact@v4
  if: success()
  with:
    name: build-${{ github.sha }}
    path: dist/

# Download artifact (in another job)
- name: Download build
  uses: actions/download-artifact@v4
  with:
    name: build-${{ github.sha }}
    path: dist/
```

---

## 9. PR Checks & Code Quality

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  danger:
    name: Danger Check
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - run: npx @danger/danger-js ci
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        # Danger checks: PR size, test files, changelog, etc.

  sonarcloud:
    name: SonarCloud Analysis
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # Full history for blame info
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  size-check:
    name: Bundle Size Check
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: maxkomarychev/oction-bundles@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          max-size-kb: 200    # Fail if bundle > 200KB
```

---

## 10. Best Practices

```yaml
# 1. Pin actions to full SHA (security)
uses: actions/checkout@v4          # Bad: tag can be moved
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # Good: pinned SHA

# 2. Minimal permissions
permissions:
  contents: read
  packages: write
  # Don't use: permissions: write-all

# 3. Timeout on jobs
jobs:
  test:
    timeout-minutes: 20   # Cancel stuck jobs

# 4. Concurrency (cancel outdated runs)
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true   # Cancel previous run on same branch

# 5. Conditions
if: github.ref == 'refs/heads/main'
if: github.event_name == 'push'
if: contains(github.event.pull_request.labels.*.name, 'deploy')
if: failure()    # Only run if previous step failed
if: always()     # Always run (for cleanup)

# 6. OIDC for cloud auth (no long-lived credentials!)
permissions:
  id-token: write
  contents: read

- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/github-actions
    aws-region: us-east-1
```

---

*Tài liệu liên quan: `git/01-git-basics.md` | `docker/02-docker-advanced.md` | `kubernetes/02-kubernetes-advanced.md`*
