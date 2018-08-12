-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: greatschools1
-- ------------------------------------------------------
-- Server version	5.7.18-0ubuntu0.16.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `city`
--
CREATE DATABASE greatschools;
USE greatschools;

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `state` varchar(200) DEFAULT NULL,
  `state_abbr` varchar(10) DEFAULT NULL,
  `state_url` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `city_url` varchar(200) DEFAULT NULL,
  `list_school` tinyint(1) DEFAULT '0',
  `school_count` int(20) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `unique_index` (`state`,`city`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school`
--

DROP TABLE IF EXISTS `school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `school_url` varchar(200) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `schooltype` varchar(100) DEFAULT NULL,
  `grades` varchar(50) DEFAULT NULL,
  `review_stars` varchar(10) DEFAULT NULL,
  `reviews_count` varchar(50) DEFAULT NULL,
  `enrollment` varchar(100) DEFAULT NULL,
  `students_per_teacher` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `test_scores` varchar(100) DEFAULT NULL,
  `academic_progress` varchar(100) DEFAULT NULL,
  `equity_overview` varchar(100) DEFAULT NULL,
  `student_low_income` varchar(100) DEFAULT NULL,
  `students_gender_male` varchar(100) DEFAULT NULL,
  `student_ethnicities_asian` varchar(100) DEFAULT NULL,
  `student_ethnicities_filipino` varchar(100) DEFAULT NULL,
  `student_ethnicities_hispanic` varchar(100) DEFAULT NULL,
  `student_ethnicities_two_or_more_races` varchar(100) DEFAULT NULL,
  `student_ethnicities_white` varchar(100) DEFAULT NULL,
  `student_ethnicities_black` varchar(100) DEFAULT NULL,
  `student_ethnicities_pacific_Islander` varchar(100) DEFAULT NULL,
  `student_ethnicities_american_indian_alaska_native` varchar(100) DEFAULT NULL,
  `student_ethnicities_hawaiian_native_pacific_islander` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `unique_index` (`name`,`school_url`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school`
--

LOCK TABLES `school` WRITE;
/*!40000 ALTER TABLE `school` DISABLE KEYS */;
/*!40000 ALTER TABLE `school` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-12 12:04:28

