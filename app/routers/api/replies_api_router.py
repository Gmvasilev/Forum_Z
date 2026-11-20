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