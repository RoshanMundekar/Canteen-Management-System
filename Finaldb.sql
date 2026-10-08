/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - canteendb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`canteendb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `canteendb`;

/*Table structure for table `invoicetbl` */

DROP TABLE IF EXISTS `invoicetbl`;

CREATE TABLE `invoicetbl` (
  `invoiceId` int(255) NOT NULL auto_increment,
  `Uname` varchar(255) default NULL,
  `invoicename` longtext,
  `invoiceDate` varchar(255) default NULL,
  PRIMARY KEY  (`invoiceId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `invoicetbl` */

insert  into `invoicetbl`(`invoiceId`,`Uname`,`invoicename`,`invoiceDate`) values (1,NULL,NULL,NULL),(2,'pari','media/Invoices/pari_34167887_invoice_.pdf','2023-05-31'),(3,'pranita','media/Invoices/pranita_61162146_invoice_.pdf','2023-06-02');

/*Table structure for table `menutbl` */

DROP TABLE IF EXISTS `menutbl`;

CREATE TABLE `menutbl` (
  `Mid` int(255) NOT NULL auto_increment,
  `dishName` varchar(255) default NULL,
  `dishPrice` varchar(255) default NULL,
  `dishAbout` varchar(255) default NULL,
  `dishImg` varchar(255) default NULL,
  `dishCategory` varchar(255) default NULL,
  PRIMARY KEY  (`Mid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `menutbl` */

insert  into `menutbl`(`Mid`,`dishName`,`dishPrice`,`dishAbout`,`dishImg`,`dishCategory`) values (1,'chicken tikka','450','abc','download_JYHXknI.jpg','NON-VEG'),(2,'vada pav','50','ahjca','dish-1.jpg','VEG'),(3,'juice','10','ac','vegan-chocolate-milkshake-recipe.jpg','BEVERAGES'),(4,'vada pav+juice','100','both dishes we will add in meal','../../../media/comboofer.jpg','comboffer');

/*Table structure for table `orderfoodtbl` */

DROP TABLE IF EXISTS `orderfoodtbl`;

CREATE TABLE `orderfoodtbl` (
  `Oid` int(255) NOT NULL auto_increment,
  `Uname` varchar(255) NOT NULL,
  `dishName` varchar(255) NOT NULL,
  `dishPrice` varchar(255) NOT NULL,
  `dishinfo` longtext NOT NULL,
  `dishimgs` varchar(255) NOT NULL,
  `dishQuantity` varchar(255) NOT NULL,
  `Statuss` varchar(255) default NULL,
  PRIMARY KEY  (`Oid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `orderfoodtbl` */

insert  into `orderfoodtbl`(`Oid`,`Uname`,`dishName`,`dishPrice`,`dishinfo`,`dishimgs`,`dishQuantity`,`Statuss`) values (1,'pranita','chicken tikka','450','abc','download_JYHXknI.jpg','2','ordered'),(2,'abc','vada pav','50','ahjca','dish-1.jpg','1','ordering');

/*Table structure for table `stafftbl` */

DROP TABLE IF EXISTS `stafftbl`;

CREATE TABLE `stafftbl` (
  `sId` int(255) NOT NULL auto_increment,
  `Sfname` varchar(255) default NULL,
  `Slname` varchar(255) default NULL,
  `Smail` varchar(255) default NULL,
  `Spass` varchar(255) default NULL,
  `Smobile` varchar(255) default NULL,
  `Saddress` longtext,
  `staffcat` varchar(255) default NULL,
  PRIMARY KEY  (`sId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `stafftbl` */

insert  into `stafftbl`(`sId`,`Sfname`,`Slname`,`Smail`,`Spass`,`Smobile`,`Saddress`,`staffcat`) values (1,'abc','xyz','a@gmail.co','a','9876543210','ajhbcjabcja','Chef');

/*Table structure for table `studentachertbl` */

DROP TABLE IF EXISTS `studentachertbl`;

CREATE TABLE `studentachertbl` (
  `Erid` int(255) NOT NULL auto_increment,
  `Uname` varchar(255) default NULL,
  `umail` varchar(255) default NULL,
  `mobileno` varchar(255) default NULL,
  `upass` varchar(255) default NULL,
  `employeerollno` varchar(255) default NULL,
  `role` varchar(255) default NULL,
  `otpval` varchar(255) default NULL,
  PRIMARY KEY  (`Erid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `studentachertbl` */

insert  into `studentachertbl`(`Erid`,`Uname`,`umail`,`mobileno`,`upass`,`employeerollno`,`role`,`otpval`) values (1,'sayali ','sayu@gmail.com','9011355283','s','85874','teacher',NULL),(2,'pari','pari@gmail.com','8856471230','p','2429','student',NULL),(3,'pranita','p@gmakaj','8468365398','p','937498','student',NULL),(4,'abc','asd@gmail.com','3845937523','asd','xyz847','teacher',NULL),(5,'aakash','a@gmail.co','3459837587','a','169','visitor',NULL);

/*Table structure for table `user_register` */

DROP TABLE IF EXISTS `user_register`;

CREATE TABLE `user_register` (
  `uint` int(255) NOT NULL auto_increment,
  `Uname` varchar(255) NOT NULL default '',
  `umail` varchar(255) NOT NULL default '',
  `mobileno` varchar(255) NOT NULL default '',
  `upass` varchar(255) NOT NULL default '',
  `uaddress` longtext NOT NULL,
  `role` varchar(255) default '',
  PRIMARY KEY  (`uint`),
  UNIQUE KEY `uint` (`uint`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user_register` */

insert  into `user_register`(`uint`,`Uname`,`umail`,`mobileno`,`upass`,`uaddress`,`role`) values (1,'pranita','p@globex.com','2876876538','p','kajbkabkjab akbakbv',''),(2,'sayali ','s@globex.com','2645865867','sayu','abc road, xyz city','');

/*Table structure for table `userfeedback` */

DROP TABLE IF EXISTS `userfeedback`;

CREATE TABLE `userfeedback` (
  `Fid` int(255) NOT NULL auto_increment,
  `Uname` varchar(255) default NULL,
  `feedbacks` longtext,
  PRIMARY KEY  (`Fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `userfeedback` */

insert  into `userfeedback`(`Fid`,`Uname`,`feedbacks`) values (1,'sayali ','Feedback From Teacher');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
