from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Fast api React todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class TodoItem(BaseModel):
    id: int
    title: str
    completed:bool = False

class TodoCreate(BaseModel):
    title:str
    completed:Optional[bool]=False

todo_db:List[TodoItem] =[
     TodoItem(id=1,title="Learn FastAPI", completed=False),
     TodoItem(id=2,title="Learn React", completed=False),
]

@app.get("/api/todos", response_model=List[TodoItem])
def get_todos():
    return todo_db

@app.post("/api/todos", responce_model=TodoItem)
def create_todo(todo:TodoCreate):
    new_id = max([t.id for t in todo_db],default=0)=1
    new_todo = TodoItem(id=new_id, title=todo.title, completed=False)
    todo_db.append(new_todo)
    return new_todo

@app.put("/api/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id:int, updated_todo;TodoCreate):
    for item in todo_db:
        if item["id"]==todo_id:
            item["title"]=updated_todo.title
            return item
    raise HTTPException(Status_code=404,detail="Todo not found")

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id:int):
    global todo_db
    for item in todo_db:
        if item["id"]==todo_id:
            todo_db=[i for i in todo_db if i["id"]!=todo_id]
            return {"message":f"Todo {todo_id} deleted successfully"}
    raise HTTPException(status_code=404,detail="Todo not found")




