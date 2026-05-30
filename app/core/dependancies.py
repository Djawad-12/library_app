from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from app.domains.portfolio.portfolio_repository import PortfolioRepository, AssetPortfolioRepository
from app.domains.portfolio.portfolio_service import PortfolioService, AssetPortfolioService
from app.domains.asset.asset_service import AssetService
from app.domains.asset.asset_repository import Asset_Repository
from app.domains.user.user_repository import UserRepository
from app.domains.user.user_service import UserService

### PORTFOLIO SERVICE
def get_portfolio_repository(db: Session = Depends(get_db)) -> PortfolioRepository:
    return PortfolioRepository(db)

def get_portfolio_service(repo: PortfolioRepository = Depends(get_portfolio_repository)) -> PortfolioService:
    return PortfolioService(repo)

### ASSET SERVICE
def get_asset_repository(db: Session = Depends(get_db)) -> Asset_Repository:
    return Asset_Repository(db)

def get_asset_service(repo: Asset_Repository = Depends(get_asset_repository)) -> AssetService :
    return AssetService(repo)

### ASSET PORTFOLIO SERVICE
def get_asset_portfolio_repository(db: Session = Depends(get_db)) -> AssetPortfolioRepository:
    return AssetPortfolioRepository(db)

def get_asset_portfolio_service(repo: AssetPortfolioRepository = Depends(get_asset_portfolio_repository), asset_repo: Asset_Repository = Depends(get_asset_repository)) -> AssetPortfolioService:
    return AssetPortfolioService(repo, asset_repo)

### USER SERVICE
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository :
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService :
    return UserService(repo)