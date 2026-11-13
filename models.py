from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    profile_slug = Column(String, index=True, nullable=False)  # Ej: 'mary-luz'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación 1 a Muchos: Una nota puede tener múltiples comentarios
    comments = relationship("CommentModel", back_populates="note", cascade="all, delete-orphan")


class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    author = Column(String, nullable=True)  # Nombre del familiar que escribe
    created_at = Column(DateTime, default=datetime.utcnow)

    note = relationship("NoteModel", back_populates="comments")