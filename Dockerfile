# 1. Utiliser une image Python officielle et légère comme base
FROM python:3.11-slim

# 2. Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. Copier la liste des dépendances dans le conteneur
COPY requirements.txt .

# 4. Installer les bibliothèques sans garder de fichiers caches inutiles
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier le code de l'API de tri créé précédemment dans le conteneur
COPY api_tri.py .

# 6. Informer Docker que le conteneur écoutera sur le port 8000
EXPOSE 8000

# 7. Commande d'exécution pour démarrer l'API au lancement du conteneur
CMD ["uvicorn", "api_tri:app", "--host", "0.0.0.0", "--port", "8000"]
