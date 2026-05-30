from app.core.database import get_db
from sqlalchemy.orm import Session
from app.domains.portfolio.portfolio_db_model import Portfolio, AssetPortfolio
from typing import List


class PortfolioRepository:
    def __init__(self, db : Session):
        self.db = db
        
    def get_all(self) -> List[Portfolio]:
        return self.db.query(Portfolio).all()
    
    def get_portfolio_by_id(self, portfolio_id : int) -> Portfolio:
        return  self.db.query(Portfolio).filter(portfolio_id == Portfolio.id).first()
    
    def create_portfolio(self, portfolio : Portfolio) -> Portfolio:
        self.db.add(portfolio)
        self.db.commit()
        return portfolio
    
    def update(self, portfolio : Portfolio) -> Portfolio:
        self.db.commit()
        return portfolio
    
    def delete(self, portfolio : Portfolio) -> None:
        self.db.delete(portfolio)
        self.db.commit()


class AssetPortfolioRepository : 
    def __init__(self, db :Session):
        self.db = db

    def get_all(self) -> List[AssetPortfolio]:
        return self.db.query(AssetPortfolio).all()
    
    def get_asset_by_portfolio_id(self, portfolio_id : int) -> List[AssetPortfolio]:
        return self.db.query(AssetPortfolio).filter(portfolio_id == AssetPortfolio.portfolio_id).all()
    
    def add_asset_in_portfolio(self, asset_in_portfolio : AssetPortfolio) -> AssetPortfolio:
        self.db.add(asset_in_portfolio)
        self.db.commit()
        return asset_in_portfolio
    
    def update(self, asset_in_portfolio : AssetPortfolio) -> AssetPortfolio:
        self.db.commit()
        return asset_in_portfolio   
    
    def delete(self, asset_in_portfolio : AssetPortfolio) -> None:
        self.db.delete(asset_in_portfolio)
        self.db.commit()