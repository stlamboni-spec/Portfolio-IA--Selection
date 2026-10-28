# 1. Image de base Python ultra-légère pour la production
FROM python:3.10-slim

# 2. Définition du dossier de travail dans le conteneur
WORKDIR /app

# 3. Installation des dépendances système nécessaires pour les calculs mathématiques lourds
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie de l'intégralité de vos 6 pipelines de production
COPY . .

# 6. Exposition du port réseau par défaut de FastAPI
EXPOSE 8000

# 7. Commande par défaut (Lance par défaut l'API principale de Credit Scoring)
# Note : Pour lancer un autre pipeline dans le Cloud, il suffira de surcharger cette commande.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
