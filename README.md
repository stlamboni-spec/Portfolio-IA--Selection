# Multi-Pipeline AI Production Portfolio (FastAPI & MLOps)

Welcome to my professional AI and MLOps portfolio. This repository contains a production-ready, production-grade enterprise ecosystem demonstrating end-to-end Machine Learning, Deep Learning, and Generative AI pipelines focusing on modular architecture, strict data validation, infrastructure resilience, and clean code deployment.

## 🏗️ Project Architecture & Pipelines

The codebase is organized into modular services covering the entire life cycle of intelligent enterprise applications:

### 🧠 Core Generative AI & NLP (`src/`)
* **`rag_pipeline.py`** | Enterprise-grade RAG Architecture (Local LLM Integration + Optimized Vector Indexing).
* **`agents_pipeline.py`** | Multi-Agent Task Orchestrator featuring intelligent routing mechanisms powered by local Qwen instances.
* **`pdf_summarizer_pipeline.py`** | AI-Powered PDF Summarizer API for automated unstructured text extraction & abstractive summarization.
* **`nlp_pipeline.py`** | Classical NLP Text Classification API leveraging highly optimized statistical baselines (Naïve Bayes).
* **`vector_pipeline.py`** & **`recommandation_pipeline.py`** | Collaborative & Content-Based Product Recommendation API driven by fast Cosine Similarity matrices.

### 🛡️ API Security & Defensive Engineering (`security/`)
* **`gateway_pipeline.py`** | Advanced API Gateway managing secure routing layouts, token verification, and strict Pydantic v2 schemas.
* **`secure_pipeline.py`** | Secure AI Microservice Template managing robust API Key validation and CORS integration.
* **`guardrail_pipeline.py`** | LLM Cost & Token Guardrail Gate preventing text injection, prompt drifts, and infrastructure budget overruns.
* **`limiter_pipeline.py`** | Defensive Volumetric IP Defense layer dropping heavy abusive traffic (`HTTP 429 Too Many Requests`).
* **`cors_pipeline.py`** | Enterprise Network Isolation shield implementing granular Cross-Origin Resource Sharing.

### ⚡ Performance, Infrastructure & Databases
* **`batch_pipeline.py`** | High-throughput Async Inference Engine managing high-volume background processing worker queues.
* **`cache_pipeline.py`** | Low-latency Memory-Mapped Accelerator leveraging structural Redis layout layers.
* **`database_pipeline.py`** | Automated Relational Data Sync system driving text metadata persistence via SQLAlchemy ORM and lightweight SQLite layouts.
* **`webhook_pipeline.py`** | Event-Driven Streaming Engine broadcasting real-time asynchronous notifications to connected webhooks.

---

## 🚀 Quick Start & Running Microservices Locally

### 1. Installation
```bash
git clone https://github.com
cd Portfolio-IA--Selection
pip install -r requirements.txt
```

### 2. Run the Pipelines with proper path mapping
```bash
# Core GenAI Engines
uvicorn src.rag_pipeline:app --reload --port 8006
uvicorn src.agents_pipeline:app --reload --port 8007
uvicorn src.vector_pipeline:app --reload --port 8009
uvicorn src.pdf_summarizer_pipeline:app --reload --port 8005

# Infrastructure & Core Gateway
uvicorn main:app --reload --port 8000
uvicorn security.gateway_pipeline:app --reload --port 8012
uvicorn src.batch_pipeline:app --reload --port 8011
uvicorn src.cache_pipeline:app --reload --port 8013

# Security Guardrails
uvicorn security.secure_pipeline:app --reload --port 8008
uvicorn security.cors_pipeline:app --reload --port 8014
uvicorn security.guardrail_pipeline:app --reload --port 8016
uvicorn security.limiter_pipeline:app --reload --port 8019

# Databases, Streaming & Monitoring
uvicorn monitoring.monitor_pipeline:app --reload --port 8010
uvicorn monitoring.logging_pipeline:app --reload --port 8015
uvicorn src.database_pipeline:app --reload --port 8017
uvicorn src.webhook_pipeline:app --reload --port 8018

# Analytics & Machine Learning
uvicorn src.churn_pipeline:app --reload --port 8011
uvicorn src.nlp_pipeline:app --reload --port 8012
uvicorn src.segmentation_pipeline:app --reload --port 8003
uvicorn src.recommandation_pipeline:app --reload --port 8004
```

---

## 🐳 Docker Local Orchestration

To spin up the entire ecosystem (Microservices, In-Memory Caching, Databases, and Security Proxies) locally in containers, execute:

```bash
docker-compose up -d --build
```

* **Swagger API Endpoint Docs:** `http://localhost:8000/docs`
* **Real-Time Monitoring Metrics (`monitoring/`):** Integrated with Prometheus/Grafana collectors via `monitor_pipeline.py` to output inference latencies and API status distribution in real-time.
