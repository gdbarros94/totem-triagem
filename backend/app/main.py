from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from . import models, database
from .routers import router

load_dotenv()

def check_and_create_default_prompt(db):
    if not db.query(models.Configuracao).first():
        default_prompt = (
            "Você é o médico de triagem assistente. Avalie os sintomas do paciente usando "
            "o protocolo de Manchester. Retorne APENAS UM JSON no formato e chaves estritas: "
            "{\"prioridade\": \"C\", \"resumo\": \"S\"} onde C é uma destas strings EXACTAMENTE: (Vermelho, Amarelo, Verde, Azul) "
            "e S é um resumo otimizado clínico dos sintomas. A prioridade é baseada no nível de dor "
            "e perigosidade da queixa."
        )
        config = models.Configuracao(prompt_ia=default_prompt)
        db.add(config)
        db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria tabelas se não existirem
    models.Base.metadata.create_all(bind=database.engine)
    
    # Seed prompt padrão
    db = database.SessionLocal()
    try:
        check_and_create_default_prompt(db)
    finally:
        db.close()
    
    yield

app = FastAPI(title="Triagem Hospitaller MVP API", lifespan=lifespan)

origins_str = os.getenv("CORS_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
origins = [origin.strip() for origin in origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
