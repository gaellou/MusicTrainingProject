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
(1,)

-- --------------------------------------------------------



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
