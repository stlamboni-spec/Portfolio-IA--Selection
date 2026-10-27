import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.cluster import KMeans

# 1. Initialisation de l'API pour le Pipeline 13
app = FastAPI(
    title="Pipeline 13 : Customer Segmentation Microservice",
    description="API MLOps pour la segmentation comportementale des clients à l'aide de l'algorithme K-Means.",
    version="1.0.0"
)

# 2. Schéma de données avec Typage Défensif
class DemandeSegmentation(BaseModel):
    client_id: str = Field(..., example="CLIENT_RETAIL_102")
    achats_annuels: int = Field(..., description="Nombre total de commandes passées à l'année", example=25)
    panier_moyen: float = Field(..., description="Montant moyen dépensé par commande en euros", example=120.0)

# 3. Entraînement avec des profils de données mieux espacés
X_train = np.array([
    [2, 15.0],    # Cluster 0 : Occasionnel
    [30, 150.0],  # Cluster 1 : VIP / Premium
    [3, 140.0],   # Cluster 2 : Gros Dépensier Rare
    [18, 30.0]    # Cluster 3 : Chasseur de Bons Plans
])

# Fixation des centres initiaux pour garantir un clustering stable et prévisible
model_kmeans = KMeans(n_clusters=4, init=X_train, n_init=1, random_state=42)
model_kmeans.fit(X_train)

# 4. Endpoint de prédiction du cluster
@app.post("/segment_client", summary="Attribuer un segment marketing à un client")
def segmenter_client(donnees: DemandeSegmentation):
    try:
        features = [[donnees.achats_annuels, donnees.panier_moyen]]
        
        # Correction de l'avertissement : extraction de la valeur brute du tableau
        raw_prediction = model_kmeans.predict(features)
        cluster_id = int(raw_prediction[0])
        
        profils_marketing = {
            0: {"nom": "Client Occasionnel 🛋️", "strategie": "Campagne de réengagement et coupons de réduction"},
            1: {"nom": "Client VIP / Premium 💎", "strategie": "Accès exclusif aux nouveautés et programme de fidélité Gold"},
            2: {"nom": "Gros Dépensier Rare 🎯", "strategie": "Offres ciblées sur des produits haut de gamme"},
            3: {"nom": "Chasseur de Bons Plans 🏷️", "strategie": "Promotions flash et déstockage personnalisé"}
        }
        
        segment_attribue = profils_marketing.get(cluster_id, {"nom": "Indéterminé", "strategie": "Analyse manuelle"})
        
        return {
            "client_id": donnees.client_id,
            "assigned_cluster_id": cluster_id,
            "marketing_segment_name": segment_attribue["nom"],
            "recommended_marketing_strategy": segment_attribue["strategie"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de segmentation : {str(e)}")
