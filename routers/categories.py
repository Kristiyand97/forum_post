from fastapi import APIRouter, status, Depends, HTTPException

from common import authorization
from data import schemas
from data.schemas import CreateCategory
from services import category_services

categories_router = APIRouter(prefix='/categories')


@categories_router.post('/create', status_code=status.HTTP_201_CREATED)
def create_category(category: CreateCategory, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_category = category_services.create(category.name, category.is_private, category.is_locked)

    if new_category is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The topic could not be created.")

    return new_category.dict(exclude_none=True)
