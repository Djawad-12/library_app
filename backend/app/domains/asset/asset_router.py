from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from .asset_schema import AssetResponse, AssetCreate, AssetUpdate, ImportAssetResponse
from .asset_service import AssetService
from app.core.dependancies import get_asset_service, get_user_service
from ...middlewares.middleware_authentification import get_current_user
from ..user.user_service import UserService


router = APIRouter(prefix = "/api/assets", tags = ["Asset"])



@router.get("/",response_model=list[AssetResponse])
def get_all_assets(service : AssetService = Depends(get_asset_service),
                   user_service : UserService = Depends(get_user_service),
                   user_id : int = Depends(get_current_user)):
    user = user_service.get_user_by_db_id(user_id)
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="You need elevated privileges")
    return service.get_all_assets()


@router.get("/{ticker}",response_model=AssetResponse)
def get_asset(ticker : str, service : AssetService = Depends(get_asset_service)):
                       
    asset = service.get_asset(ticker)
    if asset is None:
        raise HTTPException(status_code=404,detail="Asset not found")
    return asset


@router.get("/annual_returns/{ticker}", response_model=dict[int, float])
def get_annual_returns(ticker : str, service : AssetService = Depends(get_asset_service)):
    asset = service.get_stock_annual_return(ticker)
    if asset is None:
        raise HTTPException(status_code=404, detail = "Asset not found")   
    return asset

@router.get("/monthly_returns/{ticker}", response_model=dict[str, float])
def get_annual_returns(ticker : str, service : AssetService = Depends(get_asset_service)):
    asset = service.get_stock_monthly_return(ticker)
    if asset is None:
        raise HTTPException(status_code=404, detail = "Asset not found")   
    return asset


@router.get("/price/{ticker}",response_model=float)
def get_actual_price(ticker : str, service : AssetService = Depends(get_asset_service)):
    asset = service.get_stock_actual_price(ticker)
    if asset is None:
        raise HTTPException(status_code=404,detail = "Asset not found or API can't fetch the data")
    return asset



@router.post("/",response_model = AssetResponse)
def create_asset(asset : AssetCreate, service : AssetService = Depends(get_asset_service),
                 user_service : UserService = Depends(get_user_service),
                       user_id : int = Depends(get_current_user)):
    user = user_service.get_user_by_db_id(user_id)
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="You need elevated privileges")
    return service.create_asset(
        asset.ticker,
        asset.name,
        asset.market
    )


@router.put("/{ticker}",response_model=AssetResponse)
def update_asset(ticker: str, asset : AssetUpdate, service : AssetService = Depends(get_asset_service),
                       user_service : UserService = Depends(get_user_service),
                   user_id : int = Depends(get_current_user)):
    user = user_service.get_user_by_db_id(user_id)
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="You need elevated privileges")
    return service.update_asset(
        ticker,
        asset.ticker,
        asset.name,
        asset.market
    )



                 
                 