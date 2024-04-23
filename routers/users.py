from fastapi import APIRouter, status

from common.responses import BadRequest
from data.models import UserCreate
from services import user_service

users_router = APIRouter(prefix='/users')


@users_router.post('/register', status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate):
    new_user = user_service.create(user_create.email, user_create.username, user_create.password)

    return new_user or BadRequest(f'Username or email is already taken.')


