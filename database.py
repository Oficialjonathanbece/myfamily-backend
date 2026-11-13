from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Usamos SQLite localmente para desarrollo rápido (creará un archivo family.db)
# Cuando pases a PostgreSQL en producción, solo cambias esta URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión de base de datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()