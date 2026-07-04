from .portfolio_repository import PortfolioRepository, AssetPortfolioRepository
from .portfolio_db_model import Portfolio, AssetPortfolio
from typing import List
from ..asset.asset_service import AssetService
from fastapi import Depends
from ..asset.asset_repository import Asset_Repository


class PortfolioService:
    def __init__(self, portfolio_repo : PortfolioRepository):
        self.repo = portfolio_repo

    def get_all_portofolios(self) -> List[Portfolio] :
        return self.repo.get_all()
    
    def get_all_portfolios_by_user_id(self, user_id : int) -> List[Portfolio] :
        return self.repo.get_all_by_user_id(user_id)
    
    def get_portfolio(self,id: int) -> Portfolio:
        return self.repo.get_portfolio_by_id(id)
    
    def get_portfolio_by_user_id(self, user_id : int, portfolio_id : int) -> Portfolio :
        return self.repo.get_portfolio_by_user_id(user_id, portfolio_id)
    
    
    def create_portfolio(self,user_id : int, name:str, initial_deposit : int, description : str | None) -> Portfolio:
        portfolio = Portfolio(
            user_id = user_id,
            name = name,
            initial_deposit = initial_deposit,
            amount = initial_deposit,
            description = description
        )

        return self.repo.create_portfolio(portfolio)
    
    def update_portfolio(self, user_id : int, portfolio_id : int, name : str | None, amount : int | None, description : str | None) -> Portfolio :
        portfolio = self.repo.get_portfolio_by_user_id(user_id, portfolio_id)
        if name is not None:
            portfolio.name = name
        if amount is not None :
            portfolio.amount = portfolio.amount + amount 
        if description is not None :
            portfolio.description = description

        return self.repo.update(portfolio)
        



class AssetPortfolioService:
    def __init__(self, portfolio_repo : AssetPortfolioRepository, asset_repo : Asset_Repository):
        self.repo = portfolio_repo
        self.asset_repo = asset_repo

    def get_all_assets(self) -> AssetPortfolio :
        return self.repo.get_all()
    
    def get_asset_by_portfolio_id(self, portfolio_id: int) -> List[AssetPortfolio] :
        return self.repo.get_asset_by_portfolio_id(portfolio_id)
    
    def add_asset_to_portfolio(self, portfolio_id: int,ticker : str, quantity: float) -> str | None :
        try :
            asset = self.asset_repo.get_asset_by_id(ticker)
        except Exception :
            print("Asset not found")
            return None
        if quantity <=0:
            return None
        asset_portfolio = AssetPortfolio(
            portfolio_id = portfolio_id,
            asset_ticker = ticker,
            quantity = quantity
        )
        self.repo.add_asset_in_portfolio(asset_portfolio)

        return asset.ticker
    
    def remove_asset_from_portfolio(self, asset_portfolio_id : int) -> None :
        try :
            asset_portfolio = self.repo.get_asset_by_portfolio_id(asset_portfolio_id)
        except Exception :
            return None
        self.repo.delete(asset_portfolio)

        return None

        
    

