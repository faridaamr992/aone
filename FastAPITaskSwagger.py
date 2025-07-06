from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class NameRequest(BaseModel):
    name:str = Field(default="Farida")
    age:int = Field(default=23)

@app.post("/greet")
def greet_user(data: NameRequest):
    return {
        "message": f"Hello {data.name}",
        "age": data.age
    }
