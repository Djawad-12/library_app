from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from .portfolio_schema import PortfolioCreate, PortfolioResponse, PortfolioUpdate, PortfolioResponseBasic
from sqlalchemy.orm import Session
from .portfolio_service import PortfolioService, AssetPortfolioService
from ..asset.asset_schema import AssetResponse
from ..asset.asset_service import AssetService
from app.core.dependancies import get_portfolio_service, get_asset_portfolio_service, get_asset_service
from ..asset.asset_schema import AssetResponse


router = APIRouter(
    prefix="/api/portfolios",
    tags=["portfolio"],
)


## CRUD operations for portfolios with service layer and database interactions

@router.get("/",response_model=list[PortfolioResponseBasic])
def get_all_portfolios(service: PortfolioService = Depends(get_portfolio_service)):
    """Get all portfolios"""
    return service.get_all_portofolios()


@router.get("/{portfolio_id}",response_model=PortfolioResponse)
def get_portfolio(portfolio_id : int,service:PortfolioService = Depends(get_portfolio_service), 
                  asset_portfolio_service : AssetPortfolioService = Depends(get_asset_portfolio_service),
                  asset_service : AssetService = Depends(get_asset_service)):
    """Get a portfolio by id"""
    assets = asset_portfolio_service.get_asset_by_portfolio_id(portfolio_id)
    db_portfolio = service.get_portfolio(portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="portfolio not found")
    
    l = []
    for asset in assets : 
        l.append(asset_service.get_asset(asset.asset_ticker))
    
    return PortfolioResponse(
        id = portfolio_id,
        name = db_portfolio.name,
        amount = db_portfolio.amount,
        initial_deposit = db_portfolio.initial_deposit,
        description = db_portfolio.description,
        assets = l
    )
    

@router.post("/",response_model=PortfolioResponseBasic)
def create_portfolio(portfolio: PortfolioCreate, service: PortfolioService = Depends(get_portfolio_service)):
    """Create a new portfolio"""

    return service.create_portfolio(
        portfolio.name,
        portfolio.initial_deposit,
        portfolio.description
    )



@router.put("/{portfolio_id}",response_model=PortfolioResponseBasic)
def update_portfolio(portfolio_id: int, portfolio: PortfolioUpdate, service: PortfolioService = Depends(get_portfolio_service)):
    """Update a portfolio by id"""

    return service.update_portfolio(
        portfolio_id,
        portfolio.name,
        portfolio.amount,
        portfolio.description
    )



@router.put("/{portfolio_id}/{ticker}",response_model=str)
def add_asset_to_portfolio(portfolio_id : int, ticker : str, asset_portfolio_service : AssetPortfolioService = Depends(get_asset_portfolio_service)):
    try :
        result = asset_portfolio_service.add_asset_to_portfolio(portfolio_id, ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred while adding asset to portfolio")

    return result
