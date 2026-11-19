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