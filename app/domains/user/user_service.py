from .user_db_model import User
from .user_repository import UserRepository
from typing import List
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta, timezone
import dotenv
import os
dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))




pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash_password(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password :str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)








class UserService:
    def __init__(self, repo : UserRepository):
        self.repo = repo 

    def get_all_users(self) -> List[User]:
        return self.repo.get_all_users()
    
    def get_user(self,identifier : str) -> User :
        return self.repo.get_user_by_id(identifier)
    
    def register_user(self, email :str, username: str, password: str) -> User:
        user = self.repo.get_user_by_id(email)
        if user is not None :
            return None
        
        hashed_password = hash_password(password)
        user = User(
            email = email,
            username = username,
            password = hashed_password
        )
        
        return self.repo.create_user(user)
    
    
    def login_user(self,identifier:str, password :str) -> User | None:
        user = self.repo.get_user_by_id(identifier)
        if user is None :
            return None
        if not verify_password(password, user.password):
            return None

        return user
        

                            
    


