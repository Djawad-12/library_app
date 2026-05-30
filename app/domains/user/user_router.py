from fastapi import Depends, HTTPException, APIRouter
from .user_service import UserService
from app.core.dependancies import get_user_service
from .user_schema import UserCreate, UserLogin, UserResponse
from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
import dotenv
import os
dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))




def create_access_token(data : dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)


router = APIRouter(prefix = "/api/user", tags = ["User"])



@router.get("/",response_model=list[UserResponse])
def get_all_users(service : UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id : str, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if user is None :
        raise HTTPException(status_code=401, detail = "User not found")
    return user

@router.post("/",response_model=UserResponse)
def register(user : UserCreate, service:UserService = Depends(get_user_service)):
    return service.register_user(user.email, user.username, user.password)

@router.post("/token")
async def login(user : UserLogin, service : UserService = Depends(get_user_service)):
    user = service.login_user(user.identifier, user.password)
    if not user : 
        raise HTTPException(status_code=401, detail = "Incorrect credentials")
    token = create_access_token(
        data = {"sub" : str(user.id)}
    )
    return {"access_token" : token, "token_type" : "bearer"}





