-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 17, 2014 at 05:53 PM
-- Server version: 5.5.35
-- PHP Version: 5.3.10-1ubuntu3.11

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `assassins`
--

-- --------------------------------------------------------

--
-- Table structure for table `Games`
--

CREATE TABLE IF NOT EXISTS `Games` (
  `game_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(15) NOT NULL,
  `location` varchar(50) NOT NULL,
  PRIMARY KEY (`game_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `Games`
--

INSERT INTO `Games` (`game_id`, `name`, `location`) VALUES
(17, 'Dylans Game', 'HHS'),
(18, 'Ryans Game', 'ISAT'),
(19, 'Alexs Game', 'HHS'),
(20, 'Ians Game', 'Quad'),
(21, 'Fake Game', 'JMU'),
(22, 'another game', 'VA'),
(23, 'Test Game', 'JMU'),
(24, 'Roberts Game', '3022'),
(25, 'Test Game 2', '3022'),
(26, 'Dr. Salibs Game', 'HHS 3022'),
(27, 'hello', 'hhs3022');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(20) NOT NULL,
  `lastname` varchar(20) NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `game_id` int(11) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `username` (`username`),
  KEY `game_id` (`game_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=31 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `firstname`, `lastname`, `username`, `password`, `game_id`) VALUES
(1, 'Ryan', 'Carter', 'rcarter', 'checkout', 17),
(25, '1', '1', '1', '1', 1),
(27, 'dylan', 'chance', 'dchance', 'password', 17),
(28, 'Barack', 'Obama', 'POTUS', 'POTUS', 0),
(30, 'dylantoo', 'too', 'dylan2', 'checkout', 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
