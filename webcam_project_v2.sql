-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 22, 2022 at 02:45 PM
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
-- Database: `webcam_project_v2`
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
  `email` varchar(100) NOT NULL,
  `tel` varchar(10) NOT NULL,
  `role` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`, `name`, `surname`, `email`, `tel`, `role`) VALUES
(1, 'admin', '1234', 'AAAAAA', 'BBBBBB', 'AAAA@email.com', '0000000000', 'admin'),
(2, 'manager', '1234', 'manager', 'manager', 'manager@email.com', '0000000000', 'officer'),
(9, 'test1', '1234', 'dasd', 'asd', 'test1@email.com', '0000000000', 'officer'),
(22, 'bill', '1234', 'Bill', 'Cosby', 'bill@email.com', '0000000000', 'officer'),
(23, 'officer', '1234', 'dasd', 'dasd', 'officer@email.com', '0000000001', 'officer');

-- --------------------------------------------------------

--
-- Table structure for table `cases`
--

CREATE TABLE `cases` (
  `id` int(4) NOT NULL,
  `subject` varchar(50) NOT NULL,
  `pet_name` varchar(20) NOT NULL,
  `queue_time` timestamp NULL DEFAULT NULL,
  `regis_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `note` varchar(10000) NOT NULL,
  `camera_id` int(3) DEFAULT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'wait',
  `owner` varchar(101) NOT NULL,
  `username` varchar(20) NOT NULL,
  `doctor` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cases`
--

INSERT INTO `cases` (`id`, `subject`, `pet_name`, `queue_time`, `regis_time`, `note`, `camera_id`, `status`, `owner`, `username`, `doctor`) VALUES
(2, 'No2', 'Joe', '2022-02-09 16:27:00', '2022-02-08 12:24:44', 'dasd', NULL, 'complete', 'dasdtes dasd', 'dasd2', 'Marry Smith'),
(3, 'No3', 'Dill', '2022-02-17 04:56:00', '2022-02-10 04:56:40', '', NULL, 'complete', 'dasdtes dasd', 'dasd2', 'Bob Brown'),
(6, 'No5', 'Non', '2022-02-19 04:18:00', '2022-02-18 04:18:56', 'dsadas', NULL, 'complete', 'dasdtes dasd', 'dasd2', 'Roxie Swanson'),
(7, 'test', 'Test', '2022-02-19 13:20:00', '2022-02-18 13:20:37', 'sdfsdf', NULL, 'complete', 'test_rgis test_rgis', 'test_rgis', 'Ann Richmond');

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `id` int(3) NOT NULL,
  `name` varchar(50) NOT NULL,
  `role` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`id`, `name`, `role`) VALUES
(1, 'Marry Smith', 'veterinary'),
(2, 'Bob Brown', 'veterinary'),
(3, 'Ann Richmond', 'veterinary'),
(4, 'Roxie Swanson', 'veterinary');

-- --------------------------------------------------------

--
-- Table structure for table `news`
--

CREATE TABLE `news` (
  `id` int(4) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `detail` varchar(10000) NOT NULL,
  `img` varchar(200) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `modified_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `type` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `news`
--

INSERT INTO `news` (`id`, `subject`, `detail`, `img`, `create_time`, `modified_time`, `type`) VALUES
(14, 'fsfsffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', '<p>มติคณะรัฐมนตรี อนุมัติงบกลาง 251 ล้านบาท จ้างเหมาพนักงานปฏิบัติงานของกรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช 3,999 อัตรา ในอัตราจ้าง 9,000 บาทต่อเดือน เป็นเวลา 7 เดือน วันที่ 1 ก.พ. 2565 น.ส.ไตรศุลี ไตรสรณกุล รองโฆษกประจำสำนักนายกรัฐมนตรี กล่าวว่า คณะรัฐมนตรี (ครม.) อนุมัติโครงการจ้างเหมาพนักงานปฏิบัติงานของกรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช ประจำปีงบประมาณ 2565 วงเงินงบประมาณ 251.94 ล้านบาท โดยใช้งบประมาณจากงบกลาง รายการเงินสำรองจ่ายเพื่อกรณีฉุกเฉินหรือจำเป็น ประจำปีงบประมาณ 2565 สำหรับจ้างเหมาพนักงานจำนวน 3,999 อัตรา ในอัตราจ้าง 9,000 บาทต่อเดือน ระยะเวลาการจ้าง 7 เดือน ระหว่าง มี.ค.-ก.ย. 2565 เพื่อปฏิบัติงานตามภารกิจสำคัญของกรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช น.ส.ไตรศุลี กล่าวว่า โครงการดังกล่าวเป็นการจ้างงานราษฎรในพื้นที่มาช่วยสนับสนุนการดำเนินงานตามภารกิจของหน่วยงานในพื้นที่ในการอนุรักษ์ คุ้มครอง และฟื้นฟูทรัพยากรป่าไม้และสัตว์ป่า เช่น งานด้านป้องกันรักษาป่า การลาดตระเวนตรวจปราบปรามการลักลอบทำลายทรัพยากรป่าไม้ในอุทยานแห่งชาติ เขตรักษาพันธุ์สัตว์ป่า เขตห้ามล่าสัตว์ป่า งานควบคุมไฟป่าและหมอกควัน งานปราบปรามการค้าสัตว์ป่าและพืชป่าระหว่างประเทศ งานอนุรักษ์ทรัพยากรป่าต้นน้ำ งานสำรวจและวิเคราะห์ข้อมูลป่าไม้ งานบริการท่องเที่ยวเพื่อสร้างรายได้ให้กับประเทศ รวมทั้งเพื่อบรรเทาความเดือดร้อนของพนักงานที่ถูกเลิกจ้างในส่วนที่ถูกปรับลดงบประมาณ เนื่องมาจากการได้รับผลกระทบจากการระบาดของโควิด-19.</p>', '5bded8cc-b6e3-4be3-9849-bb17f276e972.jpg', '2022-02-01 06:21:46', '2022-02-03 17:00:07', 'news'),
(15, 'dad', 'adasdasd', 'a66a20fa-9320-44f7-9701-d68b8880c948.jpeg', '2022-02-01 06:42:45', '2022-02-01 07:37:16', 'article'),
(16, 'dasd', '<p>มติคณะรัฐมนตรี อนุมัติงบกลาง 251 ล้านบาท จ้างเหมาพนักงานปฏิบัติงานของกรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช 3,999 อัตรา ในอัตราจ้าง 9,000 บาทต่อเดือน เป็นเวลา 7 เดือน วันที่ 1 ก.พ. 2565 น.ส.ไตรศุลี ไตรสรณกุล รองโฆษกประจำสำนักนายกรัฐมนตรี กล่าวว่า คณะรัฐมนตรี (ครม.) อนุมัติโครงการจ้างเหมาพนักงานปฏิบัติงานของกรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช ประจำปีงบประมาณ 2565 วงเงินงบประมาณ 251.94 ล้านบาท โดยใช้งบประมาณจากงบกลาง รายการเงินสำรองจ่ายเพื่อกรณีฉุกเฉินหรือจำเป็น ประจำปีงบประมาณ 2565 สำหรับจ้างเหมาพนักงานจำนวน 3,999 อัตรา ในอัตราจ้าง 9,000 บาทต่อเดือน ระยะเวลาการจ้าง 7 เดือน ระหว่าง มี.ค.-ก.ย. 2565 เพื่อปฏิบัติงานตามภารกิจสำคัญของกรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช น.ส.ไตรศุลี กล่าวว่า โครงการดังกล่าวเป็นการจ้างงานราษฎรในพื้นที่มาช่วยสนับสนุนการดำเนินงานตามภารกิจของหน่วยงานในพื้นที่ในการอนุรักษ์ คุ้มครอง และฟื้นฟูทรัพยากรป่าไม้และสัตว์ป่า เช่น งานด้านป้องกันรักษาป่า การลาดตระเวนตรวจปราบปรามการลักลอบทำลายทรัพยากรป่าไม้ในอุทยานแห่งชาติ เขตรักษาพันธุ์สัตว์ป่า เขตห้ามล่าสัตว์ป่า งานควบคุมไฟป่าและหมอกควัน งานปราบปรามการค้าสัตว์ป่าและพืชป่าระหว่างประเทศ งานอนุรักษ์ทรัพยากรป่าต้นน้ำ งานสำรวจและวิเคราะห์ข้อมูลป่าไม้ งานบริการท่องเที่ยวเพื่อสร้างรายได้ให้กับประเทศ รวมทั้งเพื่อบรรเทาความเดือดร้อนของพนักงานที่ถูกเลิกจ้างในส่วนที่ถูกปรับลดงบประมาณ เนื่องมาจากการได้รับผลกระทบจากการระบาดของโควิด-19.\"\"</p>', '2ac6580a-9366-454a-8a6b-c56b6d329bb0.jpg', '2022-02-03 15:38:48', '2022-02-17 14:30:51', 'promotion'),
(17, 'dasd', '', '6285fb7c-3258-493c-b3b0-62301e45715f.jpg', '2022-02-03 15:41:38', '2022-02-03 15:41:38', 'news');

-- --------------------------------------------------------

--
-- Table structure for table `pet`
--

CREATE TABLE `pet` (
  `id` int(4) NOT NULL,
  `pet_name` varchar(20) NOT NULL,
  `pet_age` varchar(5) NOT NULL,
  `pet_type` varchar(10) NOT NULL,
  `owner` varchar(101) NOT NULL,
  `tel` varchar(10) NOT NULL,
  `regis_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `username` varchar(20) NOT NULL,
  `noti2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pet`
--

INSERT INTO `pet` (`id`, `pet_name`, `pet_age`, `pet_type`, `owner`, `tel`, `regis_time`, `username`, `noti2`) VALUES
(3, 'Joe', '1:1', 'cat', 'dasdtes dasd', '0000000000', '2022-02-08 12:24:00', 'dasd2', ''),
(4, 'Dill', '2:3', 'cat', 'dasdtes dasd', '0000000000', '2022-02-10 13:54:59', 'dasd2', ''),
(5, 'dasd', '0:1', 'dsad', 'dasdtes dasd', '0000000000', '2022-02-14 16:10:04', 'dasd2', ''),
(8, 'Non', '2:11', 'cat', 'dasdtes dasd', '0000000000', '2022-02-18 04:00:12', 'dasd2', ''),
(9, 'Test', '1:1', 'cat', 'test_rgis test_rgis', '0000000000', '2022-02-18 13:20:21', 'test_rgis', '');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(4) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `tel` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `name`, `surname`, `email`, `tel`) VALUES
(1, 'dasd2', '1234', 'dasdtes', 'dasd', 'dasd@email.com', '0000000001'),
(3, 'test', '1234', 'Testuser', 'Testuser', 'test@email.com', '0000000000'),
(7, 'aa', 'aaaa', 'Test Posting', 'KJ', 'a@gmail.com', '1234567890'),
(8, 'dd', '1234', 'dasd', 'dasd', 'test1@email.com', '0000000001'),
(10, 'test_rgis', '1234', 'test_rgis', 'test_rgis', 'test1@email.com', '0000000000');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cases`
--
ALTER TABLE `cases`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctor`
--
ALTER TABLE `doctor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pet`
--
ALTER TABLE `pet`
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
  MODIFY `id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `cases`
--
ALTER TABLE `cases`
  MODIFY `id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `doctor`
--
ALTER TABLE `doctor`
  MODIFY `id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `news`
--
ALTER TABLE `news`
  MODIFY `id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `pet`
--
ALTER TABLE `pet`
  MODIFY `id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

DELIMITER $$
--
-- Events
--
CREATE DEFINER=`root`@`localhost` EVENT `statusUpdate_comp` ON SCHEDULE EVERY 1 SECOND STARTS '2022-02-10 11:55:23' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE cases SET `status`='complete',`camera_id`=NULL WHERE `queue_time`<= NOW()$$

CREATE DEFINER=`root`@`localhost` EVENT `statusUpdate_wait` ON SCHEDULE EVERY 1 SECOND STARTS '2022-02-10 11:55:23' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE cases SET `status`='wait' WHERE `queue_time`> NOW()$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
