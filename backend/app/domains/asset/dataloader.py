import pandas as pd
import asyncio
from app.core.database import get_db, SessionLocal
from app.domains.asset.asset_db_model import Asset
from app.domains.asset.asset_repository import Asset_Repository
from app.domains.asset.asset_schema import ImportAssetResponse
from sqlalchemy.orm import Session
from app.domains.asset.asset_service import AssetService
from rich.traceback import install
install(show_locals=True)


PATH = "data/cleaned_stock_data.csv"

class AssetDataLoader:
    def __init__(self, db: Session):
        self.db = db
        self.repo = Asset_Repository(db)
        self.service = AssetService(self.repo)

    def load_data_from_csv(self, file_path: str) -> ImportAssetResponse:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        count, markets = self.service.import_assets_from_csv(file_content)
        return ImportAssetResponse(count=count, markets=markets)
    
def main() -> None:
    db = SessionLocal()
    loader = AssetDataLoader(db)
    result = loader.load_data_from_csv(PATH)
    print(f"Imported {result.count} assets from markets: {', '.join(result.markets)}")


if __name__ == "__main__":
    main()