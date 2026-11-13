from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Crear las tablas en la base de datos automáticamente al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Family Backend", version="1.0.0")

# --- CONFIGURACIÓN DE CORS ---
# Permite que tu frontend (tanto en local como en Vercel) se conecte al backend
origins = [
    "http://localhost:3000",
    "https://myfamily-xi-seven.vercel.app/",  # Cambia esto por tu URL real de Vercel cuando la tengas
    "*" # Opcional: permite cualquier origen temporalmente para pruebas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CLAVES PROTEGIDAS EN EL SERVIDOR ---
# Ahora las contraseñas viven aquí de forma segura y no en el navegador
CLAVES_FAMILIARES = {
    "sebastian-the-best-friend-in-the-world": "1234",
    "maria-gladis": "1234",
    "mary-luz-becerra": "1234",
    "fernando-rodriguez": "1234",
    "luis-david-macuare": "1234",
    "mileida-ortiz": "1234",
    "flor-maria": "1234",
    "daniela-giraldo": "1234",
    "david-esposo-de-daniela": "1234",
    "danna-giraldo": "1234",
    "brayan-esposo-de-danna": "1234",
    "salome-y-emmanuel": "1234",
    "hanna": "1234",
    "fernanda-becerra": "1234",
    "wesly": "1234",
    "jesus-esposo-de-fernanda": "1234",
    "edinson-viera": "1234",
    "cristian-y-jenifer": "1234",
    "padrino": "1234",
    "madrina": "1234",
    "yese": "1234",
    "shelsy-sofia": "1234",
    "oscar-humberto-aristizabal": "1234",
    "rosmary-alejandra-pena-ramos": "1234",
    "familiares": "1234"
}

SPECIAL_ADMIN_CODE = "9876"  # Código exclusivo para crear notas


# --- 1. ENDPOINT DE AUTENTICACIÓN ---
@app.post("/api/auth/login")
def login_profile(data: schemas.LoginRequest):
    slug_lower = data.slug.lower()
    
    if slug_lower not in CLAVES_FAMILIARES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado."
        )
    
    if CLAVES_FAMILIARES[slug_lower] != data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clave incorrecta."
        )
    
    return {"success": True, "message": "Acceso autorizado"}


# --- 2. OBTENER NOTAS DE UN PERFIL ---
@app.get("/api/notes/{slug}", response_model=List[schemas.NoteResponse])
def get_notes_by_slug(slug: str, db: Session = Depends(get_db)):
    notes = db.query(models.NoteModel).filter(models.NoteModel.profile_slug == slug.lower()).all()
    return notes


# --- 3. CREAR NUEVA NOTA (Protegida por código admin) ---
@app.post("/api/notes/{slug}", response_model=schemas.NoteResponse)
def create_note(slug: str, note_data: schemas.NoteCreate, db: Session = Depends(get_db)):
    # Validar el código de administración en el servidor
    if note_data.admin_code != SPECIAL_ADMIN_CODE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Código de administración incorrecto."
        )

    new_note = models.NoteModel(
        profile_slug=slug.lower(),
        content=note_data.content
    )
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


# --- 4. AGREGAR COMENTARIO A UNA NOTA (Soporta múltiples comentarios) ---
@app.post("/api/notes/{note_id}/comments", response_model=schemas.CommentResponse)
def add_comment_to_note(note_id: int, comment_data: schemas.CommentCreate, db: Session = Depends(get_db)):
    # Verificar si la nota existe
    note = db.query(models.NoteModel).filter(models.NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La nota especificada no existe."
        )

    new_comment = models.CommentModel(
        note_id=note_id,
        text=comment_data.text,
        author=comment_data.author
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment