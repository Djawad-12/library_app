from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from .portfolio_schema import PortfolioCreate, PortfolioResponse, PortfolioUpdate, PortfolioResponseBasic
from sqlalchemy.orm import Session
from .portfolio_service import PortfolioService, AssetPortfolioService
from ..asset.asset_schema import AssetResponse
from ..asset.asset_service import AssetService
from app.core.dependancies import get_portfolio_service, get_asset_portfolio_service, get_asset_service
from app.domains.user.user_service import UserService
from app.core.dependancies import get_user_service
from ..asset.asset_schema import AssetResponse
from ...middlewares.middleware_authentification import get_current_user


router = APIRouter(
    prefix="/api/portfolios",
    tags=["portfolio"],
)


## CRUD operations for portfolios with service layer and database interactions

@router.get("/",response_model=list[PortfolioResponseBasic])
def get_all_portfolios(user_id:int = Depends(get_current_user), service: PortfolioService = Depends(get_portfolio_service),
                       user_service : UserService = Depends(get_user_service)):
    """Get all portfolios"""
    user = user_service.get_user_by_db_id(user_id)
    if user.role != "admin":
        raise HTTPException(status_code=401, detail = "You need elevated privileges")
    return service.get_all_portofolios()

    

@router.get("/current}",response_model=list[PortfolioResponse])
def get_all_portfolios_by_user_id(user_id : int = Depends(get_current_user), service: PortfolioService = Depends(get_portfolio_service),
                                  user_service : UserService = Depends(get_user_service),
                                  asset_service : AssetService = Depends(get_asset_service),
                                  asset_portfolio_service : AssetPortfolioService = Depends(get_asset_portfolio_service)):
    """Get all portfolios by user id"""
    user = user_service.get_user_by_db_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    portfolios = service.get_all_portfolios_by_user_id(user_id)
    l_portfolio = []
    for portfolio in portfolios :
        l = []
        assets = asset_portfolio_service.get_asset_by_portfolio_id(portfolio.id)
        if assets is None :
            l_portfolio.append(PortfolioResponse(
                id = portfolio.id,
                name = portfolio.name,
                amount = portfolio.amount,
                initial_deposit = portfolio.initial_deposit,
                description = portfolio.description,
                user_id= portfolio.user_id
            ))
        else :
            for asset in assets : 
                l.append(asset_service.get_asset(asset.asset_ticker))
            l_portfolio.append(PortfolioResponse(
            id = portfolio.id,
            name = portfolio.name,
            amount = portfolio.amount,
            initial_deposit = portfolio.initial_deposit,
            description = portfolio.description,
            assets = l,
            user_id = portfolio.user_id
            )
            )
    return l_portfolio


@router.get("/{portfolio_id}",response_model=PortfolioResponse)
def get_portfolio(portfolio_id : int,service:PortfolioService = Depends(get_portfolio_service), 
                  asset_portfolio_service : AssetPortfolioService = Depends(get_asset_portfolio_service),
                  asset_service : AssetService = Depends(get_asset_service),
                  user_service : UserService = Depends(get_user_service),
                  user_id : int = Depends(get_current_user)):
    """Get a portfolio by id"""
    user = user_service.get_user_by_db_id(user_id)
    if user.role != "admin":
        raise HTTPException(status_code=401,detail="You need elevated privileges")
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
        assets = l,
        user_id = db_portfolio.user_id
    )


@router.get("/current/{portfolio_id}",response_model=PortfolioResponse)
def get_portfolio_by_user_id(portfolio_id : int, user_id : int = Depends(get_current_user), service: PortfolioService = Depends(get_portfolio_service), 
                  asset_portfolio_service : AssetPortfolioService = Depends(get_asset_portfolio_service),
                  asset_service : AssetService = Depends(get_asset_service),user_service : UserService = Depends(get_user_service)):  
    """Get a portfolio by user id and portfolio id"""
    user = user_service.get_user_by_db_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    assets = asset_portfolio_service.get_asset_by_portfolio_id(portfolio_id)
    db_portfolio = service.get_portfolio_by_user_id(user_id, portfolio_id)
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
        assets = l,
        user_id = db_portfolio.user_id
    )
    

@router.post("/",response_model=PortfolioResponseBasic)
def create_portfolio(portfolio: PortfolioCreate, 
                     service: PortfolioService = Depends(get_portfolio_service),
                     user_service : UserService = Depends(get_user_service),
                     user_id : int = Depends(get_current_user)):
    """Create a new portfolio"""    
    user = user_service.get_user_by_db_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return service.create_portfolio(
        user_id,
        portfolio.name,
        portfolio.initial_deposit,
        portfolio.description
    )



@router.put("/{portfolio_id}",response_model=PortfolioResponseBasic)
def update_portfolio(portfolio_id: int, portfolio: PortfolioUpdate,
                     service: PortfolioService = Depends(get_portfolio_service),
                     user_service : UserService = Depends(get_user_service),
                     user_id: int = Depends(get_current_user)):
    """Update a portfolio by id"""
    user = user_service.get_user_by_db_id(user_id)
    if user is None :
        raise HTTPException(status_code=401,detail="User not found")
    
    return service.update_portfolio(
        portfolio_id,
        portfolio.name,
        portfolio.amount,
        portfolio.description
    )



@router.put("/{portfolio_id}/{ticker}",response_model=str)
def add_asset_to_portfolio(portfolio_id : int, ticker : str, 
                           asset_portfolio_service : AssetPortfolioService = Depends(get_asset_portfolio_service),
                           user_id :int = Depends(get_current_user),
                           user_service : UserService = Depends(get_user_service)):

    user = user_service.get_user_by_db_id(user_id)
    if user.role != "admin" :
        raise HTTPException(status_code=401,detail="You need elevated privileges")
    result = asset_portfolio_service.add_asset_to_portfolio(portfolio_id, ticker)

    return result


@router.put("/current/{portfolio_id}/{ticker}",response_model=str)
def add_asset_to_portfolio_by_user(portfolio_id : int, ticker : str, 
                           asset_portfolio_service : AssetPortfolioService = Depends(get_asset_portfolio_service),
                           user_id :int = Depends(get_current_user),
                           user_service : UserService = Depends(get_user_service),
                           portfolio_service : PortfolioService = Depends(get_portfolio_service)):
    try :
        user = user_service.get_user_by_db_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail = "User not found")
        portfolio = portfolio_service.get_portfolio_by_user_id(user_id,portfolio_id)
        if portfolio is None :
            raise HTTPException(status_code=401, detail="Portfolio doesn't exist")
        result = asset_portfolio_service.add_asset_to_portfolio(portfolio_id, ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred while adding asset to portfolio")

    return result
