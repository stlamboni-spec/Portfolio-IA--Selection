import io
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from pypdf import PdfReader
from transformers import pipeline

# 1. Initialisation de l'API pour le Pipeline 15
app = FastAPI(
    title="Pipeline 15 : AI-Powered PDF Summarizer Microservice",
    description="API MLOps d'extraction de texte et de résumé automatique de fichiers PDF via le LLM Qwen.",
    version="1.0.0"
)

print("🧠 Chargement du modèle de génération textuelle open-source (Qwen-0.5B-Chat)...")
# Initialisation industrielle conforme aux standards de l'écosystème Transformers v5
generator = pipeline("text-generation", model="Qwen/Qwen1.5-0.5B-Chat")
print("✅ Modèle LLM prêt pour la production !")

# 2. Endpoint de traitement et résumé de PDF
@app.post("/summarize_pdf", summary="Extraire et résumer le contenu d'un document PDF")
async def resumer_pdf(file: UploadFile = File(..., description="Le fichier PDF à analyser")):
    try:
        # Validation défensive du format de fichier
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Le format de fichier est invalide. Seuls les documents .pdf sont acceptés.")
            
        # Lecture binaire sécurisée en mémoire
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)
        reader = PdfReader(pdf_file)
        
        # Extraction itérative des caractères textuels
        texte_extrait = ""
        for page in reader.pages:
            texte_page = page.extract_text()
            if texte_page:
                texte_extrait += texte_page + "\n"
                
        if not texte_extrait.strip():
            raise HTTPException(
                status_code=400, 
                detail="Échec de l'extraction : le document PDF ne contient aucun texte exploitable (document vide ou scanné sous forme d'image)."
            )
            
        # Application du Chat Template d'instructions (Transformers v5)
        messages = [
            {
                "role": "user",
                "content": f"Summarize the following text into one clear and concise paragraph:\n\n{texte_extrait[:1000]}"
            }
        ]
        
        # Inférence LLM déterministe (sans échantillonnage aléatoire pour garantir la stabilité bancaire)
        outputs = generator(messages, max_new_tokens=150, do_sample=False)
        texte_resume = outputs["generated_text"][-1]["content"]
        
        return {
            "filename": file.filename,
            "status": "success",
            "extracted_characters": len(texte_extrait),
            "pdf_summary": texte_resume.strip()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'infrastructure LLM : {str(e)}")
