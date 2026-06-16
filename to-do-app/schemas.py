from pydantic import BaseModel

class TaskCreate(BaseModel):
    task:str

class Task(BaseModel):
    id:int
    task:str

    class Config:
        orm_mode=True