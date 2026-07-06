from pydantic import BaseModel

class Login(BaseModel):
  username:str
  password:str

class Register(BaseModel):
  name:str
  email:str
  password:str
