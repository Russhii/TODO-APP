from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoCreate(BaseModel):
  title:str=Field(...,min_length=2,max_length=100)
  description:Optional[str]=None

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoOut(BaseModel):
  id:int
  title:str
  description:Optional[str]
  completed:bool
  created_at:datetime

  class config:
     from_attributes =True
