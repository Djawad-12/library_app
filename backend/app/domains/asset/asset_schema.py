from pydantic import BaseModel, Field
from typing import Optional


class AssetCreate(BaseModel):
    ticker : str
    name : str
    market : str


class AssetUpdate(BaseModel):
    name : Optional[str] = Field(default = None)
    market : Optional[str] = Field(default = None)


class AssetResponse(BaseModel):
    ticker : str
    name : str
    market : str

    class Config:
        from_attributes = True

class ImportAssetResponse(BaseModel):
    count : int
    markets : list[str]

    class Config:
        from_attributes = True



