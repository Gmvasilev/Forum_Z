# TODO: reply service (business logic)
from app.models.reply import ReplyCreate, ReplyResponse, ReplyUpdate
from app.repositories import replies_repository
from app.services import topics_service, users_service

def get_replies(topic_id: int) -> list[ReplyResponse]:
    #Waiting for topics_services.get_topic exists, so it can be called first
    #missing topic raises NotFoundError cause in this case it returns a empty list[]
    rows = replies_repository.get_by_topic(topic_id)
    return [ReplyResponse.from_query_result(*row) for row in rows]