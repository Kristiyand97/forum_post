from fastapi import APIRouter, Depends, HTTPException, status

from common import authorization
from data.schemas import ReplyCreate
from services import reply_services

replies_router = APIRouter(prefix='/replies')


@replies_router.post('/create', status_code=status.HTTP_201_CREATED)
def create_reply(reply: ReplyCreate, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_reply = reply_services.create(reply.content, reply.topic_id, current_user)

    if new_reply is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The reply could not be created.")

    return new_reply.dict(exclude_none=True)
