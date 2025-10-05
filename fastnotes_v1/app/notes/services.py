from app.db.config import async_session
from app.notes.models import Note
from sqlalchemy import select
from fastapi import HTTPException

async def create_note(title: str, content: str):
    async with async_session() as session:
      note = Note(title=title, content=content)
      session.add(note)
      await session.commit()
      await session.refresh(note)
      return note
    
async def get_note(note_id: int):
    async with async_session() as session:
      note = await session.get(Note, note_id)
      if note is None:
          raise HTTPException(status_code=404, detail="Not not found")
      return note
    
async def get_all_notes():
    async with async_session() as session:
      stmt = select(Note)
      notes = await session.scalars(stmt)
      return notes.all()
    
async def update_note(note_id: int, new_title: str, new_content: str):
    async with async_session() as session:
      note = await session.get(Note, note_id)
      if note is None:
          raise HTTPException(status_code=404, detail="Not not found")
      note.title = new_title
      note.content = new_content
      await session.commit()
      await session.refresh(note)
      return note
    
async def patch_note(note_id: int, new_title: str | None = None, new_content: str | None = None):
    async with async_session() as session:
        note = await session.get(Note, note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Not not found")

        if new_title is not None:
            note.title = new_title
        if new_content is not None:
            note.content = new_content

        await session.commit()
        await session.refresh(note)
        return note
    
async def delete_note(note_id: int):
    async with async_session() as session:
      note = await session.get(Note, note_id)
      if note is None:
          raise HTTPException(status_code=404, detail="Not not found")
      await session.delete(note)
      await session.commit()
      return {"message": "deleted"}