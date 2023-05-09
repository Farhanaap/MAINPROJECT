/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - eye_diseases
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`eye_diseases` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `eye_diseases`;

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `b_id` int(11) NOT NULL AUTO_INCREMENT,
  `s_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `date` varchar(30) NOT NULL,
  PRIMARY KEY (`b_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`b_id`,`s_id`,`p_id`,`date`) values 
(1,1,5,'2023-03-20'),
(2,1,5,'2023-03-19'),
(3,1,5,'2023-03-10'),
(4,1,5,'2023-03-29');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `complaint` varchar(100) NOT NULL,
  `date` varchar(30) NOT NULL,
  `reply` varchar(100) NOT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`c_id`,`uid`,`complaint`,`date`,`reply`) values 
(1,5,'not','2023-03-13','ok'),
(2,5,'OKOOO','2023-03-15','pending'),
(3,5,'sdfg','2023-03-15','pending');

/*Table structure for table `doc_shedule` */

DROP TABLE IF EXISTS `doc_shedule`;

CREATE TABLE `doc_shedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `docid` int(11) DEFAULT NULL,
  `day` varchar(100) DEFAULT NULL,
  `ftime` varchar(100) DEFAULT NULL,
  `totime` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `doc_shedule` */

insert  into `doc_shedule`(`id`,`docid`,`day`,`ftime`,`totime`) values 
(1,4,'MONDAY','10:00 AM','12:00 PM'),
(2,6,'SUNDAY','09:00','12:00');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `d_id` int(11) NOT NULL AUTO_INCREMENT,
  `hos_id` int(11) DEFAULT NULL,
  `l_id` int(11) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `lname` varchar(30) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `place` varchar(30) NOT NULL,
  `post` varchar(30) NOT NULL,
  `pin` int(15) NOT NULL,
  `phone` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `qualification` varchar(30) NOT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `doctor` */

insert  into `doctor`(`d_id`,`hos_id`,`l_id`,`fname`,`lname`,`gender`,`place`,`post`,`pin`,`phone`,`email`,`qualification`) values 
(1,3,4,'Dr.','pashupathy','male','chennai','chennai',632598,9852145236,'pashu@gmail.com','MBBS'),
(3,3,6,'Dr.','thrivikraman','male','wayanad','wayanad',632598,8965232014,'thri@gmail.com','MBBS MD');

/*Table structure for table `health_record` */

DROP TABLE IF EXISTS `health_record`;

CREATE TABLE `health_record` (
  `h_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `record` varchar(500) NOT NULL,
  `date` varchar(30) NOT NULL,
  PRIMARY KEY (`h_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `health_record` */

insert  into `health_record`(`h_id`,`p_id`,`d_id`,`record`,`date`) values 
(2,5,4,'20230315_095012.pdf','2023-03-15');

/*Table structure for table `hospital` */

DROP TABLE IF EXISTS `hospital`;

CREATE TABLE `hospital` (
  `hid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `hospital` */

insert  into `hospital`(`hid`,`lid`,`name`,`place`,`post`,`pin`,`phone`,`email`) values 
(1,3,'BMH','kozhikode','kozhikode','673001','9852102365','bmh@gmail.com');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `l_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `type` varchar(30) NOT NULL,
  PRIMARY KEY (`l_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`l_id`,`username`,`password`,`type`) values 
(1,'admin','admin','admin'),
(3,'h','h','hospital'),
(4,'dr','dr','doctor'),
(5,'us','us','user'),
(6,'thri@gmail.com','8263','doctor'),
(7,'bhuuu','Bhu@1234','user');

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `r_id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `dr_id` int(11) NOT NULL,
  `rating` float NOT NULL,
  `date` varchar(30) NOT NULL,
  PRIMARY KEY (`r_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`r_id`,`uid`,`dr_id`,`rating`,`date`) values 
(1,5,6,3.5,'2023-03-15'),
(2,5,4,4.5,'2023-03-15'),
(3,5,6,2,'2023-03-15'),
(4,5,6,1.5,'2023-03-15'),
(5,5,4,3.5,'2023-03-15'),
(6,5,4,5,'2023-03-15'),
(7,5,6,5,'2023-03-15');

/*Table structure for table `upload_image` */

DROP TABLE IF EXISTS `upload_image`;

CREATE TABLE `upload_image` (
  `up_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_id` int(11) NOT NULL,
  `image` text NOT NULL,
  `date` varchar(30) NOT NULL,
  PRIMARY KEY (`up_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `upload_image` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `l_id` int(11) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `lname` varchar(30) NOT NULL,
  `gender` varchar(30) NOT NULL,
  `place` varchar(30) NOT NULL,
  `post` varchar(30) NOT NULL,
  `pin` int(30) NOT NULL,
  `phone` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`uid`,`l_id`,`fname`,`lname`,`gender`,`place`,`post`,`pin`,`phone`,`email`) values 
(1,5,'go','mathy','female','thrichy','thrichy',632589,9856325697,'us@gmail.com'),
(2,7,'Bhuuu','oooo','male','kannur','kannur',632547,9658721305,'mess@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
