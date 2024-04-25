-- Create a table 
CREATE TABLE IF NOT EXISTS users (
	id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email CHAR(255) UNIQUE NOT NULL,
	name CHAR(255),
	country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);