from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def root(name:str):
    return {"message": "Hello "+name}

from pydantic import BaseModel
db = {}

class Item (BaseModel):
    name:str
    desc:str

@app.post("/postings")
async def create(item:Item):
    db[item.name] = item.desc
    return {"item": item}


@app.get("/getdata")
async def getdata():
    return db



@app.delete("/deletedata")
async def deletedata(name:str):
    del db[name]
    return db



@app.put("/putdata")
async def getdata(item:Item):
    db[item.name]= item.desc
    return db
