from fastapi import APIRouter, HTTPException
from models.models import *
from datetime import datetime
import math
import uuid

router = APIRouter()

notes_list = []

@router.post('/get-notes')
async def get_all_notes(req: GetAllNotes):
    errors = []
    if req.take <= 0:
        errors.append('take_field_cannot_be_equal_to_or_less_than_0')
    if req.skip < 0:
        errors.append('skip_field_cannot_be_less_than_0')
    if req.search:
        if not isinstance(req.search, str):
            errors.append('search_field_not_string')
        filtered = filter(lambda note: note['title'].find(req.search) > -1 or note['body'].find(req.search) > -1, notes_list)
        notes = list(filtered)
    else:
        notes = notes_list
    if len(errors):
        raise HTTPException(400, {'errorsList': errors})
    response = notes[req.skip:req.skip+req.take]
    pages = math.ceil(len(notes)/req.take)
    return {'notes': response, 'pages': pages}


@router.post('/create-note')
async def create_note(note: CreateNote):
    errors = []
    if (not note.title):
        errors.append('title_is_empty')
    if (not note.body):
        errors.append('body_is_empty')
    if len(errors):
        raise HTTPException(400, {'errorsList': errors})
    new_note = {
        'id': uuid.uuid4().hex,
        'title': note.title,
        'body': note.body,
        'created_at': datetime.now()
    }
    notes_list.insert(0, new_note)
    return new_note


@router.post('/edit-note')
async def edit_note(note: EditNote):
    errors = []
    if (not note.title):
        errors.append('title_is_empty')
    if (not note.body):
        errors.append('body_is_empty')
    if len(errors):
        raise HTTPException(400, {'errorsList': errors})
    for i in range(len(notes_list)):
        if notes_list[i]['id'] == note.id:
            changed_note = {
                'id': notes_list[i]['id'],
                'title': note.title,
                'body': note.body,
                'created_at': notes_list[i]['created_at']
            }
            notes_list[i] = changed_note
            return changed_note
    raise HTTPException(400, {'errorsList': ['note_not_found']})


@router.delete('/delete-note')
async def delete_note(id: str):
    for item in notes_list:
        if item['id'] == id:
            notes_list.remove(item)
            return 'OK'
    raise HTTPException(400, {'errorsList': ['note_not_found']})