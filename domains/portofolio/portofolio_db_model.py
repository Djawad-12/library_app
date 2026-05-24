from core.database import Base
from sqlalchemy import Column, Integer, String



class portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer,primary_key=True)
    name = Column(String,index=True)
    amount = Column(Integer)
    initial_deposit = Column(Integer)
    description = Column(String)





