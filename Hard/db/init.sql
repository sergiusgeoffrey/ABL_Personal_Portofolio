
CREATE DATABASE student_papers;
use student_papers;

CREATE TABLE `user` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `paper` (
    `id_uploader` VARCHAR(255) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `path` VARCHAR(255) NOT NULL,
    `abstract` TEXT NOT NULL,
    FOREIGN KEY (id_uploader) REFERENCES user(id)
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert  into `user`(`id`,`name`,`email`,`password`) values 
('C14190024','Sergius Geoffrey','sergius.geoffrey@gmail.com','test');