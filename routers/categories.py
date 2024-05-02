from fastapi import APIRouter, status, Depends, HTTPException

from common import authorization
from data import schemas
from data.schemas import CreateCategory, ChangeCategoryVisibility
from services import category_services

categories_router = APIRouter(prefix='/categories')


@categories_router.get('/')
def view_all_categories():
    categories = category_services.view_all_categories()
    return categories


@categories_router.get('/{category_id}')
def view_category(category_id: int, search: str = None, sort: str = None, pagination: int = None):
    category_with_topics = category_services.view_topics_in_category(category_id, search, sort, pagination)

    if not category_with_topics:
        raise HTTPException(status_code=404, detail=category_with_topics)
    elif category_with_topics == 'wrong search parameter':
        raise HTTPException(status_code=404, detail=f"Topic with name: '{search}' does not exist!")
    elif category_with_topics == 'wrong sort parameter':
        raise HTTPException(status_code=404, detail=f"Sort parameter: '{sort}' is wrong, try 'desc' or 'asc'")

    return category_with_topics


@categories_router.post('/create', status_code=status.HTTP_201_CREATED)
def create_category(category: CreateCategory, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_category = category_services.create(category.name, category.is_private, category.is_locked, current_user)

    if new_category is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The topic could not be created.")
    elif new_category == 'not admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Creating a category requires ADMIN access!")

    return new_category.dict(exclude_none=True)


@categories_router.put('/{category_id}')
def change_visibility(category_id: int, change_category: schemas.ChangeCategoryVisibility,
                      current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    category_visibility = category_services.change_visibility(category_id, change_category.is_private,
                                                              change_category.is_locked,
                                                              current_user)
    if not category_visibility:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot change category visibility!')
    elif category_visibility == 'not admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only ADMIN users can change category visibility!')

    return f'Visibility on Category with id: {category_id} is successfully changed!'
