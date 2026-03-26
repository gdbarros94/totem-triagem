from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from .database import Base

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_paciente = Column(String, index=True)
    sintomas = Column(Text)
    nivel_dor = Column(Integer)
    prioridade = Column(String)  # Vermelho, Amarelo, Verde, Azul
    senha = Column(String, index=True)
    usou_libras = Column(Boolean, default=False)
    status = Column(String, default="aguardando") # aguardando, em_atendimento, finalizado
    data_hora = Column(DateTime, default=datetime.utcnow)

class Configuracao(Base):
    __tablename__ = "configuracoes"

    id = Column(Integer, primary_key=True, index=True)
    prompt_ia = Column(Text)
