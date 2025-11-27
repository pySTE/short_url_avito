from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str

    class Config:
        scheme_example = {
            "email": "youremail@gmail.com",
            "password": "your_password123"
        }
