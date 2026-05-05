from fastapi import FastAPI, Depends ,HTTPException ,status
from sqlalchemy.orm import Session
from typing import List

import models , schemas
from database import engine , SessionLocal

models.Base.metadata.create_all(bind=engine)

app =FastAPI(
  title="To-Do API",
  version="1.0.0"
)

def get_db():
  db =SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.post('/todos',response_model=schemas.TodoOut, status_code=201)
def create_todo(todo: schemas.TodoCreate, db:Session =Depends(get_db)):
   new_todo =models.Todo(
     title=todo.title,
     description=todo.description
   )
   db.add(new_todo)
   db.commit()
   db.refresh(new_todo)
   return new_todo


@app.get('/todos',response_model=List[schemas.TodoOut])
def get_todos(
  skip:int=0,
  limit:int=10,
  db:Session=Depends(get_db)
):
  todo =db.query(models.Todo).offset(skip).limit(limit).all()
  return todo


@app.put('/todos/{todo_id}',response_model=schemas.TodoOut)
def update_todo(
  todo_id:int,
  updates:schemas.TodoUpdate,
  db:Session=Depends(get_db)
):
  todo =db.query(models.Todo).filter(models.Todo.id==todo_id).first()
  if not todo:
    raise HTTPException(status_code=404, detail="todo not found")
  
  update_data =updates.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    setattr(todo, field, value)

  db.commit()
  db.refresh(todo)
  return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return None  