from typing import Annotated

from fastapi import APIRouter, Depends, status,HTTPException

from app.models.reply import ReplyCreate, ReplyResponse, ReplyUpdate
from app.routers.dependencies import get_current_user
from app.services import replies_service

replies_api_router = APIRouter(prefix="/api", tags=["Replies"])

@replies_api_router.get("/topics/{topic_id}/replies", response_model=list[ReplyResponse])
def get_topic_replies(topic_id: int):
    return replies_service.get_replies(topic_id)

@replies_api_router.get("/replies/{replies_id}", response_model=ReplyResponse)
def get_reply(reply_id: id):
    reply = replies_service.get_reply(reply_id)
    if reply is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reply Not found")

    return reply

@replies_api_router.post("/topic/{topic_id}/replies", response_model=ReplyResponse,status_code=status.HTTP_201_CREATED,)
def create_reply(topic_id: int, data: ReplyCreate, current_user: dict = Depends()):
    #the depends needs a requre user function 
    #get_current_user returns None or False instead of failing, which is right for public pages. Write endpoints need a stricter one:
    #topic_is locked validation still needs to be writen
    return replies_service.create_reply(topic_id,data,current_user["user_id"])