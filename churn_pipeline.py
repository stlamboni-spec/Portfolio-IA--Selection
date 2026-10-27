import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestClassifier

# 1. Initialisation de l'API pour le Pipeline 11
app = FastAPI(
    title="Pipeline 11 : Customer Churn Prediction Microservice",
    description="API MLOps pour prédire l'attrition client à l'aide d'un modèle de Gradient Boosting / Random Forest.",
    version="1.0.0"
)

# 2. Schéma de données avec Typage Défensif (Pydantic v2)
class DemandeChurn(BaseModel):
    client_id: str = Field(..., example="CLIENT_TELCO_45")
    anciennete_mois: int = Field(..., description="Nombre de mois d'abonnement", example=18)
    facturation_mensuelle: float = Field(..., description="Montant de la facture en euros", example=45.5)
    reclamations_3_mois: int = Field(..., description="Nombre de réclamations récentes", example=2)

# 3. Entraînement initial d'un modèle d'arbre décisionnel (Random Forest)
# Données historiques simulées : [Ancienneté, Facture, Réclamations]
X_train = np.array([
    [36, 20.0, 0],  # Client fidèle
    [3, 85.0, 3],   # Client très propice au churn
    [12, 40.0, 1],  # Client moyen fidèle
    [6, 65.0, 2]    # Client risqué
])
y_train = np.array([0, 1, 0, 1])  # 0 = Reste, 1 = Churn (Quitte l'entreprise)

model_churn = RandomForestClassifier(n_estimators=50, random_state=42)
model_churn.fit(X_train, y_train)

# 4. Endpoint de prédiction du Churn
@app.post("/predict_churn", summary="Prédire le risque de départ d'un client")
def predire_churn(donnees: DemandeChurn):
    try:
        # Formatage des caractéristiques d'entrée
        features = [[
            donnees.anciennete_mois,
            donnees.facturation_mensuelle,
            donnees.reclamations_3_mois
        ]]
        
        # Calcul de la probabilité de churn
        prediction = int(model_churn.predict(features))
        probabilites = model_churn.predict_proba(features)
        probabilite_churn = float(probabilites[:, 1])
        
        # Logique métier d'alerte pour l'équipe Customer Success
        if probabilite_churn > 0.50:
            alerte = "CRITIQUE ⚠️"
            action = "Déclencher une offre de rétention immédiatement"
        else:
            alerte = "STABLE ✅"
            action = "Aucune action requise - Client satisfait"
            
        return {
            "client_id": donnees.client_id,
            "churn_risk_status": alerte,
            "churn_probability": round(probabilite_churn * 100, 2),  # Pourcentage
            "recommended_action": action
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'inférence Churn : {str(e)}")
