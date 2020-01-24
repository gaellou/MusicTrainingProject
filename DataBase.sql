-- phpMyAdmin SQL Dump
-- version 5.1.0-dev
-- https://www.phpmyadmin.net/
--
-- Host: 192.168.30.23
-- Generation Time: Jan 22, 2020 at 03:43 PM
-- Server version: 8.0.18
-- PHP Version: 7.4.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `MusicTraining`
--

-- --------------------------------------------------------

--
-- Table structure for table `Activity`
--

CREATE TABLE `Activity` (
  `Id` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Activity`
--

INSERT INTO `Activity` (`Id`, `Name`) VALUES
(1, 'Warmup'),
(2, 'Training');

-- --------------------------------------------------------


--
-- Table structure for table `Instrument`
--

CREATE TABLE `Instrument` (
  `Id` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Instrument`
--

INSERT INTO `Instrument` (`Id`, `Name`) VALUES
(1, 'Trumpet'),
(2, 'Flute'),
(3, 'Violin'),
(4, 'Clarinet'),
COMMIT;

--
-- Table structure for table `Exercice`
--

CREATE TABLE `Exercice` (
  `Id` int(11) NOT NULL,
  `IdAct` int(11) NOT NULL,
  `IdInst` int(11) NOT NULL,
  `Notes` varchar(50) NOT NULL,
  `Rythms` varchar(50) NOT NULL,
  `Img` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INT `Exercice`(`Id`,`IdAct`,`IdInst`,`Note`,`Rythms`,`Img`)
(1,1,1,'[-9-7-5-7-5]','[4;4;4;4;1]','Ex01.png']),
(1,1,2,'[-9-7-5-7-5]','[4;4;4;4;1]','Ex01.png']),
(1,1,3,'[-9-7-5-7-5]','[4;4;4;4;1]','Ex01.png']),
(1,1,4,'[-9-7-5-7-5]','[4;4;4;4;1]','Ex01.png']),

(2,1,1,'[-7;-5;-4;-5;-7]','[4;4;4;4;1]','Exo02.png'),
(2,1,2,'[-7;-5;-4;-5;-7]','[4;4;4;4;1]','Exo02.png'),
(2,1,3,'[-7;-5;-4;-5;-7]','[4;4;4;4;1]','Exo02.png'),
(2,1,4,'[-7;-5;-4;-5;-7]','[4;4;4;4;1]','Exo02.png'),

(3,1,1,'[-5;-4;-2;-4;-5]','[4;4;4;4;1]','Exo03.png'),
(3,1,2,'[-5;-4;-2;-4;-5]','[4;4;4;4;1]','Exo03.png'),
(3,1,3,'[-5;-4;-2;-4;-5]','[4;4;4;4;1]','Exo03.png'),
(3,1,4,'[-5;-4;-2;-4;-5]','[4;4;4;4;1]','Exo03.png'),

(4,1,1,'[-4;-2;0;-2;-4]','[4;4;4;4;1]','Exo04.png'),
(4,1,2,'[-4;-2;0;-2;-4]','[4;4;4;4;1]','Exo04.png'),
(4,1,3,'[-4;-2;0;-2;-4]','[4;4;4;4;1]','Exo04.png'),
(4,1,4,'[-4;-2;0;-2;-4]','[4;4;4;4;1]','Exo04.png'),

(5,1,1,'[-2;0;2;0;-2]','[4;4;4;4;1]','Exo05.png'),
(5,1,2,'[-2;0;2;0;-2]','[4;4;4;4;1]','Exo05.png'),
(5,1,3,'[-2;0;2;0;-2]','[4;4;4;4;1]','Exo05.png'),
(5,1,4,'[-2;0;2;0;-2]','[4;4;4;4;1]','Exo05.png'),

(6,1,1,'[0;2;3;2;0]','[4;4;4;4;1]','Exo06.png'),
(6,1,2,'[0;2;3;2;0]','[4;4;4;4;1]','Exo06.png'),
(6,1,3,'[0;2;3;2;0]','[4;4;4;4;1]','Exo06.png'),
(6,1,4,'[0;2;3;2;0]','[4;4;4;4;1]','Exo06.png'),



(7,1,1,'[-2;-7;-2;-5;-2;-4;-2;-9]','[4;4;4;4;4;4;4;4]','Exo07.png'),
(7,1,2,'[-2;-7;-2;-5;-2;-4;-2;-9]','[4;4;4;4;4;4;4;4]','Exo07.png'),
(7,1,3,'[-2;-7;-2;-5;-2;-4;-2;-9]','[4;4;4;4;4;4;4;4]','Exo07.png'),
(7,1,4,'[-2;-7;-2;-5;-2;-4;-2;-9]','[4;4;4;4;4;4;4;4]','Exo07.png'),

(8,1,1,'[0;-4;0;-2;0;-5;0;-7]','[4;4;4;4;4;4;4;4]','Exo08.png'),
(8,1,2,'[0;-4;0;-2;0;-5;0;-7]','[4;4;4;4;4;4;4;4]','Exo08.png'),
(8,1,3,'[0;-4;0;-2;0;-5;0;-7]','[4;4;4;4;4;4;4;4]','Exo08.png'),
(8,1,4,'[0;-4;0;-2;0;-5;0;-7]','[4;4;4;4;4;4;4;4]','Exo08.png'),

(9,1,1,'[2;-4;2;-2;0;-4;0;5]','[4;4;4;4;4;4;4;4]','Exo09.png'),
(9,1,2,'[2;-4;2;-2;0;-4;0;5]','[4;4;4;4;4;4;4;4]','Exo09.png'),
(9,1,3,'[2;-4;2;-2;0;-4;0;5]','[4;4;4;4;4;4;4;4]','Exo09.png'),
(9,1,4,'[2;-4;2;-2;0;-4;0;5]','[4;4;4;4;4;4;4;4]','Exo09.png'),


(10,1,1,'[3;0;3;-2;3;-4;3;2]','[4;4;4;4;4;4;4;4]','Exo10.png'),
(10,1,2,'[3;0;3;-2;3;-4;3;2]','[4;4;4;4;4;4;4;4]','Exo10.png'),
(10,1,3,'[3;0;3;-2;3;-4;3;2]','[4;4;4;4;4;4;4;4]','Exo10.png'),
(10,1,4,'[3;0;3;-2;3;-4;3;2]','[4;4;4;4;4;4;4;4]','Exo10.png'),

(11,1,1,'[-2;-5;-2;2;-2;-7;-4;3]','[4;4;4;4;4;4;4;4]','Exo11.png'),
(11,1,2,'[-2;-5;-2;2;-2;-7;-4;3]','[4;4;4;4;4;4;4;4]','Exo11.png'),
(11,1,3,'[-2;-5;-2;2;-2;-7;-4;3]','[4;4;4;4;4;4;4;4]','Exo11.png'),
(11,1,4,'[-2;-5;-2;2;-2;-7;-4;3]','[4;4;4;4;4;4;4;4]','Exo11.png'),

(12,1,1,'[-9;-7;-5;-4;-5;-7]','[4;8;8;4;4;1]','Exo12.png'),
(12,1,2,'[-9;-7;-5;-4;-5;-7]','[4;8;8;4;4;1]','Exo12.png'),
(12,1,3,'[-9;-7;-5;-4;-5;-7]','[4;8;8;4;4;1]','Exo12.png'),
(12,1,4,'[-9;-7;-5;-4;-5;-7]','[4;8;8;4;4;1]','Exo12.png'),

-- --------------------------------------------------------



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
