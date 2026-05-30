from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username : str
    password : str


class UserLogin(BaseModel):
    identifier : str
    password : str

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    username : str
    password : str

    class Config:
        from_attributes = True


