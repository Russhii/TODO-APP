from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,field_validator,EmailStr,Field
from typing import Optional,List
import uuid


app =FastAPI(
  title="Student Registration API" 
)

class Student(BaseModel):
  name:str =Field(..., min_length=2,max_length=50)
  age:int=Field(...,ge=10,le=100)
  email:str=Field(...)
  courses:List[str]=Field(default=[])
  gpa:Optional[float]


  @field_validator("name")
  @classmethod
  def name_must_be_real(cls,v):
    if not v.replace(" ","").isalpha():
      raise ValueError("Name must contain only letters and spaces ")
    return v.strip().title()
  
  @field_validator("age")
  @classmethod
  def age_must_be_valid(cls,v):
    if v<10:
      raise ValueError("Age must be at least 10")
    return v
  

  @field_validator("courses")
  @classmethod
  def courses_must_have_item(cls,v):
      if len(v)>10:
         raise ValueError("Cannot enroll in more than 10 courses")
      return [c.strip() for c in v]  
  
class StudentOut(BaseModel):
    id: str
    name: str
    age: int
    email: str
    courses: List[str]
    gpa: Optional[float]
    status: str


students_db:dict={}

@app.post("/students",response_model=StudentOut,status_code=201)
def register_student(student:Student):
   student_id =f"STU-{str(uuid.uuid4())[:8].upper()}"
   record = StudentOut(
      id=student_id,
      name=student.name,
      age=student.age,
      email=student.email,
      courses=student.courses,
      gpa=student.gpa,
      status="registered"
   )
   students_db[student_id]=record
   return record


@app.get('/students')
def list_students():
   return list(students_db.values())


@app.get('/students/{student_id}', response_model=StudentOut)
def get_student(student_id:str):
   if student_id not in students_db:
      raise HTTPException(status_code=404,detail="Student not found")
   return students_db[student_id]