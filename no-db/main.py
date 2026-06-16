from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def welcome():
    return {'message':"welcome to my fast api applcaitions"}


from pydantic import BaseModel
from typing import List


class Article(BaseModel):
    id:int
    name:str
    price:float

articles = []

@app.get("/articles", response_model=List[Article])
async def read_articles():
    return articles

@app.post("/articles", response_model=Article)
async def create_article(article:Article):
    articles.append(article)
    return article

@app.put("/articles/{article_id}",response_model=Article)
async def update_article(article_id:int,article:Article):
    articles[article_id]=article
    return article

@app.delete("/articles/{article_id}")
async def delete_article(article_id:int):
    del articles[article_id]
    return {"message":"Article deleted"}
