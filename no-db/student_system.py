from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app=FastAPI()
students =[]
class Student(BaseModel):
    id:int
    name:str
    marks:int


@app.post("/students")
def add_student(student:Student):
    students.append(student)
    return {"message":"Student_added"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id:int):
    for student in students:
        if student.id==student_id:
            return student
    raise   HTTPException(404, "Student Not Found")

@app.put("/students/{student_id}")
def upate_student(student_id:int,marks:int):
    for student in students:
        if student.id==student_id:
            student.marks=marks
            return {"message":"Updated"}
    raise HTTPException(404,"Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id:int):
    for student in students:
        if student.id==student_id:
            students.remove(student)
            return {"message":"deleted"}
    raise HTTPException(404,"Student not found")
