from pydantic import BaseModel

class CreateNote(BaseModel):
    title: str
    body: str

class EditNote(BaseModel):
    id: str
    title: str
    body: str

class GetAllNotes(BaseModel):
    take: int
    skip: int
    search: str = None