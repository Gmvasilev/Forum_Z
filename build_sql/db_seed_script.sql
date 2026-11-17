-- Seed data for forum_z_db
-- All seeded accounts use the dev password: Password123!
USE `forum_z_db`;

INSERT IGNORE INTO `user_roles` (`user_role_id`,`user_role`) VALUES (1,'admin'),(2,'user');

INSERT IGNORE INTO `topic_categories` (`category_id`,`category_name`) VALUES (1,'General Discussion'),(2,'Issues');

INSERT IGNORE INTO `users` (`user_id`,`first_name`,`last_name`,`username`,`password_hash`,`email`,`user_role_id`,`is_confirmed`) VALUES
  (1,'Admin','Forum','admin_z','$2b$12$uq7zTWW4Dn76UtOkexzZqO1eztG071jD6QA/76VXGlgfQ/USAiPKy','admin@forumz.test',1,1),
  (2,'Alex','Petrov','alex_p','$2b$12$vnPPbEm8LwKF6Bn9ZI1DVOUuBov/AQW60zsaB5re.X1xZ.V7ldeoW','alex.petrov@forumz.test',2,1),
  (3,'Maria','Ivanova','maria_i','$2b$12$CzZeCb5OCUKr7uoTlX.8P.ZGv/LHJeocvwDoPfQppRAPZwpeTOJ0y','maria.ivanova@forumz.test',2,1),
  (4,'Nikolay','Georgiev','niki_g','$2b$12$Ie/HgItGhgdLNbRuCYfhUeQThqbKuWlkuyGqY5C.H0q51hz3uS.Lq','nikolay.georgiev@forumz.test',2,1),
  (5,'Elena','Dimitrova','elena_d','$2b$12$dVosn0tH06.8BDNY5fVDiOLTWZE7UpJAcCvNo6qQBHDwgh6JCu6uy','elena.dimitrova@forumz.test',2,1);

INSERT IGNORE INTO `topics` (`topic_id`,`title`,`content`,`is_locked`,`is_private`,`author_id`,`category_id`,`created_at`) VALUES
  (1,'What are you playing this weekend?','Share what you are planning to play this weekend and why. I am trying to pick between a long RPG and something short.',0,0,2,1,'2026-11-01 10:00:00'),
  (2,'Game crashes on startup after the latest update','Since the last patch my game crashes to desktop right after the logo screen. Drivers are up to date and I already verified the game files.',0,0,3,2,'2026-11-03 18:30:00'),
  (3,'Best co-op games to play with friends','Looking for recommendations for co-op games that work well with 3 or 4 players and do not need hours of setup.',0,0,4,1,'2026-11-05 20:15:00'),
  (4,'Controller is not detected in big picture mode','My gamepad works in the system settings but is not detected inside the launcher big picture mode. Any ideas what could cause it?',1,0,5,2,'2026-11-07 09:45:00'),
  (5,'Planning our clan tournament schedule','Private thread for organizing the tournament. Please suggest dates and the game format so we can vote on them this week.',0,1,2,1,'2026-11-10 21:00:00');

INSERT IGNORE INTO `replies` (`reply_id`,`content`,`topic_id`,`author_id`,`created_at`) VALUES
  (1,'I will finally start the big RPG I have been postponing.',1,3,'2026-11-01 11:00:00'),
  (2,'Probably some relaxing farming sim, I need a break.',1,4,'2026-11-01 12:20:00'),
  (3,'Try running the launcher as administrator and disable overlays.',2,4,'2026-11-03 19:10:00'),
  (4,'Rolling back the graphics driver fixed the same crash for me.',2,5,'2026-11-03 20:05:00'),
  (5,'Thanks, the driver rollback worked. Marking it as best reply!',2,3,'2026-11-04 08:30:00'),
  (6,'Any of the survival co-op games work great with four players.',3,2,'2026-11-05 21:00:00'),
  (7,'Racing and party games are the easiest to set up.',3,5,'2026-11-06 10:40:00'),
  (8,'Have you tried unplugging other USB devices first?',4,2,'2026-11-07 10:30:00'),
  (9,'Saturday evening works best for me.',5,3,'2026-11-10 22:10:00');

-- Best replies (set after replies exist because of the composite FK)
UPDATE `topics` SET `best_reply_id` = 5 WHERE `topic_id` = 2;
UPDATE `topics` SET `best_reply_id` = 6 WHERE `topic_id` = 3;

-- reaction: 1 = like, 0 = dislike
INSERT IGNORE INTO `reactions` (`user_id`,`reply_id`,`reaction`) VALUES
  (2,5,1),
  (4,5,1),
  (5,5,1),
  (3,6,1),
  (5,6,1),
  (4,3,1),
  (2,4,1),
  (3,7,1),
  (5,2,0),
  (2,1,1),
  (4,1,0);

INSERT IGNORE INTO `topics_invited_users` (`topic_id`,`user_id`,`is_accepted`,`answered_at`) VALUES
  (5,3,1,'2026-11-10 22:00:00'),
  (5,4,0,NULL),
  (5,5,0,'2026-11-11 08:00:00');
