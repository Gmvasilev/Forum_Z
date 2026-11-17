

--  Order of table creation
-- 1. user_roles
-- 2. topic_categories
-- 3. users
-- 4. topics
-- 5. replies
-- 6. reactions
-- 7. topics_invited_users
-- 9. Triggers
-- 10.Final foreign key via ALTER TABLE

--*************************************************
--************ CREATE TABLE user_roles ************
--*************************************************

CREATE TABLE user_roles(
	user_role_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	user_role VARCHAR(52) NOT NULL,
	
	PRIMARY KEY (user_role_id),
	CONSTRAINT uq_user_role UNIQUE(user_role)
);



--*******************************************************
--************ CREATE TABLE topic_categories ************
--*******************************************************

CREATE TABLE topic_categories(
    category_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(32) NOT NULL,

    PRIMARY KEY (category_id),
    CONSTRAINT uq_category_name UNIQUE (category_name)
);



--********************************************
--************ CREATE TABLE users ************
--********************************************

CREATE TABLE users(
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,

    username VARCHAR(16)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci
        NOT NULL,

    password_hash VARCHAR(255) NOT NULL,

    email VARCHAR(254)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_general1400_as_ci
        NOT NULL,

    user_role_id INT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_confirmed BOOL NOT NULL DEFAULT FALSE,
    is_deactivated BOOL NOT NULL DEFAULT FALSE,

	PRIMARY KEY (user_id),
	CONSTRAINT uq_username UNIQUE (username),
	CONSTRAINT uq_email UNIQUE (email),
	
	CONSTRAINT FK_users_have_role
		FOREIGN KEY (user_role_id)
		REFERENCES user_roles(user_role_id),

	CONSTRAINT chck_firstname_length
		CHECK (CHAR_LENGTH(first_name) BETWEEN 2 AND 32),
		
	CONSTRAINT chck_lastname_length
		CHECK (CHAR_LENGTH(last_name) BETWEEN 2 AND 32),
		

	CONSTRAINT chck_username_length
	   CHECK (CHAR_LENGTH(username) BETWEEN 2 AND 16),

    CONSTRAINT chck_password_hash_length_bcrypt
        CHECK (CHAR_LENGTH(password_hash) = 60),

    CONSTRAINT chck_username_format
        CHECK (username REGEXP '^[A-Za-z0-9_]+$'), 
	   

	CONSTRAINT chk_email_length
   	    CHECK (CHAR_LENGTH(email) BETWEEN 6 AND 254),

   CONSTRAINT chk_email_format
   	CHECK (
      	email REGEXP
        '^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)+$'
   	),

	CONSTRAINT chk_email_no_consecutive_dots
   	CHECK (email NOT REGEXP '\\.\\.')
);



--*********************************************
--************ CREATE TABLE topics ************
--*********************************************

CREATE TABLE topics(
	topic_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	title VARCHAR(128) NOT NULL,
	content TEXT(8192) NOT NULL,
	is_locked BOOL NOT NULL DEFAULT FALSE,
	is_private BOOL NOT NULL DEFAULT FALSE,
	author_id INT UNSIGNED NOT NULL,
	category_id INT UNSIGNED NOT NULL,
	best_reply_id INT UNSIGNED DEFAULT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	
	
	PRIMARY KEY (topic_id),
		
	CONSTRAINT FK_topics_have_author
		FOREIGN KEY (author_id)
		REFERENCES users(user_id),
	
	CONSTRAINT FK_topics_have_category
		FOREIGN KEY (category_id)
		REFERENCES topic_categories(category_id),
	
	CONSTRAINT check_title_length
		CHECK(CHAR_LENGTH(title) BETWEEN 16 AND 128),
		
	CONSTRAINT check_content_length
		CHECK(CHAR_LENGTH(content) BETWEEN 32 AND 8192)
);



--**********************************************
--************ CREATE TABLE replies ************
--**********************************************

CREATE TABLE replies(
    reply_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    content TEXT(8192) NOT NULL,
    topic_id INT UNSIGNED NOT NULL,
    author_id INT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (reply_id),

    CONSTRAINT uq_topic_reply        -- Added to ensure topic's FK for best reply
        UNIQUE (topic_id, reply_id), -- is actually a reply on that topic.

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




--************************************************
--************ CREATE TABLE reactions ************
--************************************************

CREATE TABLE reactions(
    user_id INT UNSIGNED NOT NULL,
    reply_id INT UNSIGNED NOT NULL,
    reaction BOOLEAN NOT NULL,

    PRIMARY KEY (user_id, reply_id),

    CONSTRAINT fk_reactions_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reactions_reply
        FOREIGN KEY (reply_id) REFERENCES replies(reply_id)
        ON DELETE CASCADE
);



--************************************************************
--************ CREATE TABLE topics_invited_users ************
--************************************************************

CREATE TABLE topics_invited_users(
	topic_id INT UNSIGNED NOT NULL,
	user_id INT UNSIGNED NOT NULL,
    is_accepted BOOLEAN DEFAULT FALSE,
	answered_at DATETIME DEFAULT NULL,

	PRIMARY KEY (topic_id, user_id),
	
	CONSTRAINT FK_topics_users_have_topic
		FOREIGN KEY (topic_id)
		REFERENCES topics(topic_id),
	
	CONSTRAINT FK_topics_users_have_user
		FOREIGN KEY (user_id)
		REFERENCES users(user_id)
);



--***********************************************************
--     *** *** *** *** ADDITIONAL *** *** *** *** ***
--***********************************************************

-- *** TRIGGER: prevent username column change
DELIMITER //

CREATE TRIGGER prevent_username_change
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF CAST(OLD.username AS BINARY) <>
       CAST(NEW.username AS BINARY) THEN

        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Username cannot be changed after registration';

    END IF;
END//

DELIMITER ;



-- *** TRIGGER: set topic's best_reply to NULL
-- ***********  , when that reply is being deleted
DELIMITER //

CREATE TRIGGER before_reply_delete
BEFORE DELETE ON replies
FOR EACH ROW
BEGIN
    UPDATE topics
    SET best_reply_id = NULL
    WHERE topic_id = OLD.topic_id
      AND best_reply_id = OLD.reply_id;
END//

DELIMITER ;



-- *** CONSTRAINT FK_topic_best_reply

ALTER TABLE topics
    ADD CONSTRAINT FK_topic_has_best_reply
    FOREIGN KEY (topic_id, best_reply_id)
    REFERENCES replies(topic_id, reply_id)
;




