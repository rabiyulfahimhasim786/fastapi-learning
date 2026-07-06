from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
  return {"message":"hello world"}

@app.get("/health")
def health():
  return {"message":"server running"}


