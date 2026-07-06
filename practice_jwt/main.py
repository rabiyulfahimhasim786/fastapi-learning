from fastapi import FastAPI
from schemas import login
app=FastAPI()

@app.get("/health")
def health():
  return {"message":"server running"}

@app.post("/login")
def login(data:login):
  return {
    "username":data.username,
    "password":data.password
  }


