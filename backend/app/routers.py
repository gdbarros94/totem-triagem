from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
import httpx
import os
import json

router = APIRouter()

@router.post("/login")
def login(credentials: schemas.LoginRequest):
    # Mock de autenticação
    if credentials.username == "admin" and credentials.password == "admin":
        return {"access_token": "mock_token_123", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.get("/configuracoes/prompt", response_model=schemas.ConfiguracaoResponse)
def get_prompt(db: Session = Depends(database.get_db)):
    config = db.query(models.Configuracao).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    return config

@router.put("/configuracoes/prompt", response_model=schemas.ConfiguracaoResponse)
def update_prompt(config_update: schemas.ConfiguracaoUpdate, db: Session = Depends(database.get_db)):
    config = db.query(models.Configuracao).first()
    if not config:
        config = models.Configuracao(prompt_ia=config_update.prompt_ia)
        db.add(config)
    else:
        config.prompt_ia = config_update.prompt_ia
    db.commit()
    db.refresh(config)
    return config

@router.post("/atendimentos", response_model=schemas.AtendimentoResponse)
async def criar_atendimento(atendimento: schemas.AtendimentoCreate, db: Session = Depends(database.get_db)):
    # 1. Buscar o prompt atual
    config = db.query(models.Configuracao).first()
    prompt = config.prompt_ia if config else "Classifique a prioridade usando o protocolo de Manchester (Vermelho, Amarelo, Verde, Azul)."
    
    # 2. Comunicação com n8n (Síncrona para o cliente, mas assíncrona no FastAPI)
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    prioridade = "Verde" # Fallback
    resumo = atendimento.sintomas
    
    if webhook_url and webhook_url != "http://your-n8n-domain.com/webhook/triagem-ia":
        payload = {
            "prompt_ia": prompt,
            "paciente": atendimento.nome_paciente,
            "sintomas": atendimento.sintomas,
            "nivel_dor": atendimento.nivel_dor,
            "usou_libras": atendimento.usou_libras
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(webhook_url, json=payload, timeout=30.0)
                if response.status_code == 200:
                    data = response.json()
                    prioridade = data.get("prioridade", "Verde")
                    resumo = data.get("resumo", atendimento.sintomas)
                else:
                    print(f"Erro N8N HTTP: {response.status_code}")
        except Exception as e:
            print(f"Erro N8N Exception: {e}")

    # Limpar string da prioridade recebida ou setar fallback se for fora do escopo
    cores_validas = ["Vermelho", "Amarelo", "Verde", "Azul"]
    if prioridade not in cores_validas:
        prioridade = "Verde"

    # 3. Salvar no banco
    db_atendimento = models.Atendimento(
        nome_paciente=atendimento.nome_paciente,
        sintomas=resumo,
        nivel_dor=atendimento.nivel_dor,
        prioridade=prioridade,
        usou_libras=atendimento.usou_libras,
        senha="TEMP",
        status="aguardando"
    )
    db.add(db_atendimento)
    db.flush() # Para pegar o ID gerado imediatamente
    
    # 4. Gerar Senha
    inicial = prioridade[0].upper()
    db_atendimento.senha = f"{inicial}-{db_atendimento.id:03d}"
    
    db.commit()
    db.refresh(db_atendimento)
    
    return db_atendimento

@router.get("/atendimentos", response_model=list[schemas.AtendimentoResponse])
def listar_atendimentos(db: Session = Depends(database.get_db)):
    return db.query(models.Atendimento).order_by(models.Atendimento.data_hora.desc()).all()

@router.put("/atendimentos/{atendimento_id}", response_model=schemas.AtendimentoResponse)
def atualizar_status(atendimento_id: int, update_data: schemas.AtendimentoStatusUpdate, db: Session = Depends(database.get_db)):
    atendimento = db.query(models.Atendimento).filter(models.Atendimento.id == atendimento_id).first()
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    
    atendimento.status = update_data.status
    db.commit()
    db.refresh(atendimento)
    return atendimento
