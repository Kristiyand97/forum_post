from fastapi import APIRouter, status, HTTPException
import services.user_service
from common.authentication import create_access_token
# from common.authentication import create_access_token
from common.responses import BadRequest
from data.schemas import UserCreate, UserOut, UserLogin
from security.password_hashing import get_password_hash, verify_password
from services import user_service

users_router = APIRouter(prefix='/users')


@users_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def register(user_create: UserCreate):
    hashed_password = get_password_hash(user_create.password)
    user_create.password = hashed_password

    new_user = user_service.create(user_create.email, user_create.username, user_create.password)

    return new_user or BadRequest(f'Username or email is already taken.')


@users_router.post('/login')
def login(user_credentials: UserLogin):

    user = services.user_service.try_login(user_credentials.email, user_credentials.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}