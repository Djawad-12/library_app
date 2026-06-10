from app.core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from .asset_db_model import Asset
from typing import List


class Asset_Repository():
    def __init__(self,db: Session = Depends(get_db)):
        self.db = db

    def get_all_assets(self) -> List[Asset] :
        return self.db.query(Asset).all()
    
    def get_asset_by_id(self,ticker: str) -> Asset:
        return self.db.query(Asset).filter(ticker == Asset.ticker).first()

    def create_asset(self, asset: Asset) -> Asset:
        self.db.add(asset)
        self.db.commit()
        return asset

    def create_assets(self, assets: list[Asset]) -> list[Asset]:
        if not assets:
            return assets
        self.db.add_all(assets)
        self.db.commit()
        return assets
    
    def update(self, asset: Asset) -> Asset :
        self.db.commit()
        return asset
    
    def delete_asset(self, asset: Asset) -> None :
        self.db.delete(asset)

