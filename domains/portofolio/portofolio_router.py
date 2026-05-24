from fastapi import APIRouter, Depends, HTTPException
from core.database import get_db
from .portfolio_db_model import portfolio
from .portfolio_schema import portfolioCreate, portfolioResponse, portfolioUpdate
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/api/portfolios",
    tags=["portfolio"],
)


## CRUD operations for portfolios (without services or repository layers for simplicity)


@router.get("/",response_model=list[portfolioResponse])
def get_all_portfolios(db:Session = Depends(get_db)):
    """Get all portfolios"""
    return db.query(portfolio).all()


@router.get("/{item_id}",response_model=portfolioResponse)
def get_portfolio(item_id : int,db:Session = Depends(get_db)):
    """Get a portfolio by id"""
    db_portfolio = db.query(portfolio).filter(portfolio.id == item_id).first()
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="portfolio not found")
    return db_portfolio
    

@router.post("/",response_model=portfolioResponse)
def create_portfolio(portfolio: portfolioCreate, db: Session = Depends(get_db)):
    """Create a new portfolio"""
    db_portfolio = portfolio(
        name=portfolio.name,
        initial_deposit=portfolio.initial_deposit,
        amount=portfolio.initial_deposit,
        description=portfolio.description,
    )

    db.add(db_portfolio)
    db.commit()
    return db_portfolio


@router.put("/{item_id}",response_model=portfolioResponse)
def update_portfolio(item_id: int, portfolio: portfolioUpdate, db: Session = Depends(get_db)):
    """Update a portfolio by id"""
    db_portfolio = db.query(portfolio).filter(portfolio.id == item_id).first()
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="portfolio not found")
    if portfolio.name is not None:
        db_portfolio.name = portfolio.name
    if portfolio.amount is not None:
        db_portfolio.amount = db_portfolio.amount + portfolio.amount
    if portfolio.description is not None:
        db_portfolio.description = portfolio.description
    
    db.commit()
    return db_portfolio