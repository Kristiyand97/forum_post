from fastapi import APIRouter, status, Depends, HTTPException

from common import authorization
from data import schemas
from services import topic_services

topics_router = APIRouter(prefix='/topics')


@topics_router.get('/')
def get_all_topics(search: str = None, sort: str = None, pagination: int = None):
    topics_result = topic_services.get_all_topics(search, sort, pagination)

    if topics_result == 'wrong search parameter':
        raise HTTPException(status_code=404,
                            detail=f"Topic 'search' parameter is wrong, try with existing topic name!")
    elif topics_result == 'wrong sort parameter':
        raise HTTPException(status_code=404,
                            detail=f"Topic 'sort' parameter is wrong, try 'asc' or 'desc'")

    return topics_result


@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int):
    topic_result = topic_services.get_topic_by_id(topic_id)

    if topic_result == 'wrong topic id':
        raise HTTPException(status_code=404, detail=f"Topic with id: {topic_result} does not exist!")

    return topic_result


@topics_router.post('/create', status_code=status.HTTP_201_CREATED)
def create_topic(topic: schemas.TopicCreate, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_topic = topic_services.create(topic.name, topic.category_id, current_user)

    if new_topic is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The topic could not be created.")

    return new_topic.dict(exclude_none=True)
