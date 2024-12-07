CREATE DATABASE db_project;
USE db_project;

# admin 1234
INSERT INTO users (username, password)
VALUES ('admin', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

SELECT * FROM users;

CREATE TABLE users (
 id INT AUTO_INCREMENT PRIMARY KEY,
 username VARCHAR(255) NOT NULL UNIQUE,
 password VARCHAR(64) NOT NULL
);



