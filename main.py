from sqlalchemy import text  # Adicione esta importação no início do seu arquivo
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Definir a URL do banco de dados MySQL (credenciais e nome do banco de dados)
DATABASE_URL = "mysql+pymysql://root:avela123@localhost/forum"

# Criação do motor que se conecta ao banco de dados
engine = create_engine(DATABASE_URL)

# Criação de uma sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para a definição dos modelos ORM
Base = declarative_base()

# Inicialização da aplicação FastAPI
app = FastAPI()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Nome de usuário único
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    user = relationship("User")
    topic = relationship("Topic")

# Rota principal para verificar se o serviço está funcionando
@app.get("/")
async def read_root():
    return {"message": "Bem-vindo ao Fórum!"}

# Rota para testar a conexão com o banco de dados
@app.get("/test-db")
async def test_db_connection():
    try:
        
        # Tentar criar uma sessão e consultar o banco de dados
        db = SessionLocal()
        # Apenas uma consulta simples para verificar a conexão
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Conexão com o banco de dados bem-sucedida!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco de dados: {str(e)}")
    finally:
        db.close()