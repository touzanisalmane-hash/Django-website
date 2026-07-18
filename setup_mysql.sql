-- Script to create the database and user for the NOVA STORE project on
-- XAMPP (MariaDB).
--
-- How to use it on XAMPP (Windows/macOS/Linux):
--   1) Open the XAMPP Control Panel and start the MySQL service
--      (it actually runs MariaDB).
--   2) Open phpMyAdmin in your browser: http://localhost/phpmyadmin
--   3) Go to the "SQL" tab at the top, paste the full contents of this
--      file, then click "Go".
--
-- Or from the command line (if mysql.exe is available in
-- XAMPP\mysql\bin):
--   "C:\xampp\mysql\bin\mysql.exe" -u root < setup_mysql.sql

CREATE DATABASE IF NOT EXISTS ecommerce_en_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'ecommerce_user'@'localhost' IDENTIFIED BY 'ecommerce_pass123';
CREATE USER IF NOT EXISTS 'ecommerce_user'@'127.0.0.1' IDENTIFIED BY 'ecommerce_pass123';

GRANT ALL PRIVILEGES ON ecommerce_en_db.* TO 'ecommerce_user'@'localhost';
GRANT ALL PRIVILEGES ON ecommerce_en_db.* TO 'ecommerce_user'@'127.0.0.1';

FLUSH PRIVILEGES;
