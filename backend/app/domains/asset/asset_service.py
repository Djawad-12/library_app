
from .asset_repository import Asset_Repository
from .asset_db_model import Asset
import pandas as pd
import io
from typing import List
import yfinance as yf
import calendar
from datetime import datetime


class AssetService():
    def __init__(self, repo: Asset_Repository):
        self.repo = repo

    def get_all_assets(self) -> List[Asset] :
        return self.repo.get_all_assets()
    
    def get_asset(self,ticker : str) -> Asset :
        return self.repo.get_asset_by_id(ticker)
    
    def create_asset(self, ticker: str, name : str, market: str) -> Asset:
        asset = Asset(
            ticker = ticker,
            name = name,
            market = market
        )
        return self.repo.create_asset(asset)


    def update_asset(self,ticker: str, name : str | None, market: str | None) -> Asset:
        asset = self.repo.get_asset_by_id(ticker)
        if name is not None : 
            asset.name = name
        if market is not None :
            asset.market is not None
        
        return self.repo.update(asset)
    
    def delete_asset(self, asset : Asset) -> None :
        self.repo.delete_asset(asset)

    def import_assets_from_csv(self, file: bytes) -> tuple[int, list[str]]:
        data = pd.read_csv(io.BytesIO(file))
        assets = [
            Asset(ticker=row.Ticker, name=row.Company, market=row.Market)
            for row in data.itertuples(index=False)
        ]
        self.repo.create_assets(assets)

        return len(data), data["Market"].value_counts().index.to_list()


    def get_stock_annual_return(self, ticker : str) -> dict[int, float] | None :
        asset = self.repo.get_asset_by_id(ticker)
        if asset is None:  
            return None
        try :
            stock = yf.Ticker(asset.ticker)
            prices = stock.history(period='126mo')
            prices['Returns'] = prices["Close"].pct_change()
            annual_returns = prices["Returns"].groupby(prices.index.year).sum()
            return annual_returns.to_dict()
        except Exception :
            return None
        
        
    
    
    def get_stock_monthly_return(self, ticker:str) -> dict[str, float] | None :
        asset = self.repo.get_asset_by_id(ticker)
        if asset is None : 
            return None 
        try :
            stock = yf.Ticker(asset.ticker)
            prices = stock.history(period='12mo')
            prices['Returns'] = prices["Close"].pct_change()
            monthly_returns = prices["Returns"].groupby(prices.index.month).sum()
            monthly_returns = monthly_returns.drop(datetime.now().month)
            month_order = [ (datetime.now().month - i - 2) % 12 +1 for i in range (11) ]
            monthly_returns = monthly_returns.reindex(month_order)
            monthly_returns.index = [calendar.month_name[i] for i in monthly_returns.index]
            return monthly_returns.to_dict()
        except Exception:
            return None

        
    

    def get_stock_actual_price(self, ticker:str) -> float | None : 
        asset = self.repo.get_asset_by_id(ticker)
        if asset is None:
            return None
        try :
            price = yf.Ticker(asset.ticker).info["regularMarketPrice"]
            return price
        except Exception :
            return None
        


