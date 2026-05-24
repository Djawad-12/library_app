from rich.traceback import install
install(show_locals=True)
from fastapi import FastAPI
from domains.portfolio.portfolio_router import router as portfolio_router
from core.database import Base, engine



## Import models and setup database Base.metadata.create_all(bind=engine) in the main file
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(portfolio_router)
