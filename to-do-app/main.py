from typing import List
from fastapi import FastAPI, status,HTTPException,Depends
from database import Base,engine,SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

Base.metadata.create_all(engine)

app=FastAPI()

def get_session():
    session =SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def home():
    return "all"

@app.post("/todo",response_model=schemas.Task,status_code=status.HTTP_201_CREATED)
def create_task(task:schemas.TaskCreate,session:Session=Depends(get_session)):
    task_db=models.Task(task=task.task)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db

@app.post("/todo/{id}",response_model=schemas.Task)
def read_task(id:int,session:Session=Depends(get_session)):
    task=session.query(models.Task).get(id)
    if not task:
        raise HTTPException(status_code=404,detail=f"Task with id {id} not found")
    return task

@app.put("/todo/{id}",response_model=schemas.Task)
def update_task(id:int,task:str,session:Session=Depends(get_session)):
    task_db=session.query(models.Task).get(id)
    if task_db:
        task_db.task=task
        session.commit()
    if not task_db:
        raise HTTPException(status_code=404,detail=f"Task with id {id} not found ")
    return task_db

@app.delete("/todo/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int,session:Session=Depends(get_session)):
    task_db=session.query(models.Task).get(id)
    if task_db:
        session.delete(task_db)
        session.commit()
    else:
        raise HTTPException(status_code=404,detail=f"Task with id {id} not found")
    return None

@app.get("/todo",response_model=List[schemas.Task])
def read_task_list(session:Session=Depends(get_session)):
    task_list=session.query(models.Task).all()
    return task_list
