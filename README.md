# Multi-Pipeline AI Production Portfolio (FastAPI, MLOps & Cloud Infrastructure)

Welcome to my professional AI, MLOps, and Cloud Infrastructure portfolio. This repository contains a production-ready, production-grade enterprise ecosystem demonstrating end-to-end Machine Learning, Deep Learning, and Generative AI pipelines focusing on cloud orchestration, modular architecture, strict data validation, infrastructure resilience, and clean code deployment.

## 🏗️ Cloud Orchestration & Infrastructure (Production-Grade)

The entire microservices ecosystem is designed to run on highly available cloud environments, leveraging modern DevSecOps, Containerization, and GitOps workflows:

* **🐳 Multi-Container Docker Orchestration:** Complete stack containerization (`docker-compose up -d --build`) isolating microservices, databases, proxies, and caching layers into standardized environments.
* **🎡 Kubernetes & Helm Architecture:** Formatted to easily port into Kubernetes Clusters using declarative manifests, custom Operator/CRD logics, and modular Helm Charts for fluid environment staging (Dev/Staging/Prod).
* **📈 Asynchronous Autoscaling (KEDA-ready):** Powered by an event-driven streaming pipeline via real-time Webhooks. The architecture natively supports event-driven auto-scalers like KEDA to scale Kubernetes pods based on background queue volumes.
* **📊 Monitoring & Observability:** Integrated with custom telemetry modules (`monitoring/monitor_pipeline.py`) designed to interface with Prometheus and Grafana collectors, outputting real-time inference latencies and HTTP status distributions.

## 🏗️ Project Architecture & Pipelines

The codebase is organized into modular services covering the entire life cycle of intelligent enterprise applications:

### 🧠 Core Generative AI & NLP (src/)
* **rag_pipeline.py** | Enterprise-grade RAG Architecture (Local LLM Integration + Optimized Vector Indexing).
* **agents_pipeline.py** | Production-validated Multi-Agent Task Orchestrator featuring intelligent semantic routing mechanisms powered by local Qwen instances.
* **pdf_summarizer_pipeline.py** | AI-Powered PDF Summarizer API for automated unstructured text extraction & abstractive summarization.
* **nlp_pipeline.py** | Classical NLP Text Classification API leveraging highly optimized statistical baselines (Naïve Bayes).
* **vector_pipeline.py & recommandation_pipeline.py** | Collaborative & Content-Based Product Recommendation API driven by fast Cosine Similarity matrices.

### 🛡️ API Security & Defensive Engineering (security/)
* **gateway_pipeline.py** | Advanced API Gateway serving as a secure Reverse-Proxy routing layer, featuring token verification, TLS/CORS configuration, and strict Pydantic v2 entry schemas.
* **guardrail_pipeline.py** | Production-validated LLM Safety Gate preventing malicious prompt injections (Jailbreaks) and infrastructure budget overruns via real-time token estimation.
* **secure_pipeline.py** | Secure AI Microservice Template managing robust API Key validation and CORS integration.
* **limiter_pipeline.py** | Production-validated Volumetric Network Protection shield implementing a sliding-window algorithm to drop abusive or raw DDoS traffic via HTTP 429 Too Many Requests blocks.
* **cors_pipeline.py** | Enterprise Network Isolation shield implementing granular Cross-Origin Resource Sharing.

### ⚡ Performance, Infrastructure & Databases
* **pipeline_21_batch_indexer.py** | High-throughput Async Document Ingestion Engine managing background processing worker queues for chunking and vector embeddings generation.
* **batch_pipeline.py** | Enterprise background processing architecture running secondary distributed inference tasks.
* **cache_pipeline.py** | Low-latency In-Memory Accelerator leveraging structural Redis layout layers.
* **database_pipeline.py** | Automated Relational Data Sync system driving text metadata and batch states persistence (`Queued`, `Processing`, `Completed`) via SQLAlchemy ORM and PostgreSQL/SQLite layouts.
* **webhook_pipeline.py** | Event-Driven Streaming Engine broadcasting real-time asynchronous notifications to connected webhooks.

## 🚀 Quick Start & Running Microservices Locally

### 1. Installation
```bash
git clone https://github.com
cd Portfolio-IA--Selection
pip install -r requirements.txt
```

### 2. Run the Pipelines with proper path mapping

#### Core GenAI Engines
```bash
uvicorn rag_pipeline:app --reload --port 8006
uvicorn agents_pipeline:app --reload --port 8007
uvicorn vector_pipeline:app --reload --port 8009
uvicorn pdf_summarizer_pipeline:app --reload --port 8005
```

#### Infrastructure, Core Gateway & Batch processing
```bash
uvicorn main:app --reload --port 8000
uvicorn gateway_pipeline:app --reload --port 8012
uvicorn batch_pipeline:app --reload --port 8011
uvicorn pipeline_21_batch_indexer:app --reload --port 8020
uvicorn cache_pipeline:app --reload --port 8013
```

#### Security Guardrails
```bash
uvicorn secure_pipeline:app --reload --port 8008
uvicorn cors_pipeline:app --reload --port 8014
uvicorn guardrail_pipeline:app --reload --port 8016
uvicorn limiter_pipeline:app --reload --port 8019
```

#### Databases, Streaming & Monitoring
```bash
uvicorn monitor_pipeline:app --reload --port 8010
uvicorn logging_pipeline:app --reload --port 8015
uvicorn database_pipeline:app --reload --port 8017
uvicorn webhook_pipeline:app --reload --port 8018
```

#### Analytics & Machine Learning
```bash
uvicorn churn_pipeline:app --reload --port 8011
uvicorn nlp_pipeline:app --reload --port 8012
uvicorn segmentation_pipeline:app --reload --port 8003
uvicorn recommandation_pipeline:app --reload --port 8004
```


