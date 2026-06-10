from rich.traceback import install
install(show_locals=True)
from fastapi import FastAPI
from app.domains.portfolio.portfolio_router import router as portfolio_router
from app.domains.asset.asset_router import router as asset_router
from app.core.database import Base, engine
from app.domains.user.user_router import router as user_router
from fastapi.middleware.cors import CORSMiddleware



## Import models and setup database Base.metadata.create_all(bind=engine) in the main file
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Your Vue app URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolio_router)
app.include_router(asset_router)
app.include_router(user_router)
