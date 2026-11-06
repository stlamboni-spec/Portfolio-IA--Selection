import os
import logging
import asyncio
import warnings
from typing import List, Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

# Nettoyage des logs parasites de Hugging Face
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

# Configuration du Logger MLOps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Pipeline21_BatchIndexer")

app = FastAPI(
    title="Pipeline 21: Async Batch Embedding Extractor & Semantic Indexer",
    version="1.0.0"
)

# Modèles de données Pydantic v2
class DocumentInput(BaseModel):
    doc_id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChunkOutput(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    real_embedding: List[float]

# Initialisation globale du modèle (all-MiniLM-L6-v2)
logger.info("Loading semantic embedding model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
logger.info("Model loaded successfully. Pipeline 21 Ready.")

class BatchIndexerEngine:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    async def extract_chunks(self, document: DocumentInput) -> List[Dict[str, Any]]:
        text = document.content
        chunks = []
        start = 0
        chunk_idx = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            chunks.append({
                "chunk_id": f"{document.doc_id}_chunk_{chunk_idx}",
                "doc_id": document.doc_id,
                "text": chunk_text
            })
            start += (self.chunk_size - self.overlap)
            chunk_idx += 1
            await asyncio.sleep(0.001)
        return chunks

    async def compute_embeddings(self, chunks: List[Dict[str, Any]]) -> List[ChunkOutput]:
        texts_to_embed = [chunk["text"] for chunk in chunks]
        
        # Exécution du modèle IA dans un exécuteur pour ne pas bloquer FastAPI
        loop = asyncio.get_running_loop()
        embeddings = await loop.run_in_executor(None, embedding_model.encode, texts_to_embed)
        
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            processed_chunks.append(
                ChunkOutput(
                    chunk_id=chunk["chunk_id"],
                    doc_id=chunk["doc_id"],
                    text=chunk["text"],
                    real_embedding=embeddings[i].tolist()
                )
            )
        return processed_chunks

# --- POINTS DE TERMINAISON API (ENDPOINTS) ---

@app.get("/health")
async def health_check():
    return {"status": "healthy", "pipeline": "Pipeline 21 Async Batch Indexer"}

@app.post("/index/batch", response_model=List[ChunkOutput])
async def process_batch_indexing(documents: List[DocumentInput]):
    """Endpoint pour exécuter l'extraction et la vectorisation sémantique par lots."""
    if not documents:
        raise HTTPException(status_code=400, detail="Document list cannot be empty.")
    
    try:
        engine = BatchIndexerEngine(chunk_size=300, overlap=30)
        
        # 1. Extraction asynchrone des morceaux
        tasks = [engine.extract_chunks(doc) for doc in documents]
        extracted_results = await asyncio.gather(*tasks)
        
        all_chunks = []
        for result in extracted_results:
            all_chunks.extend(result)
            
        if not all_chunks:
            return []
            
        # 2. Calcul des embeddings sémantiques réels
        results = await engine.compute_embeddings(all_chunks)
        logger.info(f"Successfully processed batch: {len(results)} chunks embedded.")
        return results
        
    except Exception as e:
        logger.error(f"Error during batch indexing pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during indexing.")
