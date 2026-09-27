# Enterprise Digital Identity, Trust & Deepfake Detection Platform
### Production Deployment Guide

---

## 1. Quick Start (Standalone Local Development)

### Prerequisites
- Python 3.12+ (or Python 3.14)
- Git & Bash

### Step 1: Clone and Set Up Virtual Environment
```bash
git clone <repo-url> digital-identity-platform
cd digital-identity-platform

python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Step 2: Execute Engine Test Suite
```bash
PYTHONPATH="." ./venv/bin/pytest backend/tests/test_engines.py -v
```

### Step 3: Launch Local Gateway
```bash
./run_server.sh
```
Open **`http://localhost:8000`** in your browser to experience the Executive Dashboard, Live Studio, Knowledge Graph, AI Copilot, and Alert Center.
API Documentation is available at **`http://localhost:8000/docs`**.

---

## 2. Enterprise Docker Stack Deployment

The production deployment runs as an isolated micro-services cluster managed by Docker Compose:

```bash
docker-compose up -d --build
```

### Verified Service Endpoints:
- **Core Gateway & UI:** `http://localhost:8000`
- **PostgreSQL Database:** `localhost:5432`
- **Neo4j Knowledge Graph:** `http://localhost:7474` (Bolt: `localhost:7687`)
- **Redis Cache & State:** `localhost:6379`
- **Kafka Event Streaming Broker:** `localhost:9092`

---

## 3. Kubernetes Production Topology

For high availability across multiple availability zones supporting 250M+ records:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trust-core-api
  labels:
    app: trust-identity
spec:
  replicas: 12
  selector:
    matchLabels:
      app: trust-identity
  template:
    metadata:
      labels:
        app: trust-identity
    spec:
      containers:
      - name: trust-api
        image: trust/core-api:1.0.0
        resources:
          limits:
            cpu: "4000m"
            memory: "8Gi"
          requests:
            cpu: "1000m"
            memory: "2Gi"
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
```

---

## 4. Environment Variables Reference

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `HOST` | `0.0.0.0` | API bind address |
| `PORT` | `8000` | Gateway port |
| `POSTGRES_URL` | `postgresql://...` | Connection URI for identity database |
| `NEO4J_URI` | `bolt://neo4j:7687` | Knowledge Graph cluster Bolt protocol URI |
| `REDIS_URL` | `redis://redis:6379/0`| High-throughput session cache |
| `KAFKA_BOOTSTRAP_SERVERS`| `kafka:9092` | Event-driven partition broker |
| `TRUST_AUTO_APPROVE` | `800` | Minimum score for automated KYC pass |
| `DEEPFAKE_ALERT_THRESHOLD`| `0.50` | Critical probability cutoff for deepfake flag |
