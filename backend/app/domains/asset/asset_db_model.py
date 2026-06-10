from app.core.database import Base
from sqlalchemy import Column, Integer, String  


class Asset(Base):
    __tablename__ = "assets"
    ticker = Column(String, primary_key=True)
    name = Column(String)
    market = Column(String)