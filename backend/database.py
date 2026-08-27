from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Definimos que la base de datos será un archivo local llamado lifestyle.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./lifestyle.db"

# 2. Creamos el motor de conexión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Definimos nuestro primer Modelo de Datos (La tabla 'tareas')
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    contenido = Column(String, nullable=True)  # <-- ESTA ES LA LÍNEA NUEVA
    dominio = Column(String)
    estado = Column(String, default="pendiente")