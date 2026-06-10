from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .user_service import UserService
from app.core.dependancies import get_user_service
from .user_schema import UserCreate, UserLogin, UserResponse
from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
from ...middlewares.middleware_authentification import get_current_user
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
def get_all_users(service : UserService = Depends(get_user_service),
                  user_id : int = Depends(get_current_user)):
    user = service.get_user_by_db_id(user_id)
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="You need elevated privileges")
    return service.get_all_users()

@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id : str, service: UserService = Depends(get_user_service),
             user_id_db : int = Depends(get_current_user)):
    user_db = service.get_user_by_db_id(user_id_db)
    if user_db.role != "admin":
        raise HTTPException(status_code=401, detail="You need elevated privileges")
    user = service.get_user(user_id)
    if user is None :
        raise HTTPException(status_code=401, detail = "User not found")
    return user

@router.post("/",response_model=UserResponse)
def register(user : UserCreate, service:UserService = Depends(get_user_service)):
    registered_flag = service.get_user(user.email)
    if registered_flag is not None :
        raise HTTPException(status_code=409,detail="User already registered")
    user_register = service.register_user(user.email, user.username, user.password)
    
    return user_register

@router.post("/token",response_model=dict)
async def login(form : OAuth2PasswordRequestForm = Depends(), service : UserService = Depends(get_user_service)):
    user = service.login_user(form.username, form.password)
    if not user : 
        raise HTTPException(status_code=401, detail = "Incorrect credentials")
    token = create_access_token(
        data = {"sub" : str(user.id)}
    )
    return {"access_token" : token, "token_type" : "bearer"}





