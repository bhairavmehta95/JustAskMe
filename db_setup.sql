# Setup the database of questions
CREATE DATABASE ahhh_db;
USE ahhh_db;
CREATE TABLE questions(
  QuestionID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  string VARCHAR(2000) NOT NULL,
  upvotes INT NOT NULL,
  posted_time TIMESTAMP,
  namespace VARCHAR(200) NOT NULL,
  answered TINYINT(1)
);

CREATE TABLE admins(
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  admin_number INT UNSIGNED NOT NULL,
  namespace VARCHAR(200) NOT NULL
);