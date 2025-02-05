from pydantic import BaseModel

class User(BaseModel):
    userid: str
    username: str
    email: str
    hashed_password: str