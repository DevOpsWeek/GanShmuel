--
-- Database: `billdb`
--

CREATE DATABASE IF NOT EXISTS `billdb`;
USE `billdb`;

-- --------------------------------------------------------

--
-- Table structure
--

CREATE TABLE IF NOT EXISTS `Providers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `Rates` (
  `product_id` varchar(50) NOT NULL,
  `rate` int(11) DEFAULT 0,
  `scope` varchar(50) DEFAULT NULL,
  FOREIGN KEY (scope) REFERENCES `Providers`(`id`)
) ENGINE=MyISAM ;

CREATE TABLE IF NOT EXISTS `Trucks` (
  `id` varchar(10) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`provider_id`) REFERENCES `Providers`(`id`)
) ENGINE=MyISAM ;


-- Dumping data

--
INSERT INTO Providers (`id`,`provider_name`) VALUES (1,'pro1'),
(2, 'pro2');

INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES ('1', 2, 'ALL'),
('2', 4, 'pro1');

INSERT INTO Trucks (`id`, `provider_id`) VALUES ('134-33-443', 2),
('222-33-111', 1);

