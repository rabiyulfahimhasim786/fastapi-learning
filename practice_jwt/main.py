from fastapi import FastAPI

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


