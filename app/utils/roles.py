from enum import Enum
from fastapi import HTTPException, Depends
from app.models import User
from app.utils.oauth2 import get_current_user
from typing import List
import logging

logger = logging.getLogger(__name__)

class Role(Enum):
    ADMIN:str = 'admin'
    USER:str = 'user'

class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")


