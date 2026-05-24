from pydantic import BaseModel, Field
from typing import Optional

class portfolioCreate(BaseModel):
    name : str = Field(min_length=4,max_length=100)
    initial_deposit : int = Field(gt=0, description="Initial deposit must be greater than zero")
    description : str = Field(max_length=200)


class portfolioUpdate(BaseModel):
    name : Optional[str] = Field(min_length=4,max_length=100)
    amount : Optional[int] 
    description : Optional[str] = Field(max_length=200)


class portfolioResponse(BaseModel):
    id : int
    name : str
    amount : int
    initial_deposit : int
    description : str

    class Config:
        orm_mode = True
    
