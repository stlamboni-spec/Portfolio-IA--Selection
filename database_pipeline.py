from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. CONFIGURATION DE LA BASE DE DONNÉES DE PRODUCTION (SQLAlchemy ORM)
DATABASE_URL = "sqlite:///./ia_portfolio.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogInferenceSQL(Base):
    __tablename__ = "inference_history"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    response = Column(String)
    tokens_used = Column(Integer)
    cost_usd = Column(Float)

# Création automatisée des schémas de tables
Base.metadata.create_all(bind=engine)

# 2. INITIALISATION DU MICROSERVICE
app = FastAPI(
    title="Pipeline 18 : Automated Database Schema Sync Microservice",
    description="Microservice gérant la persistance de l'historique d'inférence au sein d'une base de données relationnelle via SQLAlchemy.",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Version corrigée conforme Pydantic v2 (Zéro Warning)
class PromptPayload(BaseModel):
    user_prompt: str = Field(
        ..., 
        json_schema_extra={"example": "Analyse foncière à Lomé"}
    )

@app.post("/inference_persistent", summary="Exécuter l'inférence et persister les structures de données en base SQL")
def executer_et_sauvegarder(payload: PromptPayload, db: Session = Depends(get_db)):
    try:
        simulated_output = f"Analyse persistée pour : '{payload.user_prompt}'"
        tokens = len(payload.user_prompt.split()) + 15
        cost = round(tokens * 0.000015, 6)
        
        nouvel_enregistrement = LogInferenceSQL(
            prompt=payload.user_prompt,
            response=simulated_output,
            tokens_used=tokens,
            cost_usd=cost
        )
        
        db.add(nouvel_enregistrement)
        db.commit()
        db.refresh(nouvel_enregistrement)
        
        return {
            "status": "SUCCESS_DATA_PERSISTED",
            "database_row_id": nouvel_enregistrement.id,
            "saved_record": {
                "prompt": nouvel_enregistrement.prompt,
                "response": nouvel_enregistrement.response,
                "tokens_used": nouvel_enregistrement.tokens_used,
                "cost_usd": nouvel_enregistrement.cost_usd
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Crash: {str(e)}")
