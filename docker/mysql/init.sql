CREATE DATABASE IF NOT EXISTS tapandchew_kitchen
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

GRANT ALL PRIVILEGES ON tapandchew_kitchen.* TO 'root'@'%';
FLUSH PRIVILEGES;