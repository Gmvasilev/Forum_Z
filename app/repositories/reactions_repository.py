from app.data.database import read_query,insert_query,update_query,delete_query
from app.models.reactions import StoredReaction, ReactionType


def get_reaction(user_id: int, reply_id: int) -> StoredReaction | None:
    rows = read_query('''
                      SELECT user_id, reply_id FROM reactions
                      WHERE user_id = ? and reply_id = ?''',
                      (user_id, reply_id))

    if not rows:
        return None

    uid, rid, value = rows[0]

    return StoredReaction(
        user_id=uid,
        reply_id=rid,
        reaction_type=ReactionType.from_db(value)
    )

def create_reaction(user_id: int, reply_id: int, reaction_type: ReactionType) -> int:
    return insert_query(
        '''INSERT INTO reactions (user_id,reply_id,reaction) VALUES (?,?,?)''',
        (user_id, reply_id, reaction_type.value))


def update_reaction(user_id: int, reply_id: int, reaction_type: ReactionType) -> int:
    return update_query(
        '''UPDATE reactions SET reaction = ? WHERE user_id = ? AND reply_id = ?''',
        (reaction_type.to_db(), user_id, reply_id)
    )


def delete_reaction(user_id: int, reply_id: int) -> bool:
    return delete_query(
        '''DELETE FROM reactions WHERE user_id = ? AND reply_id = ?''',
        (user_id, reply_id))


def counts_for_reply(reply_id: int) -> tuple[int, int]:
    rows = read_query(
        '''SELECT COALESCE(SUM(reaction = 1),0), COALESCE(SUM(reaction = 0),0) 
           FROM reactions WHERE reply_id = ?''',
           (reply_id,)
    )

    likes, dislikes = rows[0]

    return int(likes), int(dislikes)


def counts_for_topic(topic_id: int) -> dict[int, tuple[int, int]]:
    rows = read_query(
        '''SELECT r.reply_id,
                COALESCE(SUM(rx.reaction = 1),0),
                COALESCE(SUM(rx.reaction = 0),0)
           FROM replies r
           LEFT JOIN reactions rx ON rx.reply_id = r.reply_id 
           WHERE r.topic_id = ?
           GROUP BY r.reply_id''',
        (topic_id,)
    )
    return {rid: (int(likes), int(dislikes)) for rid, likes, dislikes in rows}


def user_reactions_for_topic(user_id: int, topic_id: int) -> dict[int, ReactionType]:
    rows = read_query(
        '''SELECT rx.reply_id, rx.reaction
           FROM reactions rx
           JOIN replies r ON rx.reply_id = r.reply_id 
           WHERE r.topic_id = ? AND rx.user_id = ?''',
        (topic_id, user_id)
    )

    return {rid: ReactionType.from_db(value) for rid, value in rows}