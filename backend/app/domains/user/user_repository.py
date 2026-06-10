from sqlalchemy.orm import Session
from typing import List
from .user_db_model import User
from sqlalchemy import or_

class UserRepository:
    def __init__(self, db: Session):
        self.db = db 

    def get_all_users(self) -> List[User] :
        return self.db.query(User).all()
    
    def get_user_by_db_id(self, user_id : int) -> User :
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_id(self,  user_id : str) -> User :
        return self.db.query(User).filter(or_(User.email == user_id, User.username == user_id)).first()

    def create_user(self, user: User) -> User :
        self.db.add(user)
        self.db.commit()
        return user
    

    


    



