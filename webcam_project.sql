-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 02, 2022 at 02:25 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `webcam_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(3) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`, `name`, `surname`, `role`) VALUES
(1, 'admin', '1234', 'hill', 'hill', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(4) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `queue_time` timestamp NULL DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'Wait',
  `pet_name` varchar(20) NOT NULL,
  `pet_age` varchar(5) NOT NULL,
  `pet_type` varchar(10) NOT NULL,
  `register_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `password` varchar(50) NOT NULL,
  `camera_id` int(3) NOT NULL,
  `note` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `surname`, `queue_time`, `status`, `pet_name`, `pet_age`, `pet_type`, `register_time`, `password`, `camera_id`, `note`) VALUES
(6, 'Hello23', 'dsad', '2021-12-30 17:29:00', 'Completed', 'asd', '2:11', 'dasd', '2021-12-27 08:35:57', 'password', 0, ''),
(7, 'BBBB', 'asd', '2021-12-27 13:09:00', 'Completed', 'asd', '33:0', 'dasd', '2021-12-27 08:40:34', 'password', 0, 'cczxcz'),
(8, 'FFF', 'sadA', '2021-12-27 13:18:00', 'Completed', 'ads', '3:1', 'dasd', '2021-12-27 13:16:55', 'password', 0, 'asdas'),
(9, 'dsda', 'sdasd', '2021-12-29 12:46:00', 'Completed', 'dasd', '3:2', 'sdada', '2021-12-29 08:46:29', 'sada', 1, 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'),
(10, 'hill', 'asd', '2021-12-30 08:30:00', 'Completed', 'dsad', '2:4', 'sad', '2021-12-30 08:29:41', 'dsad', 1, 'ddddd'),
(11, 'dsad', 'asdas', '2021-12-30 08:36:00', 'Completed', 'das', '2:4', 'dasd', '2021-12-30 08:36:01', 'sadad', 1, 'dasdasd'),
(12, 'sad', 'fsdf', '2021-12-30 10:16:00', 'Completed', 'asd', '2:2', 'dasd', '2021-12-30 10:15:01', 'sadad', 0, ''),
(14, 'dasd', 'adsad', '2021-12-30 13:27:00', 'Completed', 'dasd', '2:2', 'dasd', '2021-12-30 13:26:38', 'sadasdad', 0, 'dasd'),
(16, 'sa', 'assa', '2021-12-30 13:33:00', 'Completed', 'as', '1:1', 'as', '2021-12-30 13:32:48', 'dsad', 0, 'sa'),
(19, 'das', 'dsad', '2021-12-31 08:01:00', 'Completed', 'dasd', '1:1', 'dasd', '2021-12-31 08:00:43', 'adsd', 1, 'dasd'),
(20, 'asd', 'sadA', '2021-12-31 08:13:00', 'Completed', 'sad', '2:2', 'dasd', '2021-12-31 08:12:43', 'dsad', 1, 'sadasd'),
(21, 'jill', 'sadA', '2021-12-31 08:15:00', 'Completed', 'dasd', '3:2', 'asd', '2021-12-31 08:13:46', 'sdad', 1, 'dsadasd'),
(22, 'dsad', 'ads', '2021-12-31 09:14:00', 'Completed', 'dasd', '1:1', 'asd', '2021-12-31 09:12:49', 'dsa', 1, 'dasd'),
(26, 'dsa', 'asd', '2021-12-31 16:09:00', 'Completed', 'dda', '1:1', 'asd', '2021-12-31 16:08:46', 'dasd', 1, 'dasd'),
(29, 'fds', 'asd', '2021-12-31 16:16:00', 'Completed', 'dda', '3:2', 'dad', '2021-12-31 16:14:54', 'dsad', 0, 'dasd'),
(30, 'das', 'asd', '2021-12-31 16:18:00', 'Completed', 'dda', '1:0', 'dad', '2021-12-31 16:15:12', 'dsad', 1, 'dasd'),
(32, 'das', 'asd', '2021-12-31 16:18:00', 'Completed', 'dda', '1:0', 'dad', '2021-12-31 16:15:12', 'dsad', 1, 'dasd'),
(38, 'dasd', 'sads', '2022-01-01 10:13:00', 'Completed', 'dasd', '1:1', 'adasd', '2022-01-01 08:04:28', 'sada', 10, 'dasdad'),
(39, 'dsad', 'dasd', '2022-01-01 09:04:00', 'Completed', 'dasd', '1:1', 'dasd', '2022-01-01 09:01:57', 'dasd', 9, 'dasd'),
(43, 'hill', 'sup', '2022-01-02 09:14:00', 'Completed', 'kj', '0:1', 'dasd', '2022-01-02 07:14:06', '1234', 1, 'dsadasdasdasdasd'),
(44, 'Bill', 'joe', '2022-01-02 10:25:00', 'Completed', 'asd', '1:1', 'dasd', '2022-01-02 07:25:55', '1234', 0, 'dasdadsdad'),
(45, 'dasd', 'dasd', '2022-01-03 08:50:00', 'Wait', 'dasd', '2:2', 'dasd', '2022-01-02 08:50:55', 'asdasd', 2, 'dasdasdsad'),
(46, 'hill1', 'dasdas', '2022-01-02 13:23:00', 'Completed', 'dasd', '2:2', 'dasd', '2022-01-02 11:23:58', '1234', 0, 'dasdasd'),
(47, 'hill2', 'dasdsa', '2022-01-02 15:24:00', 'Wait', 'dasd', '3:2', 'dasd', '2022-01-02 11:24:19', '1234', 1, 'dsad');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

DELIMITER $$
--
-- Events
--
CREATE DEFINER=`root`@`localhost` EVENT `check_queue_time` ON SCHEDULE EVERY 1 SECOND STARTS '2021-12-27 15:34:40' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE `user` SET status= 'Completed' WHERE queue_time <= NOW()$$

CREATE DEFINER=`root`@`localhost` EVENT `check_queue_time2` ON SCHEDULE EVERY 1 SECOND STARTS '2021-12-30 00:17:15' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE `user` SET status= 'Wait' WHERE queue_time > NOW()$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
