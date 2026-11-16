-- TODO: CREATE DATABASE / CREATE TABLE statements

CREATE TABLE replies(
    reply_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    content VARCHAR(8192) NOT NULL,
    topic_id INT UNSIGNED NOT NULL,
    author_id INT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (reply_id),

    CONSTRAINT FK_replies_have_topic
        FOREIGN KEY (topic_id)
        REFERENCES topics(topic_id)
        ON DELETE CASCADE,

    CONSTRAINT FK_replies_have_author
        FOREIGN KEY (author_id)
        REFERENCES users(user_id),

    CONSTRAINT chk_reply_content_length
        CHECK (CHAR_LENGTH(content) BETWEEN 2 AND 8192)
);

CREATE TABLE topic_categories(
    category_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(32) NOT NULL,

    PRIMARY KEY (category_id),
    CONSTRAINT uq_category_name UNIQUE (category_name)
);

INSERT INTO topic_categories (category_name) VALUES ('General Discussion'),('Issue')

CREATE TABLE reactions(
    user_id INT NOT NULL,
    reply_id INT NOT NULL,
    reaction BOOLEAN NOT NULL,
    PRIMARY KEY (user_id,reply_id),
    CONSTRAINT fk_reactions_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reactions_reply
        FOREIGN KEY (reply_id) REFERENCES replies(reply_id)
        ON DELETE CASCADE
);