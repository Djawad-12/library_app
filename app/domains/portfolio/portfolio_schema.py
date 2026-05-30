from pydantic import BaseModel, Field
from typing import Optional, List
from ..asset.asset_schema import AssetResponse



class PortfolioCreate(BaseModel):
    name : str = Field(min_length=4,max_length=100)
    initial_deposit : int = Field(gt=0, description="Initial deposit must be greater than zero")
    description : str = Field(max_length=200)


class PortfolioUpdate(BaseModel):
    name : Optional[str] = Field(default=None, min_length=4, max_length=100)
    amount : Optional[int] = None
    description : Optional[str] = Field(default=None, max_length=200)


class PortfolioResponseBasic(BaseModel):
    id : int
    name : str
    amount : int
    initial_deposit : int
    description : str

    class Config:
        from_attributes = True


class PortfolioResponse(BaseModel):
    id : int
    name : str
    amount : int
    initial_deposit : int
    description : str
    assets : List[AssetResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
    
    
