import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.metrics.pairwise import cosine_similarity

# 1. Initialisation de l'API pour le Pipeline 14
app = FastAPI(
    title="Pipeline 14 : Product Recommendation Microservice",
    description="API MLOps de recommandation de produits basée sur le calcul de similitude de cosinus.",
    version="1.0.0"
)

# 2. Schéma de données avec Typage Défensif (Pydantic v2)
class DemandeRecommandation(BaseModel):
    client_id: str = Field(..., example="CLIENT_ECOM_55")
    historique_achats: list[int] = Field(
        ..., 
        description="Vecteur binaire (0 ou 1) représentant l'achat des produits [Tech, Mode, Maison, Livres]",
        example=[1, 0, 0, 1]
    )

# 3. Matrice de données historiques d'achat reconstruite de manière ultra-sécurisée
donnees_brutes = "1,0,1,0;0,1,0,1;1,1,0,0;0,0,1,1"
lignes = [list(map(int, x.split(","))) for x in donnees_brutes.split(";")]
base_clients_matrix = np.array(lignes)

catalogue_produits = {
    0: "Ordinateur portable Pro 💻",
    1: "Veste en jean tendance 🧥",
    2: "Lampe de bureau LED connectée 💡",
    3: "Livre Best-Seller Business 📚"
}

# 4. Endpoint de recommandation
@app.post("/recommend", summary="Calculer des recommandations personnalisées")
def recommander_produits(donnees: DemandeRecommandation):
    try:
        if len(donnees.historique_achats) != 4:
            raise HTTPException(status_code=400, detail="Le vecteur d'historique doit contenir exactement 4 éléments.")
            
        user_vector = np.array([donnees.historique_achats])
        
        # Calcul mathématique de la similitude de Cosinus
        similarites = cosine_similarity(user_vector, base_clients_matrix)
        client_le_plus_proche = int(np.argmax(similarites))
        
        profil_cible = base_clients_matrix[client_le_plus_proche]
        recommandations = []
        
        for idx, de_ja_achete in enumerate(donnees.historique_achats):
            if de_ja_achete == 0 and profil_cible[idx] == 1:
                recommandations.append(catalogue_produits.get(idx, "Produit mystère ✨"))
                
        if not recommandations:
            recommandations.append("Carte cadeau Premium Upwork 🎁 (Découvrez de nouvelles catégories !)")
            
        return {
            "client_id": donnees.client_id,
            "matched_historical_profile_id": client_le_plus_proche,
            "similarity_score": round(float(similarites[0, client_le_plus_proche]), 2),
            "recommended_products": recommandations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur du système de recommandation : {str(e)}")
