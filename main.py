from fastapi import FastAPI
from pydantic import Field, BaseModel


app = FastAPI(
    title="Message_App"
)

class User(BaseModel):
    telephone:str
    password:str
    nickname:str

class SMS(BaseModel):
    text:str



@app.get("/")
def get_user(user_id: int):
    return "хело мир"

@app.get("/register")
def register_user(user_id: int):
    return "хело мир"