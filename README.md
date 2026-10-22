# 🚀 Portfolio IA : NLP, Computer Vision & Modèles Multimodaux

Ce dépôt rassemble les codes sources et l'architecture de **3 projets concrets d'Intelligence Artificielle** développés en autonomie suite à l'interruption de ma formation théorique initiale. L'objectif était de passer de la théorie (Machine Learning / Deep Learning) à la pratique industrielle en domptant l'écosystème **PyTorch**, **Hugging Face**, et l'accélération matérielle sur **GPU NVIDIA (CUDA)**.

---

## 🗳️ Projet 1 : Observatoire de Réputation Électorale (NLP)
### Description
Développement d'un classificateur d'avis et de messages politiques (Analyse de sentiments) capable de traiter des flux textuels en anglais et en français.

### Technologies & Architecture
* **Modèles de base :** `distilbert-base-uncased-finetuned-sst-2-english` (Anglais) et `nlptown/bert-base-multilingual-uncased-sentiment` (Français).
* **Concepts clés :** Tokenisation (Subword tokens, Attention Masks, Padding), extraction de la représentation contextuelle via le token spécial `[CLS]`, et manipulation des *Logits* en sortie.
* **Interface :** Widgets interactifs intégrés (`ipywidgets`) s'exécutant directement en mémoire GPU.

---

## ♻️ Projet 2 : Tri Automatique des Déchets industriels (Computer Vision)
### Description
Système de vision industrielle par ordinateur conçu pour trier automatiquement des objets défilant sur un tapis roulant vers 4 bacs distincts : Plastique, Verre, Carton, ou Métal.

### Technologies & Architecture
* **Framework :** PyTorch & Torchvision.
* **Méthodologie :** **Transfer Learning** basé sur l'architecture étatique **ResNet50**.
* **Technique :** Gel des poids des couches convolutives inférieures (*Weight Freezing*) pour conserver l'extraction de caractéristiques visuelles universelles, et remplacement/entraînement exclusif de la tête de classification linéaire supérieure (`nn.Linear`).
* **Optimisation :** Génération de données matricielles en mémoire vive pour maximiser l'usage de la bande passante du GPU Tesla T4 et éliminer les goulets d'étranglement réseau.

---

## 📸 Projet 3 : Générateur Multimodal de Légendes (Image-to-Text)
### Description
Une application hybride combinant la Vision et le Traitement du Langage Naturel pour forcer une IA à comprendre la géométrie d'une image et à en rédiger une description textuelle humaine exacte.

### Technologies & Architecture
* **Modèle :** Architecture pré-entraînée **BLIP** (*Bootstrapped Language-Image Pre-training*) de Salesforce hébergée sur le Hub Hugging Face.
* **Pipeline :** Synthèse d'images géométriques via la bibliothèque *PIL (Pillow)* transmises à un `BlipProcessor` pour la normalisation des pixels, suivies d'une génération autoregressive de tokens textuels décodés en langage naturel.

---## 📊 Projets de Machine Learning Traditionnel
### Description
Implémentation d'algorithmes de Machine Learning pour la prédiction et la classification de données tabulaires structurées.

### Technologies & Algorithmes
* **Librairies :** Scikit-Learn, Pandas, NumPy, Matplotlib.
* **Modèles entraînés :** Régression Logistique,Bayes Naive; Arbres de décision: Random Forest, et algorithmes de Boosting (XGBoost/LightGBM), ID3, CART,C4.5; K-Mean, ACP
* **Concepts clés :** Nettoyage des données (Missing values), encodage des variables catégorielles (One-Hot Encoding), feature engineering, et évaluation des performances (Matrice de confusion, score F1, courbe ROC).
## 📊 Projets de Machine Learning Traditionnel
### 📧 1. Filtre Anti-Spam Automatique
*   **Objectif :** Classifier automatiquement les emails ou messages reçus en deux catégories : "Spam" ou "Ham" (message légitime).
*   **Algorithmes & Tech :** Scikit-Learn, Naive Bayes (MultinomialNB), Régression Logistique.
*   **Concepts clés :** Prétraitement du texte (Stopwords, lemmatisation), vectorisation textuelle (*TF-IDF* / *CountVectorizer*), et optimisation de la précision pour éviter les faux positifs (un message important classé en spam).

### ✈️ 2. Prédiction de Retards de Vols (Météo & Trafic)
*   **Objectif :** Prédire si un vol aérien va subir un retard en fonction des caractéristiques temporelles et des conditions météorologiques du jour.
*   **Algorithmes & Tech :** Pandas, Random Forest Regressor/Classifier, XGBoost, Matplotlib pour la visualisation.
*   **Concepts clés :** Fusion de datasets (données de vols + données météo), gestion du déséquilibre des classes (*Imbalanced Data*), encodage des variables catégorielles (compagnies, aéroports), et analyse de l'importance des variables (*Feature Importance*).
  ---

## 🤖 Projet 4 : Système RAG Autonome (Retrieval-Augmented Generation)
### Description
Conception d'une architecture RAG permettant à un grand modèle de langage (LLM) de répondre précisément à des questions complexes en s'appuyant exclusivement sur une base de connaissances d'entreprise confidentielle, sans risque d'hallucination.

### Technologies & Architecture
* **Orchestrateur :** `LangChain` (pipelines d'interconnexion de données).
* **Base de données vectorielle :** `ChromaDB` (stockage local des embeddings et recherche de similarité cosinus).
* **Embeddings :** `sentence-transformers/all-MiniLM-L6-v2` s'exécutant sur GPU pour la vectorisation sémantique des blocs de texte (*Chunking*).
* **LLM local :** `facebook/opt-350m` (Pipeline d'inférence causale hautement optimisé pour l'extraction de faits contextuels en VRAM).
---

## 🚀 Projet 5 : Microservice d'Inférence IA en Production (FastAPI)
### Description
Encapsulation industrielle du modèle de Vision par Ordinateur (ResNet50) sous forme d'API REST Web hautement performante. Cette architecture découplée permet à n'importe quelle application tierce (Web, Mobile, Automate industriel) d'interroger le modèle d'IA et de recevoir une décision de tri instantanée.

### Technologies & Architecture
* **Framework Web :** `FastAPI` (Asynchronous Server Gateway Interface orienté haute performance).
* **Serveur de Production :** `Uvicorn` (implémentation de serveur web de production exécutée en tâche de fond Linux).
* **Validation des Données :** `Pydantic` (sécurisation et typage strict des structures de données JSON entrantes via la classe `ImageMetadata`).
* **Pipeline d'Inférence :** Passage automatique du modèle PyTorch en mode d'évaluation sécurisé (`model.eval()`) avec désactivation du calcul des gradients (`torch.no_grad()`) pour diviser le temps de latence par 10 sur GPU CUDA.

  ---

## 🤖 Projet 6 : Pipeline Automatisé de Support Client Hybride (FastAPI & Inférence Couplée)
### Description
Conception d'un microservice de support client autonome. L'API reçoit les réclamations des utilisateurs, analyse en temps réel la tonalité sémantique du message (classification NLP) et génère de façon dynamique une proposition de réponse ciblée (génération générative LLM).

### Technologies & Architecture
* **Analyse de Sentiment :** `BERT Multilingual` finetuné, extrayant précisément les structures sémantiques négatives et positives.
* **Moteur Génératif :** `facebook/opt-350m` piloté par du *Prompt Conditioning* dynamique selon la classification en amont.
* **Industrialisation :** Encapsulation asynchrone dans une architecture `FastAPI` validée par des tests unitaires d'intégration via `TestClient`.

  ---

## 🤖 Projet 7 : Architecture RAG Orientée Routage Intelligent (FastAPI & Hybridation NLP/LLM)
### Description
Conception d'un système de support e-commerce avancé combinant une classification de sentiment en amont et un moteur de recherche documentaire dynamique (RAG) en aval. Pour optimiser les ressources de calcul GPU, le système n'interroge la base de connaissances d'entreprise que si le message utilisateur est classé comme négatif.

### Technologies & Architecture
* **Routage sémantique :** Pipeline `BERT` aiguillant dynamiquement les requêtes selon la tonalité émotionnelle détectée.
* **Extraction contextuelle (RAG) :** Indexation de la politique de l'entreprise dans une base vectorielle `ChromaDB` à l'aide d'embeddings `sentence-transformers`.
* **Génération conditionnée :** Injection exclusive de la règle extraite dans le prompt du LLM `OPT-350m` pour garantir des réponses d'excuses conformes aux directives de l'entreprise et sans hallucinations.
  
## 🛠️ Compétences d'Ingénierie Validées
Au-delà des modèles, ce portfolio démontre une capacité robuste à résoudre des problématiques d'infrastructure et de production :
1. **Gestion du Matériel :** Allocation dynamique des tenseurs sur GPU via `torch.device("cuda")` et parallélisation des calculs matriciels.
2. **Interopérabilité des Frameworks :** Résolution des conflits de formats de poids (sauvegardes TensorFlow vs instanciations PyTorch) et gestion des structures de dictionnaires d'états (`.state_dict()`).
3. **Persistance des Données :** Exportation et sérialisation des modèles entraînés (fichiers `.pth` et dossiers `.save_pretrained()`) pour des déploiements ultérieurs.

--------

## 📊 Projet 9 : Segmentation Sémantique des Clients (Apprentissage Non Supervisé RFM)
### Description
Développement d'un pipeline complet de Data Science permettant de regrouper automatiquement la base de données clients d'une entreprise en segments homogènes, sans aucune étiquette préalable. Ce système permet aux équipes marketing de cibler précisément leurs campagnes.

### Technologies & Architecture
* **Ingénierie de caractéristiques :** Agrégation de données brutes de vente pour calculer les indicateurs pivots **RFM** (*Récence, Fréquence, Montant*).
* **Prétraitement :** Normalisation standard (`StandardScaler`) pour éliminer les biais d'échelle lors du calcul des distances Euclidiennes.
* **Algorithme de Clustering :** Implémentation du modèle `K-Means` (Scikit-Learn) pour la classification géométrique des données.
* **Profilage Métier :** Analyse automatique des centroïdes des clusters pour traduire les groupes mathématiques en profils stratégiques exploitables (*VIP, Clients dormants, Clients réguliers*).-

## 📦 Brique MLOps : Conteneurisation & Industrialisation (Docker)
### Description
Mise en place d'une infrastructure de déploiement continu pour isoler le microservice d'inférence et garantir une réplication stricte de l'environnement de calcul sur n'importe quel cluster Cloud (AWS, GCP, Azure).

### Technologies & Configuration
* **Conteneurisation :** `Dockerfile` basé sur une distribution Linux alpine légère (`python:3.11-slim`).
* **Gestion des dépendances :** Figeage des versions logicielles majeures (`torch`, `torchvision`, `fastapi`, `uvicorn`) dans un fichier `requirements.txt` avec exclusion des caches pour optimiser le poids de l'image.
* **Orchestration de production :** Configuration du point d'entrée réseau sur le port `8000` (`EXPOSE`) et automatisation du lancement asynchrone via l'exécuteur de processus d'arrière-plan de l'image.
---

## 💳 Projet 8 : Microservice d'Interception des Fraudes Bancaires (FastAPI & Random Forest)
### Description
Développement d'un système de détection des fraudes financières en temps réel pour le secteur bancaire/fintech. L'API intercepte les flux de métadonnées des transactions par carte de crédit, valide les types de données via des contraintes de sécurité strictes et applique un modèle d'apprentissage supervisé pour bloquer instantanément les anomalies.

### Technologies & Architecture
* **Modèle Prédictif :** Algorithme de classification `Random Forest` (Scikit-Learn) évaluant les corrélations sémantiques entre les montants, les distances géographiques et la récurrence des transactions.
* **Sécurité des Données :** Utilisation de `Pydantic Fields` pour implémenter un filtrage défensif empêchant l'injection de montants négatifs ou de valeurs aberrantes.
* **Format de Production :** Restitution de scores probabilistes précis (`predict_proba`) encapsulés dans un format universel JSON standardisé pour les serveurs d'autorisation bancaire.
  

---

## 💻 Comment exécuter les projets

Pour tester et exécuter l'ensemble des modules de ce portfolio, deux modes d'implémentation sont mis à disposition :

### Option 1 : Inférence rapide via Google Colab / Jupyter
1. Ouvrez un environnement **Google Colab** et activez l'accélération matérielle **GPU Tesla T4** (Menu *Exécuter > Modifier le type d'exécution > GPU*).
2. Téléchargez ou clonez le fichier global `.ipynb` de ce dépôt.
3. Installez l'intégralité des dépendances industrielles requises en exécutant la commande suivante dans votre première cellule :
   ```bash
   pip install torch torchvision transformers langchain-huggingface langchain-chroma langchain-text-splitters fastapi uvicorn pydantic requests scikit-learn pillow nest-asyncio
   ```
4. Exécutez les cellules pas à pas pour lancer les serveurs locaux, les tests unitaires via `TestClient` et les architectures RAG.

### Option 2 : Déploiement Industriel MLOps (Docker)
Pour isoler et déployer le microservice de production sur n'importe quel serveur Cloud :
1. Assurez-vous que **Docker** est installé sur votre machine.
2. Placez-vous dans le dossier racine contenant les livrables et lancez la construction de l'image conteneurisée :
   ```bash
   docker build -t portfolio-ia-service:v1 .
   ```
3. Déployez et lancez instantanément le conteneur asynchrone sur le port réseau de production `8000` :
   ```bash
   docker run -d -p 8000:8000 --gpus all portfolio-ia-service:v1
   ```
