from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AtendimentoCreate(BaseModel):
    nome_paciente: str
    sintomas: str
    nivel_dor: int
    usou_libras: bool = False

class AtendimentoResponse(BaseModel):
    id: int
    nome_paciente: str
    sintomas: str
    nivel_dor: int
    prioridade: str
    senha: str
    usou_libras: bool
    status: str
    data_hora: datetime

    class Config:
        from_attributes = True

class AtendimentoStatusUpdate(BaseModel):
    status: str

class ConfiguracaoUpdate(BaseModel):
    prompt_ia: str

class ConfiguracaoResponse(BaseModel):
    id: int
    prompt_ia: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
