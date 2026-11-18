# TODO: reply repository (raw SQL)
#Here is pure sql and return a result from sql cursor as a List of tuples with possiblity of minor modification
from app.data.database import read_query,insert_query,update_query,delete_query

def get_by_topic(topic_id: int):
    return read_query(
        """
        SELECT r.reply_id, r.topic_id, r.author_id,
            u.username,r.content,r.created_at,
            COUNT(CASE WHEN rx.reaction = TRUE THEN 1 END) AS likes,
            COUNT(CASE WHEN rx.reaction = FALSE THEN 1 END) AS dislikes
        FROM replies r 
        JOIN users u ON u.user_id = r.author_id
        LEFT JOIN reactions rx ON rx.reply_id = r.reply_id
        WHERE r.topic_id = ?
        GROUP BY r.reply_id, r.topic_id, r.author_id,
            u.username,r.content,r.created_at
        ORDER BY r.created_at, r.reply_id
        """,
        (topic_id,)

    )

def get_by_id(reply_id: int):
    rows = read_query(
        """
        SELECT r.reply_id, r.topic_id, r.author_id,
            u.username,r.content,r.created_at,
            COUNT(CASE WHEN rx.reaction = TRUE THEN 1 END) AS likes,
            COUNT(CASE WHEN rx.reaction = FALSE THEN 1 END) AS dislikes
        FROM replies r 
        JOIN users u ON u.user_id = r.author_id
        LEFT JOIN reactions rx ON rx.reply_id = r.reply_id
        WHERE r.reply_id = ?
        GROUP BY r.reply_id, r.topic_id, r.author_id,
            u.username,r.content,r.created_at
        """,
        (reply_id,)

    )
    return rows[0] if rows else None
    