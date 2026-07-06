from fastapi import FastAPI
from schemas import Login
app=FastAPI()

@app.get("/health")
def health():
  return {"message":"server running"}

@app.post("/login")
def login(data:Login):
  return {
    "username":data.username,
    "password":data.password
  }


