# TODO: reply service (business logic)
from app.models.reply import ReplyCreate, ReplyResponse, ReplyUpdate
from app.repositories import replies_repository
from app.services import topics_service, users_service


def get_reply(reply_id: int) -> ReplyResponse | None:
    row = replies_repository.get_by_id(reply_id)
    if row is None:
        return None
    return ReplyResponse.from_query_result(*row)

def get_replies(topic_id: int) -> list[ReplyResponse]:
    #Waiting for topics_services.get_topic exists, so it can be called first
    #missing topic raises NotFoundError cause in this case it returns a empty list[]
    rows = replies_repository.get_by_topic(topic_id)
    return [ReplyResponse.from_query_result(*row) for row in rows]

def create_reply(topic_id: int, data: ReplyCreate, user_id: int) -> ReplyResponse:
    #for the first part i need the get topic again to be able to check if a topic exists
    #second i need to check if a topic is locked
    #3rd i need to check if a user is blocked

    reply_id = replies_repository.create_reply(data.content, topic_id, user_id)
    return get_reply(reply_id)

def delete_reply(user_id: int, reply_id, role: str) -> bool | None:
    reply = get_reply(reply_id)
    if reply is None:
        return None
    if reply.author_id != user_id and role != "admin":
        return False
    return replies_repository.delete_reply(reply_id)

def update_reply(user_id: int , reply_id: int, data: str):
    reply = get_reply(reply_id)
    if reply is None:
        return None
    if reply.author_id != user_id:
        return False
    #TODO: need to write a users_service.get_user check to see if user is blocked here
    return replies_repository.update_reply(reply_id)