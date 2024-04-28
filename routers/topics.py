from fastapi import APIRouter, status, Depends, HTTPException

from common import authentication
from data import schemas
from services import topic_services

topics_router = APIRouter(prefix='/topics')


@topics_router.post('/create', status_code=status.HTTP_201_CREATED)
def create_topic(topic: schemas.TopicCreate, current_user: int = Depends(authentication.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_topic = topic_services.create(topic.name, topic.category_id, current_user)

    if new_topic is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The topic could not be created.")

    return new_topic.dict(exclude_none=True)
