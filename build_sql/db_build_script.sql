-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               12.3.3-MariaDB - MariaDB Server
-- Server OS:                    Win64
-- HeidiSQL Version:             12.21.0.7344
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for forum_z_db
CREATE DATABASE IF NOT EXISTS `forum_z_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `forum_z_db`;

-- Dumping structure for table forum_z_db.reactions
CREATE TABLE IF NOT EXISTS `reactions` (
  `user_id` int(10) unsigned NOT NULL,
  `reply_id` int(10) unsigned NOT NULL,
  `reaction` tinyint(1) NOT NULL,
  PRIMARY KEY (`user_id`,`reply_id`),
  KEY `fk_reactions_reply` (`reply_id`),
  CONSTRAINT `fk_reactions_reply` FOREIGN KEY (`reply_id`) REFERENCES `replies` (`reply_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_reactions_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table forum_z_db.reactions: ~0 rows (approximately)

-- Dumping structure for table forum_z_db.replies
CREATE TABLE IF NOT EXISTS `replies` (
  `reply_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `topic_id` int(10) unsigned NOT NULL,
  `author_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`reply_id`),
  UNIQUE KEY `uq_topic_reply` (`topic_id`,`reply_id`),
  KEY `FK_replies_have_author` (`author_id`),
  CONSTRAINT `FK_replies_have_author` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FK_replies_have_topic` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`) ON DELETE CASCADE,
  CONSTRAINT `chk_reply_content_length` CHECK (char_length(`content`) between 2 and 8192)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table forum_z_db.replies: ~0 rows (approximately)

-- Dumping structure for table forum_z_db.topic_categories
CREATE TABLE IF NOT EXISTS `topic_categories` (
  `category_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `category_name` varchar(32) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `uq_category_name` (`category_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table forum_z_db.topic_categories: ~0 rows (approximately)

-- Dumping structure for table forum_z_db.topics
CREATE TABLE IF NOT EXISTS `topics` (
  `topic_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `content` text NOT NULL,
  `is_locked` tinyint(1) NOT NULL DEFAULT 0,
  `is_private` tinyint(1) NOT NULL DEFAULT 0,
  `author_id` int(10) unsigned NOT NULL,
  `category_id` int(10) unsigned NOT NULL,
  `best_reply_id` int(10) unsigned DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`topic_id`),
  KEY `FK_topics_have_author` (`author_id`),
  KEY `FK_topics_have_category` (`category_id`),
  KEY `FK_topic_has_best_reply` (`topic_id`,`best_reply_id`),
  CONSTRAINT `FK_topic_has_best_reply` FOREIGN KEY (`topic_id`, `best_reply_id`) REFERENCES `replies` (`topic_id`, `reply_id`),
  CONSTRAINT `FK_topics_have_author` FOREIGN KEY (`author_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FK_topics_have_category` FOREIGN KEY (`category_id`) REFERENCES `topic_categories` (`category_id`),
  CONSTRAINT `check_title_length` CHECK (char_length(`title`) between 16 and 128),
  CONSTRAINT `check_content_length` CHECK (char_length(`content`) between 32 and 8192)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table forum_z_db.topics: ~0 rows (approximately)

-- Dumping structure for table forum_z_db.topics_invited_users
CREATE TABLE IF NOT EXISTS `topics_invited_users` (
  `topic_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `is_accepted` tinyint(1) DEFAULT 0,
  `answered_at` datetime DEFAULT NULL,
  PRIMARY KEY (`topic_id`,`user_id`),
  KEY `FK_topics_users_have_user` (`user_id`),
  CONSTRAINT `FK_topics_users_have_topic` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`),
  CONSTRAINT `FK_topics_users_have_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table forum_z_db.topics_invited_users: ~0 rows (approximately)

-- Dumping structure for table forum_z_db.user_roles
CREATE TABLE IF NOT EXISTS `user_roles` (
  `user_role_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_role` varchar(52) NOT NULL,
  PRIMARY KEY (`user_role_id`),
  UNIQUE KEY `uq_user_role` (`user_role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table forum_z_db.user_roles: ~0 rows (approximately)

-- Dumping structure for table forum_z_db.users
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `username` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general1400_as_ci NOT NULL,
  `user_role_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `is_confirmed` tinyint(1) NOT NULL DEFAULT 0,
  `is_deactivated` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `uq_username` (`username`),
  UNIQUE KEY `uq_email` (`email`),
  KEY `FK_users_have_role` (`user_role_id`),
  CONSTRAINT `FK_users_have_role` FOREIGN KEY (`user_role_id`) REFERENCES `user_roles` (`user_role_id`),
  CONSTRAINT `chck_firstname_length` CHECK (char_length(`first_name`) between 2 and 32),
  CONSTRAINT `chck_lastname_length` CHECK (char_length(`last_name`) between 2 and 32),
  CONSTRAINT `chck_username_length` CHECK (char_length(`username`) between 2 and 16),
  CONSTRAINT `chck_username_format` CHECK (`username` regexp '^[A-Za-z0-9_]+$'),
  CONSTRAINT `chk_email_length` CHECK (char_length(`email`) between 6 and 254),
  CONSTRAINT `chk_email_format` CHECK (`email` regexp '^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)+$'),
  CONSTRAINT `chk_email_no_consecutive_dots` CHECK (!(`email` regexp '\\.\\.'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table forum_z_db.users: ~0 rows (approximately)

-- Dumping structure for trigger forum_z_db.before_reply_delete
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
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
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger forum_z_db.prevent_username_change
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
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
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
