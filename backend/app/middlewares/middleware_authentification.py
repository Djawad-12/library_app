from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.core.dependancies import get_user_service
from app.domains.user.user_service import UserService
from fastapi.security import OAuth2PasswordBearer
import dotenv
import os

dotenv.load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(get_user_service)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        db_id: str = payload.get("sub")
        if db_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = service.get_user_by_db_id(int(db_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user.id