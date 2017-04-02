# Setup the database of questions
CREATE DATABASE ahhh_data;
USE ahhh_data;
CREATE TABLE questions(
  QuestionID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  string VARCHAR(2000) NOT NULL,
  upvotes INT NOT NULL,
  posted_time TIMESTAMP,
  namespace VARCHAR(200) NOT NULL,
  answered TINYINT(1)
);

# Setup the database of admins
CREATE DATABASE ahhh_admins;
USE ahhh_admins;
CREATE TABLE admins(
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  admin_pass VARCHAR(6) NOT NULL,
  namespace VARCHAR(200) NOT NULL
);
