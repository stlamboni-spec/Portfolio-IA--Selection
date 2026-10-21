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
## 🛠️ Compétences d'Ingénierie Validées
Au-delà des modèles, ce portfolio démontre une capacité robuste à résoudre des problématiques d'infrastructure et de production :
1. **Gestion du Matériel :** Allocation dynamique des tenseurs sur GPU via `torch.device("cuda")` et parallélisation des calculs matriciels.
2. **Interopérabilité des Frameworks :** Résolution des conflits de formats de poids (sauvegardes TensorFlow vs instanciations PyTorch) et gestion des structures de dictionnaires d'états (`.state_dict()`).
3. **Persistance des Données :** Exportation et sérialisation des modèles entraînés (fichiers `.pth` et dossiers `.save_pretrained()`) pour des déploiements ultérieurs.

---

## 💻 Comment exécuter les projets
1. Ouvrez un environnement **Google Colab** ou une instance Jupyter locale disposant d'un GPU.
2. Clonez ce dépôt.
3. Installez les dépendances :
   ```bash
   pip install torch torchvision transformers ipywidgets pillow
   ```
4. Exécutez les notebooks pas à pas.
