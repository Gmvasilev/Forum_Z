from typing import Annotated

from fastapi import APIRouter, Depends, status,HTTPException

from models.reply import ReplyCreate, ReplyResponse, ReplyUpdate
from routers.dependencies import get_current_user
from services import replies_service

replies_api_router = APIRouter(prefix="/api", tags=["Replies"])

@replies_api_router.get("/topics/{topic_id}/replies", response_model=list[ReplyResponse])
def get_topic_replies(topic_id: int):
    return replies_service.get_replies(topic_id)

@replies_api_router.get("/replies/{reply_id}", response_model=ReplyResponse)
def get_reply(reply_id: int):
    reply = replies_service.get_reply(reply_id)
    if reply is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reply Not found")

    return reply

@replies_api_router.post("/topics/{topic_id}/replies", response_model=ReplyResponse,status_code=status.HTTP_201_CREATED)
def create_reply(topic_id: int, data: ReplyCreate, current_user: dict = Depends()):
    #the depends needs a requre user function 
    #get_current_user returns None or False instead of failing, which is right for public pages. Write endpoints need a stricter one:
    #topic_is locked validation still needs to be writen
    return replies_service.create_reply(topic_id,data,current_user["user_id"])

@replies_api_router.delete("/replies/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reply(reply_id: int,current_user: dict = Depends()):
    #need a current_user function to implement the check for the author
    result = replies_service.delete_reply(current_user["user_id"], reply_id, current_user["role"])

    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Reply not Found")
    if result is False:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not allowed to delete this reply")

@replies_api_router.patch("/replies/{reply_id}", response_model=ReplyResponse)
def update_reply(reply_id: int, data: ReplyUpdate, current_user: dict = Depends()):
    result = replies_service.update_reply(current_user["user_id"], reply_id, data)

    if result is None:
        raise HTTPException(404, detail="Reply not found")
    if result is False:
        raise HTTPException(403, detail="You can only edit your own replies")

    return result