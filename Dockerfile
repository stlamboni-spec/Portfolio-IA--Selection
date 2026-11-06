# Image de base légère et optimisée pour Python
FROM python:3.11-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'intégralité des scripts de l'application
COPY . .

# Création d'un utilisateur non-privilégié pour la sécurité en production Cloud
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Exposition du port de l'API FastAPI
EXPOSE 8000

# Commande de lancement de l'application principale via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
