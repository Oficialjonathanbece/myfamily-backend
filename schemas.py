from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# --- ESQUEMAS DE COMENTARIOS ---
class CommentCreate(BaseModel):
    text: str
    author: Optional[str] = "Familiar"

class CommentResponse(BaseModel):
    id: int
    text: str
    author: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# --- ESQUEMAS DE NOTAS ---
class NoteCreate(BaseModel):
    content: str
    admin_code: str

class NoteResponse(BaseModel):
    id: int
    profile_slug: str
    content: str
    created_at: datetime
    comments: List[CommentResponse] = []  # Lista con todos los comentarios de la nota

    class Config:
        from_attributes = True


# --- ESQUEMA DE AUTENTICACIÓN ---
class LoginRequest(BaseModel):
    slug: str
    password: str