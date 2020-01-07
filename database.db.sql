BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `patient` (
	`pat_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`pat_first_name`	TEXT NOT NULL,
	`pat_last_name`	TEXT NOT NULL,
	`pat_insurance_no`	TEXT NOT NULL,
	`pat_ph_no`	TEXT NOT NULL,
	`pat_date`	DATE DEFAULT (datetime('now','localtime')),
	`pat_address`	TEXT NOT NULL
);
INSERT INTO `patient` (pat_id,pat_first_name,pat_last_name,pat_insurance_no,pat_ph_no,pat_date,pat_address) VALUES (5,'Jammy','Richard','IC-21067','25575544572','2016-07-26 11:09:38','3 wood mod 7'),
 (7,'Clinton','Barton','IC-201302','2558013280','2016-07-27 12:24:13','3 candle tree'),
 (12,'Wakanda','Forever','IN-3123','2558013290','2016-07-27 15:39:47','wakanda'),
 (14,'harry','den','TZ-2222','2552222222','2018-08-28 20:42:55','demo'),
 (15,'Logan','Paul','UD-1353','7850001252','2019-05-01 20:24:04','Blecker Street'),
 (17,'Sample','Name','-','2557845562','2019-12-23 11:29:38','2323, Morogoro'),
 (18,'Minerva','Mohamed','UD-2564644','+25574353637637','2019-12-23 12:16:29','Kwa Msagasumu, Dodoma');
CREATE TABLE IF NOT EXISTS `doctor` (
	`doc_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`doc_first_name`	TEXT NOT NULL,
	`doc_last_name`	TEXT NOT NULL,
	`doc_ph_no`	TEXT NOT NULL,
	`doc_date`	DATE DEFAULT (datetime('now','localtime')),
	`doc_address`	TEXT NOT NULL
);
INSERT INTO `doctor` (doc_id,doc_first_name,doc_last_name,doc_ph_no,doc_date,doc_address) VALUES (1,'Tony','Wood','9967544572','2016-07-25 19:03:25','2 candlewood tree'),
 (2,'Manson','Jonson','9967544572','2016-07-25 19:03:32','2 candlewood tree'),
 (6,'Mny','Nanson','217804567','2016-07-27 13:04:57','Westbrook apt'),
 (10,'John','Smith','7845552220','2019-05-01 20:25:03','demo address');
CREATE TABLE IF NOT EXISTS `appointment` (
	`app_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`pat_id`	INTEGER NOT NULL,
	`doc_id`	INTEGER NOT NULL,
	`appointment_date`	DATE NOT NULL,
	FOREIGN KEY(`doc_id`) REFERENCES `doctor`(`doc_id`),
	FOREIGN KEY(`pat_id`) REFERENCES `patient`(`pat_id`)
);
INSERT INTO `appointment` (app_id,pat_id,doc_id,appointment_date) VALUES (4,7,1,'2016-08-18 14:30:14'),
 (6,12,6,'2016-09-15 18:55:16'),
 (7,5,1,'2016-09-17 11:35:16'),
 (8,15,10,'2019-05-08 07:50:31'),
 (9,17,10,'2019-12-27 11:30:08'),
 (10,15,10,'2019-12-27 11:30:08'),
 (11,18,10,'2019-12-25 13:10:43'),
 (12,18,10,'2019-12-23 13:25:19');
CREATE TABLE IF NOT EXISTS `admin` (
	`ad_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`ad_first_name`	TEXT NOT NULL,
	`ad_last_name`	TEXT NOT NULL,
	`ad_email`	TEXT NOT NULL,
	`ad_password`	TEXT NOT NULL,
	`ad_gender`	INTEGER NOT NULL
);
COMMIT;
