from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey



class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer,primary_key=True)
    name = Column(String,index=True)
    amount = Column(Integer)
    initial_deposit = Column(Integer)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


class AssetPortfolio(Base):
    __tablename__ = "asset_in_portfolios"
    id = Column(Integer, primary_key= True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset_ticker = Column(String,ForeignKey("assets.ticker"))


