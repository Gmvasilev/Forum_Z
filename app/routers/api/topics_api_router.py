from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status
from models.topic import Page, TopicListItem, TopicDetail, TopicListQuery, TopicCreate, TopicUpdate, TopicLockRequest, \
     TopicVisibilityRequest, BestReplyRequest
from services import topics_service


topics_api_router = APIRouter(prefix = '/topics', tags=["Topics"])


@topics_api_router.get("", response_model=Page[TopicListItem])
def list_topics(query: Annotated[TopicListQuery, Query()], user: dict = Depends()):
    return topics_service.get_all(query, user)


@topics_api_router.get("/{topic_id}", response_model=TopicDetail)
def get_topic(topic_id: int, user: dict = Depends()):
    topic = topics_service.get_topic(topic_id, user)
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Topic not found.")
    return topic


@topics_api_router.post("", response_model=TopicDetail, status_code=status.HTTP_201_CREATED)
def create_topic(data: TopicCreate, user: dict = Depends()):
    return topics_service.create_topic(user, data)


@topics_api_router.put("/{topic_id}", response_model=TopicDetail)
def update_topic(topic_id: int, data: TopicUpdate, user: dict = Depends()):
    update_result = topics_service.update_topic(topic_id, data, user)

    if update_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found.")
    if update_result is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to perform this action.")

    return update_result

@topics_api_router.delete("/{topic_id}", response_model=TopicDetail, status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(topic_id: int, user: dict = Depends()):
     delete_result = topics_service.delete_topic(topic_id, user)

     if delete_result is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Topic not found.")
     if delete_result is False:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permission to perform this action.")


# --------------------- state changes ----------------------------------------------------------------------------------


@topics_api_router.put("/{topic_id}/lock", response_model=TopicDetail)
def lock_topic(topic_id: int, data: TopicLockRequest, user: dict = Depends()):
    return topics_service.lock_topic(user, topic_id, data.is_locked)

#TODO Decide if there should be another endpoint to handle unlocking the topic or if both should be in one.

@topics_api_router.put("/{topic_id}/visibility", response_model=TopicDetail)
def set_topic_visibility(topic_id: int, data: TopicVisibilityRequest, user: dict = Depends()):
    topics_service.set_private(user, topic_id, data.is_private)

#TODO Decide if there should be another endpoint to handle setting public visibility of the topic or if both should be in one.

@topics_api_router.put("/{topic_id}/best-reply", response_model=TopicDetail)
def set_best_reply(topic_id: int, data: BestReplyRequest, user: dict = Depends()):
    return topics_service.set_best_reply(user, topic_id, data.reply_id)


@topics_api_router.delete("/{topic_id}/best-reply", response_model=TopicDetail,
                          status_code=status.HTTP_204_NO_CONTENT
                          )
def clear_best_reply(topic_id: int, user: dict = Depends()):
    topics_service.clear_best_reply(user, topic_id)