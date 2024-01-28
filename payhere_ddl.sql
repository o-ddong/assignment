-- 유저 테이블 --
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `name` varchar(15) NOT NULL,
  `mdn` varchar(64) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mdn` (`mdn`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 상품 테이블 --
CREATE TABLE `billings_product` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `category` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `cost` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `barcode` varchar(50) NOT NULL,
  `expire_date` date NOT NULL,
  `size` int(11) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billings_product_user_id_0000001_fk_user_id` (`user_id`),
  CONSTRAINT `billings_product_user_id_0000001_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
