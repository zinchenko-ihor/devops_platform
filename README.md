# 🚀 DevOps Platform

Automated platform for deploying and managing applications based on **Kubernetes (K3S)** with full **CI/CD** integration via GitHub Actions and **HashiCorp Vault** for secure secrets management.

## 📋 What is this?

This is a local DevOps platform that demonstrates best practices:
- ✅ Local Kubernetes cluster (K3S)
- ✅ Self-hosted GitHub Runner for CI/CD
- ✅ HashiCorp Vault for credentials management
- ✅ Secure Docker Hub credentials storage
- ✅ Automated building and deployment
- ✅ Load Balancing via MetalLB
- ✅ Access via NGINX Ingress with TLS certificates
- ✅ Monitoring and logging (Grafana, Loki)

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│  (Webhook on Push → Self-Hosted Runner Activation)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   GitHub Actions      │
         │  (Self-Hosted Runner) │
         │  - Build Backend      │
         │  - Build Frontend     │
         │  - Push to Docker Hub │
         └────────────┬──────────┘
                      │
                      ▼
      ┌──────────────────────────────┐
      │   HashiCorp Vault            │
      │ (Docker Hub Credentials)     │
      │ (AppRole Auth)               │
      └──────────────────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────┐
    │       K3S Kubernetes Cluster        │
    │  (Local: 192.168.49.240-250)       │
    │                                     │
    │  ┌─────────────────────────────┐   │
    │  │  Namespace: devops-app      │   │
    │  │                             │   │
    │  │  ┌────────┐  ┌──────────┐  │   │
    │  │  │Backend │  │ Frontend │  │   │
    │  │  │ Django │  │   Vue3   │  │   │
    │  │  └────────┘  └──────────┘  │   │
    │  └─────────────────────────────┘   │
    │                                     │
    │  ┌──────────────┐                  │
    │  │ MetalLB      │                  │
    │  │ (Load Balancer)                 │
    │  └──────────────┘                  │
    │                                     │
    │  ┌──────────────┐                  │
    │  │ NGINX Ingress│ + TLS            │
    │  └──────────────┘                  │
    │                                     │
    │  ┌──────────────────────────────┐  │
    │  │ Monitoring Stack             │  │
    │  │ - Grafana (Dashboard)        │  │
    │  │ - Loki (Log Aggregation)     │  │
    │  │ - Prometheus (Metrics)       │  │
    │  └──────────────────────────────┘  │
    └─────────────────────────────────────┘
           │
           ▼
      http://dev.local
      https://dev.local
```

---

## 🔧 Project Structure

```
devops_platform/
├── apps/                      # Application source code
│   ├── backend/              # Django REST API
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── config/           # Django configuration
│   │   ├── api/              # API endpoints
│   │   └── manage.py
│   │
│   └── frontend/             # Vue3 + TypeScript + Vite
│       ├── Dockerfile
│       ├── src/              # Vue components
│       ├── package.json
│       └── vite.config.ts
│
├── docker/                    # Docker configurations
│   ├── docker-compose.yml     # Local development
│   └── nginx/
│       └── default.conf       # NGINX config
│
├── k8s/                       # Kubernetes manifests
│   ├── namespace.yaml         # Namespace: devops-app
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml          # NGINX Ingress + TLS
│   ├── metallb/              # Load Balancer configuration
│   │   ├── l2.yaml
│   │   └── ip-pool.yaml
│   ├── cert-manager/         # SSL Certificate Management
│   │   ├── cluster-issuer.yaml
│   │   └── certificate.yaml
│   └── monitoring/           # Monitoring stack
│       ├── values-grafana.yaml
│       ├── grafana-ingress.yaml
│       └── loki-datasource.yaml
│
├── metallb-config.yaml        # MetalLB configuration (backup)
│
└── .github/
    └── workflows/
        └── deploy.yml         # CI/CD Pipeline (GitHub Actions)
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# K3S must be installed
# GitHub Self-Hosted Runner must be configured
# HashiCorp Vault running on 192.168.0.230:8200
# Docker must be installed
```

### 1. Local Development (Docker Compose)

```bash
cd docker
docker-compose up -d

# Access:
# Backend API: http://localhost:8000
# Frontend:    http://localhost:5173
# Reverse Proxy: http://localhost
```

### 2. Deployment on K3S

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy backend
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

# Deploy frontend
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Configure Ingress
kubectl apply -f k8s/ingress.yaml

# Configure TLS certificates
kubectl apply -f k8s/cert-manager/

# Configure MetalLB
kubectl apply -f metallb-config.yaml
kubectl apply -f k8s/metallb/
```

### 3. Application Access

```
Frontend: https://dev.local/
Backend API: https://dev.local/api/
Grafana (Monitoring): https://dev.local/grafana
```

---

## 🔐 HashiCorp Vault Setup

### 1. Vault Initialization

```bash
# Vault running on 192.168.0.230:8200
export VAULT_ADDR=http://192.168.0.230:8200

# Initialize Vault
vault operator init

# Unseal Vault
vault operator unseal
```

### 2. Configure AppRole for GitHub Actions

```bash
# Login to Vault
vault login

# Enable AppRole auth method
vault auth enable approle

# Create AppRole
vault write auth/approle/role/github-runner \
  bind_secret_id=true \
  secret_id_ttl=60m

# Get Role ID
vault read auth/approle/role/github-runner/role-id
# Save as GitHub Secret: VAULT_ROLE_ID

# Generate Secret ID
vault write -f auth/approle/role/github-runner/secret-id
# Save as GitHub Secret: VAULT_SECRET_ID
```

### 3. Store Docker Credentials

```bash
# Store Docker credentials in Vault
vault kv put secret/docker \
  username=your-dockerhub-username \
  password=your-dockerhub-password

# Configure permissions for AppRole
vault write auth/approle/role/github-runner/policies \
  policies=github-runner
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

### Workflow: `.github/workflows/deploy.yml`

Automated deployment process:

1. **Checkout** - Clone the repository
2. **Vault Login** - Authenticate via AppRole
3. **Get Docker Credentials** - Retrieve credentials from Vault
4. **Docker Login** - Login to Docker Hub
5. **Build Backend** - Build backend Docker image
6. **Build Frontend** - Build frontend Docker image
7. **Push to Registry** - Upload to Docker Hub
8. **Deploy to K3S** - Update images in K3S
9. **Verify Rollout** - Verify successful deployment

### Trigger

```yaml
- Push to main branch triggers automatic deployment
```

### Versioning

```
TAG: 1.0.${{ github.run_number }}
Example: 1.0.5, 1.0.42 (based on GitHub Actions run number)
```

---

## 📊 Моніторинг та Логування

### Компоненти

| Компонент | Назначення | URL |
|-----------|-----------|-----|
| **Grafana** | Dashboard для метрик | https://dev.local/grafana |
| **Loki** | Агрегація логів | http://loki:3100 |
| **Prometheus** | Збір метрик | http://prometheus:9090 |

### Налаштування Loki як Data Source

У Grafana автоматично налаштований Data Source до Loki:
- URL: `http://loki:3100`
- Type: `Loki`

---

## 🌐 Ingress and Load Balancing

### NGINX Ingress

```yaml
Host: dev.local
Routing rules:
  /api       → Backend (port 8000)
  /          → Frontend (port 80)
  
TLS: Certificate for dev.local
```

### MetalLB

```yaml
IP Pool: 192.168.49.240-192.168.49.250
Method: L2 Advertisement (Local network)
```

---

## 🐳 Docker Images

### Backend
- **Repository**: `jumper93/backend`
- **Base Image**: Python 3.x
- **Framework**: Django
- **Port**: 8000
- **Health Check**: `/api/health/`

### Frontend
- **Repository**: `jumper93/frontend`
- **Base Image**: Node.js
- **Framework**: Vue3 + TypeScript
- **Port**: 80 (internal), 5173 (development)
- **Builder**: Vite

---

## 🔌 Backend API

### Endpoints

```
GET    /api/health/    - Health check
```

### Technology Stack

- **Framework**: Django REST Framework
- **Python Version**: 3.x
- **Dependencies**: requirements.txt

### Run Locally

```bash
cd apps/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

---

## 💻 Frontend

### Technology Stack

- **Framework**: Vue3
- **Language**: TypeScript
- **Build Tool**: Vite
- **Package Manager**: npm

### Run Locally (Development)

```bash
cd apps/frontend
npm install
npm run dev

# Access: http://localhost:5173
```

### Build for Production

```bash
npm run build

# Output: dist/ folder
```

---

## 🛠️ Useful Commands

### K3S & Kubernetes

```bash
# Check deployment status
kubectl get deployments -n devops-app
kubectl get pods -n devops-app
kubectl get services -n devops-app
kubectl get ingress -n devops-app

# View pod logs
kubectl logs deployment/backend -n devops-app -f
kubectl logs deployment/frontend -n devops-app -f

# Update deployment (manual)
kubectl set image deployment/backend \
  backend=jumper93/backend:1.0.100 \
  -n devops-app

# Check rollout status
kubectl rollout status deployment/backend -n devops-app

# Restart deployment
kubectl rollout restart deployment/backend -n devops-app
```

### Vault

```bash
# Check secrets
vault kv get secret/docker

# Check AppRole
vault read auth/approle/role/github-runner
vault list auth/approle/role/github-runner/secret-id
```

### Docker

```bash
# Local development
docker-compose -f docker/docker-compose.yml up -d
docker-compose -f docker/docker-compose.yml down

# Build images
docker build -t jumper93/backend:latest apps/backend
docker build -t jumper93/frontend:latest apps/frontend

# Run containers
docker run -p 8000:8000 jumper93/backend:latest
docker run -p 80:80 jumper93/frontend:latest
```

---

## 📝 GitHub Secrets (for CI/CD)

Configure in Settings → Secrets and variables → Actions:

```
DOCKER_USERNAME           # Docker Hub username
VAULT_ROLE_ID             # AppRole Role ID
VAULT_SECRET_ID           # AppRole Secret ID
```

---

## 🔒 Security Best Practices

✅ **Vault for credentials** - Never store secrets in the repository

✅ **AppRole Authentication** - Secure authentication for CI/CD

✅ **TLS by default** - HTTPS for everything with certificates

✅ **Health Checks** - Liveness & Readiness for reliability

✅ **Namespaces** - Resource isolation (devops-app)

✅ **Image Pull Policy** - Always for fresh images

---

## 📖 Documentation

### Official Documentation Links

- [K3S Documentation](https://docs.k3s.io/)
- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [HashiCorp Vault Docs](https://www.vaultproject.io/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [MetalLB Documentation](https://metallb.universe.tf/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)

---

## 🤝 Contributing

This is a demonstration project. For changes:

1. Create a feature branch
2. Make commits with clear descriptions
3. Push to main to automatically trigger CI/CD

---

## 📄 License

This project is used for learning and demonstration purposes.

---

## 💡 Tips & Tricks

### For Local Development

```bash
# Quick start
docker-compose -f docker/docker-compose.yml up

# Verify service availability
curl http://localhost/api/health/
curl http://localhost:5173
```

### For K3S Development

```bash
# Get K3S config
cat /etc/rancher/k3s/k3s.yaml

# Configure kubeconfig
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Check nodes
kubectl get nodes
```

### For Vault Development

```bash
# List secrets
vault kv list secret/

# View AppRole credentials
vault read auth/approle/role/github-runner/role-id
```

---

**Author**: Zinchenko Ihor  
**Last Updated**: 2026-06-07  
**Version**: 1.0.x
