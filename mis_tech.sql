-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mis_tech
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS auth_group;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES auth_group WRITE;
/*!40000 ALTER TABLE auth_group DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS auth_group_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  group_id int NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id,permission_id),
  KEY auth_group_permissio_permission_id_84c5c92e_fk_auth_perm (permission_id),
  CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES auth_group_permissions WRITE;
/*!40000 ALTER TABLE auth_group_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS auth_permission;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_permission (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  content_type_id int NOT NULL,
  codename varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_permission_content_type_id_codename_01ab375a_uniq (content_type_id,codename),
  CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES auth_permission WRITE;
/*!40000 ALTER TABLE auth_permission DISABLE KEYS */;
INSERT INTO auth_permission VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_customuser'),(22,'Can change user',6,'change_customuser'),(23,'Can delete user',6,'delete_customuser'),(24,'Can view user',6,'view_customuser'),(25,'Can add batch',7,'add_batch'),(26,'Can change batch',7,'change_batch'),(27,'Can delete batch',7,'delete_batch'),(28,'Can view batch',7,'view_batch'),(29,'Can add course',8,'add_course'),(30,'Can change course',8,'change_course'),(31,'Can delete course',8,'delete_course'),(32,'Can view course',8,'view_course'),(33,'Can add module',9,'add_module'),(34,'Can change module',9,'change_module'),(35,'Can delete module',9,'delete_module'),(36,'Can view module',9,'view_module'),(37,'Can add session yr',10,'add_sessionyr'),(38,'Can change session yr',10,'change_sessionyr'),(39,'Can delete session yr',10,'delete_sessionyr'),(40,'Can view session yr',10,'view_sessionyr'),(41,'Can add trade',11,'add_trade'),(42,'Can change trade',11,'change_trade'),(43,'Can delete trade',11,'delete_trade'),(44,'Can view trade',11,'view_trade'),(45,'Can add subject',12,'add_subject'),(46,'Can change subject',12,'change_subject'),(47,'Can delete subject',12,'delete_subject'),(48,'Can view subject',12,'view_subject'),(49,'Can add student',13,'add_student'),(50,'Can change student',13,'change_student'),(51,'Can delete student',13,'delete_student'),(52,'Can view student',13,'view_student'),(53,'Can add staff',14,'add_staff'),(54,'Can change staff',14,'change_staff'),(55,'Can delete staff',14,'delete_staff'),(56,'Can view staff',14,'view_staff'),(57,'Can add plan',15,'add_plan'),(58,'Can change plan',15,'change_plan'),(59,'Can delete plan',15,'delete_plan'),(60,'Can view plan',15,'view_plan'),(61,'Can add payment',16,'add_payment'),(62,'Can change payment',16,'change_payment'),(63,'Can delete payment',16,'delete_payment'),(64,'Can view payment',16,'view_payment'),(65,'Can add notification sf',17,'add_notificationsf'),(66,'Can change notification sf',17,'change_notificationsf'),(67,'Can delete notification sf',17,'delete_notificationsf'),(68,'Can view notification sf',17,'view_notificationsf'),(69,'Can add notification s',18,'add_notifications'),(70,'Can change notification s',18,'change_notifications'),(71,'Can delete notification s',18,'delete_notifications'),(72,'Can view notification s',18,'view_notifications'),(73,'Can add leave report sf',19,'add_leavereportsf'),(74,'Can change leave report sf',19,'change_leavereportsf'),(75,'Can delete leave report sf',19,'delete_leavereportsf'),(76,'Can view leave report sf',19,'view_leavereportsf'),(77,'Can add leave report s',20,'add_leavereports'),(78,'Can change leave report s',20,'change_leavereports'),(79,'Can delete leave report s',20,'delete_leavereports'),(80,'Can view leave report s',20,'view_leavereports'),(81,'Can add feedback sf',21,'add_feedbacksf'),(82,'Can change feedback sf',21,'change_feedbacksf'),(83,'Can delete feedback sf',21,'delete_feedbacksf'),(84,'Can view feedback sf',21,'view_feedbacksf'),(85,'Can add feed back s',22,'add_feedbacks'),(86,'Can change feed back s',22,'change_feedbacks'),(87,'Can delete feed back s',22,'delete_feedbacks'),(88,'Can view feed back s',22,'view_feedbacks'),(89,'Can add attendance',23,'add_attendance'),(90,'Can change attendance',23,'change_attendance'),(91,'Can delete attendance',23,'delete_attendance'),(92,'Can view attendance',23,'view_attendance'),(93,'Can add admin',24,'add_admin'),(94,'Can change admin',24,'change_admin'),(95,'Can delete admin',24,'delete_admin'),(96,'Can view admin',24,'view_admin'),(97,'Can add attendance e',25,'add_attendancee'),(98,'Can change attendance e',25,'change_attendancee'),(99,'Can delete attendance e',25,'delete_attendancee'),(100,'Can view attendance e',25,'view_attendancee'),(101,'Can add lplan',26,'add_lplan'),(102,'Can change lplan',26,'change_lplan'),(103,'Can delete lplan',26,'delete_lplan'),(104,'Can view lplan',26,'view_lplan'),(105,'Can add task',27,'add_task'),(106,'Can change task',27,'change_task'),(107,'Can delete task',27,'delete_task'),(108,'Can view task',27,'view_task'),(109,'Can add student result',28,'add_studentresult'),(110,'Can change student result',28,'change_studentresult'),(111,'Can delete student result',28,'delete_studentresult'),(112,'Can view student result',28,'view_studentresult');
/*!40000 ALTER TABLE auth_permission ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS django_admin_log;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_admin_log (
  id int NOT NULL AUTO_INCREMENT,
  action_time datetime(6) NOT NULL,
  object_id longtext,
  object_repr varchar(200) NOT NULL,
  action_flag smallint unsigned NOT NULL,
  change_message longtext NOT NULL,
  content_type_id int DEFAULT NULL,
  user_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY django_admin_log_content_type_id_c4bce8eb_fk_django_co (content_type_id),
  KEY django_admin_log_user_id_c564eba6_fk_mistech_customuser_id (user_id),
  CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
  CONSTRAINT django_admin_log_user_id_c564eba6_fk_mistech_customuser_id FOREIGN KEY (user_id) REFERENCES mistech_customuser (id),
  CONSTRAINT django_admin_log_chk_1 CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES django_admin_log WRITE;
/*!40000 ALTER TABLE django_admin_log DISABLE KEYS */;
/*!40000 ALTER TABLE django_admin_log ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS django_content_type;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_content_type (
  id int NOT NULL AUTO_INCREMENT,
  app_label varchar(100) NOT NULL,
  model varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY django_content_type_app_label_model_76bd3d3b_uniq (app_label,model)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES django_content_type WRITE;
/*!40000 ALTER TABLE django_content_type DISABLE KEYS */;
INSERT INTO django_content_type VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(24,'mistech','admin'),(23,'mistech','attendance'),(25,'mistech','attendancee'),(7,'mistech','batch'),(8,'mistech','course'),(6,'mistech','customuser'),(22,'mistech','feedbacks'),(21,'mistech','feedbacksf'),(20,'mistech','leavereports'),(19,'mistech','leavereportsf'),(26,'mistech','lplan'),(9,'mistech','module'),(18,'mistech','notifications'),(17,'mistech','notificationsf'),(16,'mistech','payment'),(15,'mistech','plan'),(10,'mistech','sessionyr'),(14,'mistech','staff'),(13,'mistech','student'),(28,'mistech','studentresult'),(12,'mistech','subject'),(27,'mistech','task'),(11,'mistech','trade'),(5,'sessions','session');
/*!40000 ALTER TABLE django_content_type ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS django_migrations;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_migrations (
  id bigint NOT NULL AUTO_INCREMENT,
  app varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  applied datetime(6) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES django_migrations WRITE;
/*!40000 ALTER TABLE django_migrations DISABLE KEYS */;
INSERT INTO django_migrations VALUES (1,'contenttypes','0001_initial','2024-02-18 15:49:49.397257'),(2,'contenttypes','0002_remove_content_type_name','2024-02-18 15:49:49.445978'),(3,'auth','0001_initial','2024-02-18 15:49:49.618310'),(4,'auth','0002_alter_permission_name_max_length','2024-02-18 15:49:49.665288'),(5,'auth','0003_alter_user_email_max_length','2024-02-18 15:49:49.680814'),(6,'auth','0004_alter_user_username_opts','2024-02-18 15:49:49.680814'),(7,'auth','0005_alter_user_last_login_null','2024-02-18 15:49:49.680814'),(8,'auth','0006_require_contenttypes_0002','2024-02-18 15:49:49.696449'),(9,'auth','0007_alter_validators_add_error_messages','2024-02-18 15:49:49.697188'),(10,'auth','0008_alter_user_username_max_length','2024-02-18 15:49:49.697188'),(11,'auth','0009_alter_user_last_name_max_length','2024-02-18 15:49:49.712268'),(12,'auth','0010_alter_group_name_max_length','2024-02-18 15:49:49.718458'),(13,'auth','0011_update_proxy_permissions','2024-02-18 15:49:49.727966'),(14,'auth','0012_alter_user_first_name_max_length','2024-02-18 15:49:49.727966'),(15,'mistech','0001_initial','2024-02-18 15:49:52.300276'),(16,'admin','0001_initial','2024-02-18 15:49:52.442980'),(17,'admin','0002_logentry_remove_auto_add','2024-02-18 15:49:52.458604'),(18,'admin','0003_logentry_add_action_flag_choices','2024-02-18 15:49:52.458604'),(19,'sessions','0001_initial','2024-02-18 15:49:52.490407'),(20,'mistech','0002_remove_subject_sf_id_subject_sf_id','2024-02-19 00:54:24.967926'),(21,'mistech','0003_attendancee','2024-02-23 08:08:07.320787'),(22,'mistech','0004_module_c_id','2024-03-05 08:35:27.317041'),(23,'mistech','0005_rename_mode_name_module_mod_name','2024-03-05 08:49:58.425749'),(24,'mistech','0006_lplan_task_delete_plan_lplan_tk_id','2024-03-18 21:08:11.819521'),(25,'mistech','0007_remove_lplan_time_lplan_lp_time_task_tk_wk_and_more','2024-03-19 07:31:04.278197'),(26,'mistech','0008_alter_task_status','2024-03-21 09:47:02.145462'),(27,'mistech','0009_studentresult','2024-03-23 12:12:31.920906'),(28,'mistech','0010_alter_staff_mobileno','2024-03-29 08:32:43.487059'),(29,'mistech','0011_alter_student_mobileno','2024-03-29 08:36:13.766201'),(30,'mistech','0012_staff_fcm_token_student_fcm_token','2024-03-29 22:37:11.897377'),(31,'mistech','0013_leavereportsf_medical_img','2024-03-30 04:52:43.178601'),(32,'mistech','0014_notificationsf_is_read_and_more','2024-05-18 10:22:19.123603'),(33,'mistech','0015_leavereportsf_reason_lv','2024-05-19 08:36:00.925854'),(34,'mistech','0016_alter_leavereportsf_reason_lv','2024-05-19 08:38:19.734106');
/*!40000 ALTER TABLE django_migrations ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS django_session;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_session (
  session_key varchar(40) NOT NULL,
  session_data longtext NOT NULL,
  expire_date datetime(6) NOT NULL,
  PRIMARY KEY (session_key),
  KEY django_session_expire_date_a5c62663 (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES django_session WRITE;
/*!40000 ALTER TABLE django_session DISABLE KEYS */;
INSERT INTO django_session VALUES ('0esnteepdw7p0yts7q2v471qezjeuxzs','.eJxVjs0KwjAQhN8lZxFNtvnxKPQ5yu52lwTbIqY9Fd_diBd7nG_4htnNgNuah63KayijuRlrTv-MkB-yfIu51FU4n_sZy3RvuF_GQziKGWtulsZOAztKCJHZk1PLnZUrhyjBM9kEimJbpaQO-IIBWRyQJvIRoI1Oz9-zaN4fjRE45Q:1rqQFZ:4obUQ8_aJND0ZL5Sa5TAQVczvhNATqvl7jwTIAcONwM','2024-04-13 04:23:25.951450'),('0m7tv02auwhq7i2qughl9di3hvd0yb40','.eJxVi0EOwiAQAP_C2RgWWAoeTfoOsrBLINoepD0Z_2692ePMZN4q0b61tA95pc7qpkBd_l2m8pD1F5Y-NintOi_Un_dDzyuf4Dw2Gu24LBZBFvAmotXeI0zGVWfZamIqwBgg6uKzsM4GEWMNFExlHzKYyanPF6qcM8U:1s8cap:z53KJvxdzF2PQPt9eGxZtxWJ7mlan_ECPO-2JLMYj0g','2024-06-02 09:12:35.377413'),('45dp3zymcjhp69isy04y5kahdec2rkjg','.eJxVi7sOwjAMAP8lM0IlcfNgROp3RLZrKxG0A2knxL8Ttna8O93HZNy3kvcm71xnczfWXI6OkJ-y_sNS2yZcrtOC9fXoelrnE5zHgq30S-OogR0lhMjsyanl0cqNQ5TgmWwCRbE9KakDHjAgiwPSRD4CmO8P9Jc1tw:1rqg69:GuGwZISppWJ3X7Z2HGftQnF38GuxFbs94y_G0UxY4C8','2024-04-13 21:18:45.775453'),('6arzwofk0j36ws2ysregp6mw7xkp1aw6','.eJxVi00OwiAUBu_C2hj-KS5Neg7y8XgEou1C2pXx7tadXc5M5i0S9q2lffAr9SJuworLv8ugB6-_sPSxMbXrvKA_74ee13KC89gw2nFBwQRrjXaViIOS0WIyORYfM4okW3QwiJqyJ5d1paoAzWDJ3k1Oi88X0Y81BQ:1ri8FA:3XgKALTzg8ysn1nwuyB9EyiYVuuiA8mTBqpnSpApI9U','2024-03-21 07:32:44.393244'),('6oasg92csenn8g1zfyxalks7awm0f147','.eJxVi8EOwiAQBf-FszHAmkI8mvQ7yGN3CUTbg7Snxn8Xb_Y4M5nDJOxbTXvXd2pi7mYyl3-XwU9df2FpfVOu13lBez2Gnlc5wXms6HVcTMSFJRdmYZLicnDeKWxW8bZMoyhBKVD0AmJrrSjE3YCoCNF8vibFNp8:1ri6Dz:RaI1zJb2_ieB4I0abK6l7BfZIRp6cJATle0-vIZI8G0','2024-03-21 05:23:23.639475'),('7ubh8cjyvrjgyls58t5ar3thh0umq502','.eJxVi7sOwjAMAP8lM0IlcfNgROp3RLZrKxG0A2knxL8Ttna8O93HZNy3kvcm71xnczfWXI6OkJ-y_sNS2yZcrtOC9fXoelrnE5zHgq30S-OogR0lhMjsyanl0cqNQ5TgmWwCRbE9KakDHjAgiwPSRD4CmO8P9Jc1tw:1s8Wbu:gxlWbJ6SV0svqycpYyYXXGfFtJPvqvDuXl-dEdAEOHs','2024-06-02 02:49:18.795522'),('fd0v2gfyfpqff9my5x2d4lx064sr780r','.eJxVizEOwyAMAP_iuaqCgQQ6Vso7kLGNQG0ylGSq-vemWzPene4Nifatpr3rKzWBGxgHl3-ZiR-6_srS-qZcr_NC7Xk_9LzKCc5jpV6Py1uaxAY2o1B0pWRCjgaVBzE-cCEkNkqeJWdyODLihMEOIUtURA-fLw8SNWE:1rqOl9:hUG_aWhX0WYivWYfK_lEk_YRZAm-Eg7Y78h2T9R9A-U','2024-04-13 02:47:55.826817'),('k9rq792us6kb0sfq93eigy0axprcckrn','.eJxVi0EOwiAQAP_C2RgWWAoeTfoOsrBLINoepD0Z_2692ePMZN4q0b61tA95pc7qpkBd_l2m8pD1F5Y-NintOi_Un_dDzyuf4Dw2Gu24LBZBFvAmotXeI0zGVWfZamIqwBgg6uKzsM4GEWMNFExlHzKYyanPF6qcM8U:1s0WoA:TS1KnelxT9wq1r7nyipXmnHsVK2pztYvdOBQJbt_dEI','2024-05-11 01:24:54.436216'),('klsz10wh5mjg90k9a4v8ghxh3xvtkm1z','.eJxVizEOwyAMAP_CXFUYQwwdK-UdyNhEoDYZmmSq-vemWzPene5tMu9by_taX7mruRkH5vIvC8ujLr8y93Wr0q7jzP15P_S46AnOY-O1HZetISnFOIUBphSGQGrBIRAGLGItSFLPGAvZCGjJF4yiEgmdB1Y1ny-0UjNo:1svBqP:5I1nzA25ZkOBLFiOTKh97NvBHHdT_29jP5x9dXAKtDE','2024-10-14 08:33:25.898950'),('mwik2yi0fnugnx95w5cdhr3q95hs5in9','.eJxVizEOwyAMAP_iuapqCCZ0rJR3IIONQG0ylGSK-vemWzPenW6HyNta49b1HZvAHRDh8i8T56cuvzK3vmqu12nm9nocelrkBOexcq_HVbCQTxYpqfM5k8NkmSWTtTfUMg4yiBBxEG8UjaArVjCIM8FzoRE-X_ssNO4:1rppy9:ZIQDOngyL7pcRbo7KS5X6bTFc2Uuc5rLt7KFyblCGsM','2024-04-11 13:39:01.400835'),('nyj6rvjasgr2kw4tl96i36nw301d1c4j','.eJxVi0sOwjAMBe-SNUKy3U_CEqnniJzYViJoF6RdIe5O2NHV05vRvF3kYy_xaPqKVdzNobv8s8T5odtPrLXtmst1Wbk-7x0vm5zOOSzcSq8Ci0-zsQfzYcw4B0AUFJuIiQzVYAAkSmiEWQMOmPuAVx4nAXSfL8kBNFg:1suwhm:6MOKsiulOR6Xa0HaHvKkJqaCu9SOSKMbnFEp1HTZH0M','2024-10-13 16:23:30.612789'),('py1mxai1fzx6x7fizamksbh3utyy81cz','.eJxVizEOwyAMAP_iuaqCgQQ6Vso7kLGNQG0ylGSq-vemWzPene4Nifatpr3rKzWBGxgHl3-ZiR-6_srS-qZcr_NC7Xk_9LzKCc5jpV6Py1uaxAY2o1B0pWRCjgaVBzE-cCEkNkqeJWdyODLihMEOIUtURA-fLw8SNWE:1svBfX:Ed5tbJI0HtZe4zLSct9OzUNPEkhSWucNwe4gZfF4D7s','2024-10-14 08:22:11.247328'),('so9784cvlgjr5ekid273t9nyxayxafbg','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjNzlvOXktM2M5ZmU5NWI5NjMwNTljMjU2YTFkNTc3OTg2MWNmNWQifQ:1s8XSd:uBMZatteNxtc70IER3C50jJMohG9LsrnZ1ntZTry6zU','2024-06-02 03:43:47.399442'),('soxdwd9uueyrmvxl7d44mw1mxl26cyc5','.eJxVizEOwyAMAP_iuaqCgQQ6Vso7kLGNQG0ylGSq-vemWzPene4Nifatpr3rKzWBGxgHl3-ZiR-6_srS-qZcr_NC7Xk_9LzKCc5jpV6Py1uaxAY2o1B0pWRCjgaVBzE-cCEkNkqeJWdyODLihMEOIUtURA-fLw8SNWE:1rzK1p:qtT_9cTRGlmqCP1mnyIlhN030jFAnXo1ZjkQ-_PYLL4','2024-05-07 17:34:01.863569'),('t1cum336efbzcamumioyi5m27yobof9w','.eJxVi7sOwyAMAP-FOarCw8F0rJTvQMYYgdpkKMlU9d-bbsl4d7qPirRvNe5d3rFldVca1XCWifgp678srW_C9TYv1F6PQ89rvsB1rNTrcWVnUvHE6DBnAWYJ1kkyASGNDHryxRChgLEjgp2YAuvkwYsVgyWo7w8JwzUE:1s8U4n:VygM6Ie227HKUfBsT9IT8rMY1VT31sbTU5EuHSBjkqI','2024-06-02 00:06:57.136174'),('t4izwk1eweb2ghj2fr70h8a8nbkled1l','.eJxVi8EOwiAQBf-FszHAmkI8mvQ7yGN3CUTbg7Snxn8Xb_Y4M5nDJOxbTXvXd2pi7mYyl3-XwU9df2FpfVOu13lBez2Gnlc5wXms6HVcTMSFJRdmYZLicnDeKWxW8bZMoyhBKVD0AmJrrSjE3YCoCNF8vibFNp8:1rm6Kr:BKp1rDipdJFPiTNO2MRBKUB7Q0ilF-LFnhLp62op1sA','2024-04-01 06:19:01.224944'),('t9v0ud6fpkbby9une9jent8mui26fu48','.eJxVi0EOwiAQAP_C2RgWWAoeTfoOsrBLINoepD0Z_2692ePMZN4q0b61tA95pc7qpkBd_l2m8pD1F5Y-NintOi_Un_dDzyuf4Dw2Gu24LBZBFvAmotXeI0zGVWfZamIqwBgg6uKzsM4GEWMNFExlHzKYyanPF6qcM8U:1rqQBq:4X_hisbXDO9dO94NGvowySvAWvdsrWshuw57c8R8BLE','2024-04-13 04:19:34.733404'),('xvg01ks5rpfz7myf9upzokh540kwjdcr','.eJxVizEOwyAMAP_iuaqCgQQ6Vso7kLGNQG0ylGSq-vemWzPene4Nifatpr3rKzWBGxgHl3-ZiR-6_srS-qZcr_NC7Xk_9LzKCc5jpV6Py1uaxAY2o1B0pWRCjgaVBzE-cCEkNkqeJWdyODLihMEOIUtURA-fLw8SNWE:1s8U0r:KXpIC46uF0R8z2VzJGJt4hhv4NzI_uzNyoVJ1ItVl4Y','2024-06-02 00:02:53.884493');
/*!40000 ALTER TABLE django_session ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_admin`
--

DROP TABLE IF EXISTS mistech_admin;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_admin (
  id int NOT NULL AUTO_INCREMENT,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  admin_id bigint NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY admin_id (admin_id),
  CONSTRAINT mistech_admin_admin_id_1aa101ff_fk_mistech_customuser_id FOREIGN KEY (admin_id) REFERENCES mistech_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_admin`
--

LOCK TABLES mistech_admin WRITE;
/*!40000 ALTER TABLE mistech_admin DISABLE KEYS */;
INSERT INTO mistech_admin VALUES (1,'2024-02-18 15:51:31.581042','2024-02-18 15:51:31.581042',1),(2,'2024-09-30 08:32:56.673789','2024-09-30 08:32:56.673789',21);
/*!40000 ALTER TABLE mistech_admin ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_attendance`
--

DROP TABLE IF EXISTS mistech_attendance;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_attendance (
  at_id int NOT NULL AUTO_INCREMENT,
  at_date datetime(6) NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  b_id_id int NOT NULL,
  c_id_id int NOT NULL,
  sf_id_id bigint NOT NULL,
  st_id_id int NOT NULL,
  sub_id_id int NOT NULL,
  yr_id_id int NOT NULL,
  PRIMARY KEY (at_id),
  KEY mistech_attendance_b_id_id_f8a9ef87_fk_mistech_batch_b_id (b_id_id),
  KEY mistech_attendance_c_id_id_930eb681_fk_mistech_course_c_id (c_id_id),
  KEY mistech_attendance_sf_id_id_43759620_fk_mistech_customuser_id (sf_id_id),
  KEY mistech_attendance_st_id_id_024d8111_fk_mistech_student_st_id (st_id_id),
  KEY mistech_attendance_sub_id_id_da9ad9ee_fk_mistech_subject_sub_id (sub_id_id),
  KEY mistech_attendance_yr_id_id_f5e2888a_fk_mistech_sessionyr_yr_id (yr_id_id),
  CONSTRAINT mistech_attendance_b_id_id_f8a9ef87_fk_mistech_batch_b_id FOREIGN KEY (b_id_id) REFERENCES mistech_batch (b_id),
  CONSTRAINT mistech_attendance_c_id_id_930eb681_fk_mistech_course_c_id FOREIGN KEY (c_id_id) REFERENCES mistech_course (c_id),
  CONSTRAINT mistech_attendance_sf_id_id_43759620_fk_mistech_customuser_id FOREIGN KEY (sf_id_id) REFERENCES mistech_customuser (id),
  CONSTRAINT mistech_attendance_st_id_id_024d8111_fk_mistech_student_st_id FOREIGN KEY (st_id_id) REFERENCES mistech_student (st_id),
  CONSTRAINT mistech_attendance_sub_id_id_da9ad9ee_fk_mistech_subject_sub_id FOREIGN KEY (sub_id_id) REFERENCES mistech_subject (sub_id),
  CONSTRAINT mistech_attendance_yr_id_id_f5e2888a_fk_mistech_sessionyr_yr_id FOREIGN KEY (yr_id_id) REFERENCES mistech_sessionyr (yr_id)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_attendance`
--

LOCK TABLES mistech_attendance WRITE;
/*!40000 ALTER TABLE mistech_attendance DISABLE KEYS */;
INSERT INTO mistech_attendance VALUES (1,'2024-02-21 21:20:50.362393','Present','2024-02-21 21:20:50.362393','2024-02-21 21:20:50.362393',1,1,4,2,1,1),(2,'2024-02-21 21:20:50.372974','Absent','2024-02-21 21:20:50.372974','2024-02-21 21:20:50.372974',1,1,4,3,1,1),(3,'2024-02-21 22:09:28.586662','Present','2024-02-21 22:09:28.586662','2024-02-21 22:09:28.586662',4,1,4,4,1,1),(4,'2024-02-21 22:11:26.874553','Present','2024-02-21 22:11:26.874553','2024-02-21 22:11:26.874553',1,1,4,3,1,1),(5,'2024-02-21 22:11:26.892534','Absent','2024-02-21 22:11:26.892534','2024-02-21 22:11:26.892534',1,1,4,2,1,1),(6,'2024-02-21 22:25:17.529581','Present','2024-02-21 22:25:17.529581','2024-02-21 22:25:17.529581',1,1,4,2,1,1),(7,'2024-02-21 22:25:17.554789','Absent','2024-02-21 22:25:17.554789','2024-02-21 22:25:17.554789',1,1,4,3,1,1),(8,'2024-02-21 23:57:24.508763','Present','2024-02-21 23:57:24.508763','2024-02-21 23:57:24.508763',1,1,4,2,1,1),(9,'2024-02-21 23:57:24.516363','Absent','2024-02-21 23:57:24.516363','2024-02-21 23:57:24.516363',1,1,4,3,1,1),(10,'2024-02-22 06:12:08.459798','Present','2024-02-22 06:12:08.459798','2024-02-22 06:12:08.459798',1,1,4,3,1,1),(11,'2024-02-22 06:12:08.491018','Absent','2024-02-22 06:12:08.491018','2024-02-22 06:12:08.491018',1,1,4,2,1,1),(12,'2024-02-22 06:30:43.122245','Present','2024-02-22 06:30:43.122245','2024-02-22 06:30:43.122245',3,2,4,5,6,3),(13,'2024-02-22 06:30:43.132126','Absent','2024-02-22 06:30:43.132126','2024-02-22 06:30:43.132126',3,2,4,1,6,3),(14,'2024-02-22 06:34:08.281105','Present','2024-02-22 06:34:08.281105','2024-02-22 06:34:08.281105',1,1,4,3,1,1),(15,'2024-02-22 06:34:08.298082','Absent','2024-02-22 06:34:08.298082','2024-02-22 06:34:08.298082',1,1,4,2,1,1),(16,'2024-02-22 06:37:13.049305','Present','2024-02-22 06:37:13.049305','2024-02-22 06:37:13.049305',3,2,4,1,6,3),(17,'2024-02-22 06:37:13.064916','Absent','2024-02-22 06:37:13.064916','2024-02-22 06:37:13.064916',3,2,4,5,6,3),(18,'2024-02-22 06:37:27.365229','Present','2024-02-22 06:37:27.365229','2024-02-22 06:37:27.365229',3,2,4,5,6,3),(19,'2024-03-29 18:52:36.170995','Present','2024-03-29 18:52:36.170995','2024-03-29 18:52:36.170995',1,1,2,3,1,1),(20,'2024-03-29 18:52:36.175667','Absent','2024-03-29 18:52:36.175667','2024-03-29 18:52:36.175667',1,1,2,2,1,1),(21,'2024-03-29 18:55:11.559172','Present','2024-03-29 18:55:11.559172','2024-03-29 18:55:11.559172',1,1,2,2,1,1),(22,'2024-03-29 18:55:11.575124','Absent','2024-03-29 18:55:11.575124','2024-03-29 18:55:11.575124',1,1,2,3,1,1),(23,'2024-03-29 18:55:23.401227','Present','2024-03-29 18:55:23.401227','2024-03-29 18:55:23.401227',1,1,2,3,1,1),(24,'2024-03-30 04:21:49.766927','Present','2024-03-30 04:21:49.766927','2024-03-30 04:21:49.766927',1,1,2,3,1,1),(25,'2024-03-30 04:21:49.783297','Absent','2024-03-30 04:21:49.783297','2024-03-30 04:21:49.783297',1,1,2,2,1,1),(26,'2024-05-18 15:11:56.202759','Present','2024-05-18 15:11:56.202759','2024-05-18 15:11:56.202759',1,1,4,10,1,1),(27,'2024-05-18 15:11:56.202759','Absent','2024-05-18 15:11:56.202759','2024-05-18 15:11:56.202759',1,1,4,2,1,1),(28,'2024-05-18 15:11:56.220045','Absent','2024-05-18 15:11:56.220045','2024-05-18 15:11:56.220045',1,1,4,3,1,1),(29,'2024-05-18 15:14:56.731006','Present','2024-05-18 15:14:56.731006','2024-05-18 15:14:56.731006',1,1,4,10,1,1),(30,'2024-05-18 15:14:56.747653','Absent','2024-05-18 15:14:56.747653','2024-05-18 15:14:56.747653',1,1,4,2,1,1),(31,'2024-05-18 15:14:56.754846','Absent','2024-05-18 15:14:56.754846','2024-05-18 15:14:56.754846',1,1,4,3,1,1),(32,'2024-05-19 03:46:52.934981','Present','2024-05-19 03:46:52.934981','2024-05-19 03:46:52.934981',1,1,2,10,1,1),(33,'2024-05-19 03:46:52.951513','Absent','2024-05-19 03:46:52.951513','2024-05-19 03:46:52.951513',1,1,2,2,1,1),(34,'2024-05-19 03:46:52.951513','Absent','2024-05-19 03:46:52.951513','2024-05-19 03:46:52.951513',1,1,2,3,1,1),(35,'2024-05-19 07:46:28.778907','Present','2024-05-19 07:46:28.778907','2024-05-19 07:46:28.778907',1,1,2,10,1,1),(36,'2024-05-19 07:46:28.778907','Absent','2024-05-19 07:46:28.778907','2024-05-19 07:46:28.778907',1,1,2,2,1,1),(37,'2024-05-19 07:46:28.800095','Absent','2024-05-19 07:46:28.800095','2024-05-19 07:46:28.800095',1,1,2,3,1,1);
/*!40000 ALTER TABLE mistech_attendance ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_attendancee`
--

DROP TABLE IF EXISTS mistech_attendancee;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_attendancee (
  ae_id int NOT NULL AUTO_INCREMENT,
  ae_date datetime(6) NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  ex_name varchar(200) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  b_id_id int NOT NULL,
  c_id_id int NOT NULL,
  sf_id_id bigint NOT NULL,
  st_id_id int NOT NULL,
  sub_id_id int NOT NULL,
  yr_id_id int NOT NULL,
  PRIMARY KEY (ae_id),
  KEY mistech_attendancee_b_id_id_79c30e90_fk_mistech_batch_b_id (b_id_id),
  KEY mistech_attendancee_c_id_id_0ff016af_fk_mistech_course_c_id (c_id_id),
  KEY mistech_attendancee_sf_id_id_fd05dc8d_fk_mistech_customuser_id (sf_id_id),
  KEY mistech_attendancee_st_id_id_0374a084_fk_mistech_student_st_id (st_id_id),
  KEY mistech_attendancee_sub_id_id_99c833f7_fk_mistech_subject_sub_id (sub_id_id),
  KEY mistech_attendancee_yr_id_id_98865aee_fk_mistech_sessionyr_yr_id (yr_id_id),
  CONSTRAINT mistech_attendancee_b_id_id_79c30e90_fk_mistech_batch_b_id FOREIGN KEY (b_id_id) REFERENCES mistech_batch (b_id),
  CONSTRAINT mistech_attendancee_c_id_id_0ff016af_fk_mistech_course_c_id FOREIGN KEY (c_id_id) REFERENCES mistech_course (c_id),
  CONSTRAINT mistech_attendancee_sf_id_id_fd05dc8d_fk_mistech_customuser_id FOREIGN KEY (sf_id_id) REFERENCES mistech_customuser (id),
  CONSTRAINT mistech_attendancee_st_id_id_0374a084_fk_mistech_student_st_id FOREIGN KEY (st_id_id) REFERENCES mistech_student (st_id),
  CONSTRAINT mistech_attendancee_sub_id_id_99c833f7_fk_mistech_subject_sub_id FOREIGN KEY (sub_id_id) REFERENCES mistech_subject (sub_id),
  CONSTRAINT mistech_attendancee_yr_id_id_98865aee_fk_mistech_sessionyr_yr_id FOREIGN KEY (yr_id_id) REFERENCES mistech_sessionyr (yr_id)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_attendancee`
--

LOCK TABLES mistech_attendancee WRITE;
/*!40000 ALTER TABLE mistech_attendancee DISABLE KEYS */;
INSERT INTO mistech_attendancee VALUES (1,'2024-02-23 12:25:45.225806','Present','IT Exam','2024-02-23 12:25:45.225806','2024-02-23 12:25:45.225806',1,1,11,2,1,1),(2,'2024-02-23 12:25:45.242180','Absent','','2024-02-23 12:25:45.242180','2024-02-23 12:25:45.242180',1,1,11,3,1,1),(3,'2024-02-23 12:25:54.125486','Present','IT Exam','2024-02-23 12:25:54.125486','2024-02-23 12:25:54.125486',1,1,11,2,1,1),(4,'2024-02-23 12:25:54.142167','Absent','','2024-02-23 12:25:54.142167','2024-02-23 12:25:54.142167',1,1,11,3,1,1),(5,'2024-02-23 12:34:40.108708','Present','IT Exam 2023','2024-02-23 12:34:40.108708','2024-02-23 12:34:40.108708',1,1,11,2,1,1),(6,'2024-02-23 12:36:07.371412','Present','IT Examination 2023','2024-02-23 12:36:07.387034','2024-02-23 12:36:07.387034',1,1,11,2,1,1),(7,'2024-02-23 12:36:07.403055','Absent','IT Examination 2023','2024-02-23 12:36:07.403055','2024-02-23 12:36:07.403055',1,1,11,3,1,1),(8,'2024-02-23 12:36:15.792074','Present','IT Examination 2023','2024-02-23 12:36:15.792074','2024-02-23 12:36:15.792074',1,1,11,2,1,1),(9,'2024-02-23 12:36:15.816468','Absent','IT Examination 2023','2024-02-23 12:36:15.816468','2024-02-23 12:36:15.816468',1,1,11,3,1,1),(10,'2024-02-23 12:37:06.809109','Present','IT Examination 2023','2024-02-23 12:37:06.809109','2024-02-23 12:37:06.809109',1,1,11,3,1,1),(11,'2024-02-23 12:38:15.158597','Present','IT Examination 2023','2024-02-23 12:38:15.158597','2024-02-23 12:38:15.158597',4,1,11,4,1,1),(12,'2024-02-29 04:31:44.244372','Present','Ex_IT_02','2024-02-29 04:31:44.244372','2024-02-29 04:31:44.244372',1,1,11,3,1,1),(13,'2024-02-29 04:31:44.262379','Absent','Ex_IT_02','2024-02-29 04:31:44.262379','2024-02-29 04:31:44.262379',1,1,11,2,1,1),(14,'2024-03-06 02:48:43.123311','Present','Exam IT 02','2024-03-06 02:48:43.123311','2024-03-06 02:48:43.123311',1,1,11,2,1,1),(15,'2024-03-06 02:48:43.138936','Absent','Exam IT 02','2024-03-06 02:48:43.138936','2024-03-06 02:48:43.138936',1,1,11,3,1,1),(16,'2024-03-06 02:48:53.123391','Present','Exam IT 02','2024-03-06 02:48:53.138995','2024-03-06 02:48:53.138995',1,1,11,2,1,1),(17,'2024-03-06 02:48:53.154836','Absent','Exam IT 02','2024-03-06 02:48:53.154836','2024-03-06 02:48:53.154836',1,1,11,3,1,1),(18,'2024-03-06 02:49:25.758945','Present','','2024-03-06 02:49:25.758945','2024-03-06 02:49:25.758945',1,1,11,3,1,1),(19,'2024-03-06 02:49:25.775233','Absent','','2024-03-06 02:49:25.775233','2024-03-06 02:49:25.775233',1,1,11,2,1,1),(20,'2024-03-06 06:59:01.084574','Present','Ex-02','2024-03-06 06:59:01.084574','2024-03-06 06:59:01.084574',1,1,11,2,1,1),(21,'2024-03-06 06:59:01.116008','Absent','Ex-02','2024-03-06 06:59:01.116008','2024-03-06 06:59:01.116008',1,1,11,3,1,1),(22,'2024-03-07 04:43:43.868206','Present','Ex','2024-03-07 04:43:43.868206','2024-03-07 04:43:43.868206',1,1,11,2,1,1),(23,'2024-03-07 04:43:43.869606','Absent','Ex','2024-03-07 04:43:43.869606','2024-03-07 04:43:43.869606',1,1,11,3,1,1),(24,'2024-03-07 04:44:07.836733','Present','Ex','2024-03-07 04:44:07.836733','2024-03-07 04:44:07.836733',1,1,11,2,1,1),(25,'2024-03-07 04:44:07.853144','Absent','Ex','2024-03-07 04:44:07.853144','2024-03-07 04:44:07.853144',1,1,11,3,1,1),(26,'2024-03-07 04:44:19.988499','Present','','2024-03-07 04:44:19.988499','2024-03-07 04:44:19.988499',1,1,11,2,1,1),(27,'2024-03-07 04:44:20.005431','Absent','','2024-03-07 04:44:20.005431','2024-03-07 04:44:20.005431',1,1,11,3,1,1),(28,'2024-03-07 04:44:26.816593','Present','','2024-03-07 04:44:26.816593','2024-03-07 04:44:26.816593',1,1,11,2,1,1),(29,'2024-03-07 04:44:26.832237','Absent','','2024-03-07 04:44:26.832237','2024-03-07 04:44:26.832237',1,1,11,3,1,1),(30,'2024-03-07 04:44:35.337636','Present','','2024-03-07 04:44:35.337636','2024-03-07 04:44:35.337636',1,1,11,3,1,1);
/*!40000 ALTER TABLE mistech_attendancee ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_batch`
--

DROP TABLE IF EXISTS mistech_batch;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_batch (
  b_id int NOT NULL AUTO_INCREMENT,
  b_code varchar(50) NOT NULL,
  sem_no varchar(1) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  c_id_id int NOT NULL,
  PRIMARY KEY (b_id),
  UNIQUE KEY b_code (b_code),
  KEY mistech_batch_c_id_id_25e8fa4c_fk_mistech_course_c_id (c_id_id),
  CONSTRAINT mistech_batch_c_id_id_25e8fa4c_fk_mistech_course_c_id FOREIGN KEY (c_id_id) REFERENCES mistech_course (c_id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_batch`
--

LOCK TABLES mistech_batch WRITE;
/*!40000 ALTER TABLE mistech_batch DISABLE KEYS */;
INSERT INTO mistech_batch VALUES (1,'2024 ECC 12 B1','1','2024-02-19 00:35:38.119016','2024-02-19 00:35:38.119016',1),(2,'2024 ECC 05 B1','1','2024-02-19 00:36:14.775766','2024-02-19 00:36:14.775766',3),(3,'2024 ESC 02 B1','1','2024-02-19 00:36:28.367051','2024-02-19 00:36:28.367051',2),(4,'2024 ECC 12 B2','1','2024-02-20 04:21:08.623443','2024-02-20 04:21:08.623443',1);
/*!40000 ALTER TABLE mistech_batch ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_course`
--

DROP TABLE IF EXISTS mistech_course;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_course (
  c_id int NOT NULL AUTO_INCREMENT,
  c_name varchar(255) NOT NULL,
  c_code varchar(255) NOT NULL,
  c_type varchar(10) NOT NULL,
  c_duration varchar(4) NOT NULL,
  c_qualification varchar(5) DEFAULT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  tr_id_id int NOT NULL,
  PRIMARY KEY (c_id),
  UNIQUE KEY c_name (c_name),
  UNIQUE KEY c_code (c_code),
  KEY mistech_course_tr_id_id_c7ba86fa_fk_mistech_trade_tr_id (tr_id_id),
  CONSTRAINT mistech_course_tr_id_id_c7ba86fa_fk_mistech_trade_tr_id FOREIGN KEY (tr_id_id) REFERENCES mistech_trade (tr_id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_course`
--

LOCK TABLES mistech_course WRITE;
/*!40000 ALTER TABLE mistech_course DISABLE KEYS */;
INSERT INTO mistech_course VALUES (1,'Information Communication Technology Technician','ECC 12','FT','6M','NVQ4','2024-02-19 00:23:14.840877','2024-02-19 00:23:14.840877',1),(2,'National Certificate in Professional English','ESC 02','FT','12M','Certi','2024-02-19 00:24:08.373272','2024-02-19 00:24:08.373272',2),(3,'Refrigeration & Air Conditioning','ECC 05','FT','12M','NVQ4','2024-02-19 00:24:55.923848','2024-02-19 00:24:55.923848',3),(4,'National Certificate In Engineering Craft Practice (Electronics)','ECC 08','FT','24M','NVQ4','2024-05-18 23:48:30.801082','2024-05-18 23:48:30.801082',4);
/*!40000 ALTER TABLE mistech_course ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_customuser`
--

DROP TABLE IF EXISTS mistech_customuser;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_customuser (
  id bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  last_login datetime(6) DEFAULT NULL,
  is_superuser tinyint(1) NOT NULL,
  username varchar(150) NOT NULL,
  first_name varchar(150) NOT NULL,
  last_name varchar(150) NOT NULL,
  email varchar(254) NOT NULL,
  is_staff tinyint(1) NOT NULL,
  is_active tinyint(1) NOT NULL,
  date_joined datetime(6) NOT NULL,
  user_type varchar(10) NOT NULL,
  profile_img varchar(100) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_customuser`
--

LOCK TABLES mistech_customuser WRITE;
/*!40000 ALTER TABLE mistech_customuser DISABLE KEYS */;
INSERT INTO mistech_customuser VALUES (1,'pbkdf2_sha256$600000$PxWJyKAzQ6IGVLK4N1TwiV$HTFKep6UNtFdIPgmb7cdQ3bS4nnAbwp/APPmpO8vG0M=','2024-05-19 09:12:35.360970',1,'admin','','','admin@gmail.com',1,1,'2024-02-18 15:51:31.408192','1',''),(2,'pbkdf2_sha256$600000$7o5GPBVnuQmiGxuKBQR6EU$5Up51VrWwFxOkLNQU7v1nYXudRKsqzPtvAEGKYlUZSo=','2024-09-30 07:36:57.340523',0,'Priyantha','Priyantha','D','stechnologyfr@gmail.com',0,1,'2024-02-19 01:06:34.189068','4','user_img/SF_IT_01_CFZQjOs.jpg'),(3,'pbkdf2_sha256$600000$YUSq21mDLjcBeAyvsXaaqQ$FbZsqIv0VnldMKX9UkO3CUcBm1seGum0Ns3LIyibD+Q=','2024-03-06 02:52:10.517922',0,'Pushpakumara','Pushpakumara','K','pushpakumara@gmail.com',0,1,'2024-02-19 01:10:43.770146','4','user_img/SF_REF_01_FwItr1Q.jpg'),(4,'pbkdf2_sha256$600000$l3LaOzGqjY62ld4T89IANV$dVW4kNZDkytMFTiHfCS2ALc34gbeTpuTIoB9JRCwizc=','2024-05-18 23:55:14.315115',0,'San','Sanjani','Thilakarathne','sanjaniut@gmail.com',0,1,'2024-02-19 01:12:53.154571','4','user_img/IT2024_5TjyrP1.jpg'),(5,'pbkdf2_sha256$600000$uLolBLSrzjDXu6mlHBmmUq$eeuEF5aAbirZfhcOcyPaKCYqX48OYl5D0z10ofyblDY=',NULL,0,'Claudent','Claudent','Berenjer','claudent@gmail.com',0,1,'2024-02-20 04:12:36.872398','3','user_img/ST_ENG_01_MJMV9Yw.jpg'),(6,'pbkdf2_sha256$600000$QFylRxvyOsqwVWFSASOz0k$UMH2JItAaq3YTSaNOrF2BrlqLewG4Wbp7dBRmnnirew=','2024-05-17 10:48:25.713198',0,'Nishadhi','Nishadhi','Sathya','nishadhi@gmail.com',0,1,'2024-02-20 04:16:33.112720','3','user_img/ST_IT_01_eVS9JA9.jpg'),(7,'pbkdf2_sha256$600000$HJzP7I33Y2FoMdEpIkAxaa$uZJ4fqBFNAOcPbAVexTrSm/z65IIj87kRyMYNH3gcEg=','2024-05-19 02:51:49.859321',0,'Devitha','Devitha','Indrawimala','sanjani.ud@gmail.com',0,1,'2024-02-20 04:20:30.266556','3','user_img/ST_IT_02_J83VdJm.jpg'),(8,'pbkdf2_sha256$600000$IX0ZumAJahJujtjp4qu6xI$Kd5CC+zcq+Kv1GduLRHNbQ3xI9NRIxaNeABczulXlAI=','2024-03-29 10:42:19.230053',0,'Nianka','Nilanka','Jayasundara','nilanka@gmail.com',0,1,'2024-02-20 05:21:10.211463','3','user_img/ST_IT_03_erKqEiT.jpg'),(9,'pbkdf2_sha256$600000$eJzk1l4HEv472Uwr1b2Vbx$E8oHBwlwpgGIUAv+5tdUuk3bVyIdsa/hoUSq0rCXCkQ=','2024-03-03 10:14:32.808409',0,'Madhuwanthi','Madhuwanthi','Wijesooriya','madhuwanthi@gmail.com',0,1,'2024-02-22 06:21:27.622287','3','user_img/ST_ENG_02_OmA8xOt.jpg'),(10,'pbkdf2_sha256$600000$bHLMjsfP8o28TLigNESRHG$5uXqyu1C5ixpS96wmDkjGYM2i6qjuSJkomulFA4yvxI=','2024-02-22 14:46:30.802713',0,'Quleen','Merry','Kelly','quleen@gmail.com',0,1,'2024-02-22 06:27:24.793414','4','user_img/SF_Eng_01.jpg'),(11,'pbkdf2_sha256$600000$UwKrQlxeePW6DoRDAYp3xg$Sm7FvutLPGw+3ei+cSqsNZXHMF1WUSwLIUyPxqfIH3s=','2024-05-18 23:51:22.575763',0,'Madhuranga','Madhuranga','Nanayakkara','madhuranga@gmail.com',0,1,'2024-02-23 05:11:26.729108','5','user_img/Eng2024_di2ZLoZ.jpg'),(12,'pbkdf2_sha256$600000$R1zuNCPXV0Wb2kBfMGPjVY$wM59//BT6EuJut7CQMyoY3qBKIEEAzQVcmDT5PEwPko=',NULL,0,'Dushan','Dushan','Dharshana','dushan@gmail.com',0,1,'2024-03-02 13:35:54.909417','3','user_img/ST_REF_01_SdotHiC.jpg'),(13,'pbkdf2_sha256$600000$nV3k2y5GWJpESlE75f5ns7$C0BCs65ZfTGAXIUy+WAMrHhsv124ovwh4QcQVOekc8I=','2024-03-03 16:13:37.483277',0,'sanjana','sanjana','Udayanga','sanjaniudayangani@gmail.com',0,1,'2024-03-02 13:41:17.296103','3','user_img/ST_IT_04_VOLvMyw.jpg'),(14,'pbkdf2_sha256$600000$KwBrz6Zut99JIrCs9pz5J9$i9LCW/Puo3ao0acaWwzoNZiuKATjkliuabV+fWhqH5M=','2024-09-30 08:22:11.245929',0,'Suriyaarachchi','T','Suriyaarachchi','suriyaarachchi@gamail.com',0,1,'2024-03-06 02:55:57.463271','6','user_img/SF_Principal.jpg'),(15,'pbkdf2_sha256$600000$2rpFszshl43RXhvUWJsCOs$gOnITOd74qwo3cFn6mDaotjXAfOTRoD1/biMzdIJxAI=',NULL,0,'Tishan','Tishan','Fernando','tishan@gmail.com',0,1,'2024-03-06 17:42:03.836580','4','user_img/SF_Civil_01_K2458OT.jpg'),(16,'pbkdf2_sha256$600000$13ZVl3ijKhQFxAZnBdP1jS$8LYU3Ez8KKfoxJMfvQy9qHLguDoxwpqS2YJNU5kqip4=',NULL,0,'Lasanthi','Lasanthi','Silva','lnc@ucsc.cmb.ac.lk',0,1,'2024-03-29 19:29:16.158046','3','user_img/LNC_RscQVkR.jpg'),(17,'pbkdf2_sha256$600000$KiRbKIK3FajliThWLMomq5$y9lYnxKadEY5zJ7wz1Bs3Eo5h0xQWSsa5d3Yhaq2g5o=',NULL,0,'Viraj','Viraj','Welgama','wvw@ucsc.cmb.ac.lk',0,1,'2024-03-29 19:33:25.673858','3',''),(18,'pbkdf2_sha256$600000$OYaNSa2gLiHChKyCpRZF4Q$JopRQHZgsys8tOuz3wxUUSLGMRJ5d8d95VkwGRVi3jE=','2024-09-30 07:48:45.368160',0,'sanjeevani','Sanjeevani','Thilakarathene','sanjeekht@gmail.com',0,1,'2024-05-17 06:31:08.705292','3','user_img/ST_IT_05_HIM261i.jpg'),(19,'pbkdf2_sha256$600000$FOtRb13X3nVydcMjSVyJJ9$L/ZPUtBjvaU2+AexnaPLYZ83G/xvoa6jB+tUpb7Gc0Y=',NULL,0,'ab','ab','ab','ab@gmail.com',0,1,'2024-05-18 23:38:42.814013','4','user_img/avatar2_Po8Llt6.png'),(20,'pbkdf2_sha256$600000$zC7heLu92MnxTymkT8HIFk$g6p9eMmNwOc6vsG3x+zsjhA6dLNfETaTN49zJkYqyAY=',NULL,0,'ex','ex','ex','ex@gmail.com',0,1,'2024-05-18 23:44:26.386096','3','user_img/avatar04_Bq8Lwku.png'),(21,'pbkdf2_sha256$600000$9VXfctEQiywhOHMLOiGjSm$6soXf89YGPZBTyw7HibXyv8b+CuXIr8+DVaLykgM9xw=','2024-09-30 08:33:25.898950',1,'st@gmail.com','','','sat@gmail.com',1,1,'2024-09-30 08:32:56.500751','1','');
/*!40000 ALTER TABLE mistech_customuser ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_customuser_groups`
--

DROP TABLE IF EXISTS mistech_customuser_groups;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_customuser_groups (
  id bigint NOT NULL AUTO_INCREMENT,
  customuser_id bigint NOT NULL,
  group_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY mistech_customuser_groups_customuser_id_group_id_8eab33da_uniq (customuser_id,group_id),
  KEY mistech_customuser_groups_group_id_b39e8279_fk_auth_group_id (group_id),
  CONSTRAINT mistech_customuser_g_customuser_id_49720994_fk_mistech_c FOREIGN KEY (customuser_id) REFERENCES mistech_customuser (id),
  CONSTRAINT mistech_customuser_groups_group_id_b39e8279_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_customuser_groups`
--

LOCK TABLES mistech_customuser_groups WRITE;
/*!40000 ALTER TABLE mistech_customuser_groups DISABLE KEYS */;
/*!40000 ALTER TABLE mistech_customuser_groups ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_customuser_user_permissions`
--

DROP TABLE IF EXISTS mistech_customuser_user_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_customuser_user_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  customuser_id bigint NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY mistech_customuser_user__customuser_id_permission_cf71b392_uniq (customuser_id,permission_id),
  KEY mistech_customuser_u_permission_id_174efafa_fk_auth_perm (permission_id),
  CONSTRAINT mistech_customuser_u_customuser_id_0d23e515_fk_mistech_c FOREIGN KEY (customuser_id) REFERENCES mistech_customuser (id),
  CONSTRAINT mistech_customuser_u_permission_id_174efafa_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_customuser_user_permissions`
--

LOCK TABLES mistech_customuser_user_permissions WRITE;
/*!40000 ALTER TABLE mistech_customuser_user_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE mistech_customuser_user_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_feedbacks`
--

DROP TABLE IF EXISTS mistech_feedbacks;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_feedbacks (
  fb_id int NOT NULL AUTO_INCREMENT,
  fb varchar(255) NOT NULL,
  fb_rpy longtext NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  st_id_id int NOT NULL,
  PRIMARY KEY (fb_id),
  KEY mistech_feedbacks_st_id_id_949d723c_fk_mistech_student_st_id (st_id_id),
  CONSTRAINT mistech_feedbacks_st_id_id_949d723c_fk_mistech_student_st_id FOREIGN KEY (st_id_id) REFERENCES mistech_student (st_id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_feedbacks`
--

LOCK TABLES mistech_feedbacks WRITE;
/*!40000 ALTER TABLE mistech_feedbacks DISABLE KEYS */;
INSERT INTO mistech_feedbacks VALUES (1,'Need to contact','We will contact you as soon as possible','2024-03-19 20:13:35.866355','2024-03-19 20:41:32.430276',2),(2,'test 1','','2024-05-19 00:07:56.180855','2024-05-19 00:07:56.180855',10);
/*!40000 ALTER TABLE mistech_feedbacks ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_feedbacksf`
--

DROP TABLE IF EXISTS mistech_feedbacksf;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_feedbacksf (
  fbs_id int NOT NULL AUTO_INCREMENT,
  fbs varchar(255) NOT NULL,
  fbs_rpy longtext NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  sf_id_id int NOT NULL,
  PRIMARY KEY (fbs_id),
  KEY mistech_feedbacksf_sf_id_id_3de70eae_fk_mistech_staff_sf_id (sf_id_id),
  CONSTRAINT mistech_feedbacksf_sf_id_id_3de70eae_fk_mistech_staff_sf_id FOREIGN KEY (sf_id_id) REFERENCES mistech_staff (sf_id)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_feedbacksf`
--

LOCK TABLES mistech_feedbacksf WRITE;
/*!40000 ALTER TABLE mistech_feedbacksf DISABLE KEYS */;
INSERT INTO mistech_feedbacksf VALUES (1,'Test','Thanks for the message.','2024-03-06 20:01:18.752138','2024-03-19 20:39:45.296513',3),(2,'Test 1','t1','2024-03-07 05:44:52.908076','2024-05-18 11:12:45.064491',3),(3,'Test','','2024-03-30 04:24:51.002752','2024-03-30 04:24:51.002752',1),(4,'testing','testing','2024-05-18 10:44:00.023631','2024-05-18 11:19:07.073511',1),(5,'test 2','t2','2024-05-18 10:58:45.144220','2024-05-18 11:13:55.091038',1),(6,'test ','reply1','2024-05-19 07:53:08.920186','2024-05-19 07:54:14.165480',1);
/*!40000 ALTER TABLE mistech_feedbacksf ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_leavereports`
--

DROP TABLE IF EXISTS mistech_leavereports;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_leavereports (
  lr_id int NOT NULL AUTO_INCREMENT,
  lr_date date NOT NULL,
  lr_msg longtext NOT NULL,
  lr_status int NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  st_id_id int NOT NULL,
  PRIMARY KEY (lr_id),
  KEY mistech_leavereports_st_id_id_66442b19_fk_mistech_student_st_id (st_id_id),
  CONSTRAINT mistech_leavereports_st_id_id_66442b19_fk_mistech_student_st_id FOREIGN KEY (st_id_id) REFERENCES mistech_student (st_id)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_leavereports`
--

LOCK TABLES mistech_leavereports WRITE;
/*!40000 ALTER TABLE mistech_leavereports DISABLE KEYS */;
INSERT INTO mistech_leavereports VALUES (1,'2023-12-26','Formal leave',1,'2024-03-19 20:11:31.650133','2024-03-19 20:44:24.038168',2),(2,'2024-03-14','Personal',2,'2024-03-30 04:26:08.751223','2024-05-17 12:02:48.290952',2),(3,'2024-05-18','sick leave',0,'2024-05-17 11:59:24.087509','2024-05-17 11:59:24.087509',2);
/*!40000 ALTER TABLE mistech_leavereports ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_leavereportsf`
--

DROP TABLE IF EXISTS mistech_leavereportsf;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_leavereportsf (
  lrs_id int NOT NULL AUTO_INCREMENT,
  lrs_date date NOT NULL,
  lrs_msg longtext NOT NULL,
  lrs_status int NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  sf_id_id int NOT NULL,
  medical_img varchar(100) DEFAULT NULL,
  reason_lv longtext,
  PRIMARY KEY (lrs_id),
  KEY mistech_leavereportsf_sf_id_id_71676084_fk_mistech_staff_sf_id (sf_id_id),
  CONSTRAINT mistech_leavereportsf_sf_id_id_71676084_fk_mistech_staff_sf_id FOREIGN KEY (sf_id_id) REFERENCES mistech_staff (sf_id)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_leavereportsf`
--

LOCK TABLES mistech_leavereportsf WRITE;
/*!40000 ALTER TABLE mistech_leavereportsf DISABLE KEYS */;
INSERT INTO mistech_leavereportsf VALUES (1,'2023-10-12','Sick Leave',1,'2024-03-06 02:39:32.279078','2024-03-06 19:58:06.473135',3,NULL,'True'),(2,'2024-01-17','Personal Reason',2,'2024-03-06 20:02:24.918087','2024-03-06 20:04:22.772242',1,NULL,'True'),(3,'2024-01-04','formal leave',1,'2024-03-19 20:10:47.535414','2024-05-19 00:31:55.715418',3,'','True'),(4,'2024-03-19','Medical',1,'2024-03-30 04:24:03.884281','2024-03-30 04:24:29.305947',1,NULL,'True'),(5,'2024-04-06','Medical',1,'2024-03-30 06:01:40.837078','2024-05-15 09:39:08.744669',1,'','True'),(6,'2024-03-05','Personal',1,'2024-03-30 06:16:38.904513','2024-05-19 00:43:13.652692',1,'','True'),(7,'2024-03-15','Personal',1,'2024-03-30 06:44:29.484799','2024-05-19 00:33:07.521833',1,'','True'),(8,'2024-04-18','Medical',1,'2024-04-20 03:34:13.198902','2024-05-19 00:51:36.133036',1,'medical_img/prod-5.jpg','True'),(9,'2024-05-03','Medical',2,'2024-04-20 03:38:04.068607','2024-05-19 08:55:06.411866',1,'medical_img/lesson_plan_data.pdf','True'),(10,'2024-05-19','Medical',1,'2024-05-19 00:54:38.015082','2024-05-19 00:55:11.619307',1,'medical_img/photo1.png','True'),(11,'2024-05-20','Medical',1,'2024-05-19 07:50:09.512701','2024-05-19 07:50:47.866164',1,'medical_img/lesson_plan_data_UJKdyIJ.pdf','True'),(12,'2024-05-22','Casual',2,'2024-05-19 08:39:11.044567','2024-05-19 08:55:51.691542',1,'',NULL),(13,'2024-05-24','Casual',2,'2024-05-19 08:59:40.279343','2024-05-19 09:00:21.847569',1,'',NULL),(14,'2024-05-30','Personal',2,'2024-05-19 08:59:50.850879','2024-05-19 09:01:29.338623',1,'',NULL),(15,'2024-05-24','Casual',1,'2024-05-19 08:59:59.781097','2024-05-19 09:24:36.217048',1,'',NULL);
/*!40000 ALTER TABLE mistech_leavereportsf ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_lplan`
--

DROP TABLE IF EXISTS mistech_lplan;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_lplan (
  lp_id int NOT NULL AUTO_INCREMENT,
  st_activity varchar(255) NOT NULL,
  methodology varchar(255) NOT NULL,
  media varchar(255) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  sf_id_id bigint NOT NULL,
  tk_id_id int NOT NULL,
  lp_time int unsigned NOT NULL,
  PRIMARY KEY (lp_id),
  KEY mistech_lplan_tk_id_id_3fa45854_fk_mistech_task_tk_id (tk_id_id),
  KEY mistech_lplan_sf_id_id_dff91542_fk_mistech_customuser_id (sf_id_id),
  CONSTRAINT mistech_lplan_sf_id_id_dff91542_fk_mistech_customuser_id FOREIGN KEY (sf_id_id) REFERENCES mistech_customuser (id),
  CONSTRAINT mistech_lplan_tk_id_id_3fa45854_fk_mistech_task_tk_id FOREIGN KEY (tk_id_id) REFERENCES mistech_task (tk_id),
  CONSTRAINT mistech_lplan_chk_1 CHECK ((`lp_time` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_lplan`
--

LOCK TABLES mistech_lplan WRITE;
/*!40000 ALTER TABLE mistech_lplan DISABLE KEYS */;
INSERT INTO mistech_lplan VALUES (1,'Listening, Discussion, Observation, and Practice','Writing test and practical test','Multimedia, Instructor Computer, and Computers for each student','2024-03-21 13:53:05.905270','2024-03-21 13:53:05.905270',4,1,1),(2,'Listening, Discussion, Observation, and Practice','Writing test and practical test','Multimedia, Instructor Computer, and Computers for each student','2024-03-21 14:01:32.842485','2024-03-21 14:01:32.842485',4,2,5),(3,'Listening, Discussion, Observation, and Practice','Writing test and practical test','Multimedia, Instructor Computer, and Computers for each student','2024-03-21 14:01:52.725932','2024-03-21 14:01:52.725932',4,3,1),(4,'Listening, Discussion, Observation, and Practice','Writing test and practical test','Multimedia, Instructor Computer, and Computers for each student','2024-03-21 14:02:33.439759','2024-03-21 14:02:33.440249',4,4,2),(5,'Listening, Discussion, Observation, and Practice','Practical test','Multimedia, Instructor Computer, and Computers for each student','2024-03-21 14:03:16.826522','2024-03-21 14:03:16.826522',4,5,2),(6,'Listening, Discussion, Observation, and Practice','Writing test and practical test','Multimedia, Instructor Computer, and Computers for each student','2024-03-22 16:06:28.448259','2024-03-22 16:06:28.448259',2,1,1),(7,'Listening, Discussion, Observation, and Practice','Writing test and practical test','Multimedia, Instructor Computer, and Computers for each student','2024-03-22 16:06:47.545337','2024-03-22 16:06:47.545337',2,2,5),(8,'Practical','Listening','computer','2024-03-30 04:23:10.883727','2024-03-30 04:23:10.883727',2,1,1),(9,'Listening, Discussion, Observation, and Practice','Writing test and practical test','Multimedia, Instructor Computer, and Computers for each student','2024-05-17 12:50:53.892671','2024-05-17 12:50:53.892671',4,1,3),(10,'Practical','Listening','computer','2024-05-19 07:49:26.531340','2024-05-19 07:49:26.531340',2,1,3);
/*!40000 ALTER TABLE mistech_lplan ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_module`
--

DROP TABLE IF EXISTS mistech_module;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_module (
  mod_id int NOT NULL AUTO_INCREMENT,
  mod_code varchar(255) NOT NULL,
  mod_name varchar(255) NOT NULL,
  duration_hours int unsigned NOT NULL,
  academic_weeks int unsigned NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  sub_id_id int NOT NULL,
  c_id_id int NOT NULL,
  PRIMARY KEY (mod_id),
  UNIQUE KEY mod_code (mod_code),
  KEY mistech_module_sub_id_id_2185cb35_fk_mistech_subject_sub_id (sub_id_id),
  KEY mistech_module_c_id_id_95c8edeb_fk_mistech_course_c_id (c_id_id),
  CONSTRAINT mistech_module_c_id_id_95c8edeb_fk_mistech_course_c_id FOREIGN KEY (c_id_id) REFERENCES mistech_course (c_id),
  CONSTRAINT mistech_module_sub_id_id_2185cb35_fk_mistech_subject_sub_id FOREIGN KEY (sub_id_id) REFERENCES mistech_subject (sub_id),
  CONSTRAINT mistech_module_chk_1 CHECK ((`duration_hours` >= 0)),
  CONSTRAINT mistech_module_chk_2 CHECK ((`academic_weeks` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_module`
--

LOCK TABLES mistech_module WRITE;
/*!40000 ALTER TABLE mistech_module DISABLE KEYS */;
INSERT INTO mistech_module VALUES (1,'K72S004M01','Maintaining files & folders',24,3,'2024-03-18 15:52:53.930059','2024-03-18 15:52:53.930059',1,1),(2,'K72S004M02','Performing word processing',24,12,'2024-03-18 16:11:51.810076','2024-03-18 16:11:51.810076',1,1),(3,'K72S004M03','Preparing spread sheets',60,12,'2024-03-18 19:40:03.891432','2024-03-18 19:40:03.891432',4,1),(4,'K72S004M04','Preparing presentations',30,6,'2024-03-18 19:41:34.109801','2024-03-18 19:41:34.109801',7,1),(5,'G50S024BM1','Fundamentals of Refrigeration & Air Conditioning',144,30,'2024-03-18 19:53:55.806422','2024-03-18 19:53:55.806422',2,3),(6,'K72S004M05','Performing basic operations of cloud computing including internet and email services',48,10,'2024-03-21 07:50:09.804214','2024-03-21 07:50:09.804214',8,1);
/*!40000 ALTER TABLE mistech_module ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_notifications`
--

DROP TABLE IF EXISTS mistech_notifications;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_notifications (
  nfy_id int NOT NULL AUTO_INCREMENT,
  notify longtext NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  st_id_id int NOT NULL,
  PRIMARY KEY (nfy_id),
  KEY mistech_notifications_st_id_id_8f5bf9d0_fk_mistech_student_st_id (st_id_id),
  CONSTRAINT mistech_notifications_st_id_id_8f5bf9d0_fk_mistech_student_st_id FOREIGN KEY (st_id_id) REFERENCES mistech_student (st_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_notifications`
--

LOCK TABLES mistech_notifications WRITE;
/*!40000 ALTER TABLE mistech_notifications DISABLE KEYS */;
/*!40000 ALTER TABLE mistech_notifications ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_notificationsf`
--

DROP TABLE IF EXISTS mistech_notificationsf;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_notificationsf (
  nfysf_id int NOT NULL AUTO_INCREMENT,
  notify_sf longtext NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  sf_id_id int NOT NULL,
  is_read tinyint(1) NOT NULL,
  PRIMARY KEY (nfysf_id),
  KEY mistech_notificationsf_sf_id_id_ce5a8375_fk_mistech_staff_sf_id (sf_id_id),
  CONSTRAINT mistech_notificationsf_sf_id_id_ce5a8375_fk_mistech_staff_sf_id FOREIGN KEY (sf_id_id) REFERENCES mistech_staff (sf_id)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_notificationsf`
--

LOCK TABLES mistech_notificationsf WRITE;
/*!40000 ALTER TABLE mistech_notificationsf DISABLE KEYS */;
INSERT INTO mistech_notificationsf VALUES (1,'New feedback message from instructor: Staff object (1)','2024-05-18 10:44:00.038421','2024-05-18 10:44:00.038421',1,0),(2,'New feedback message from instructor: Staff object (1)','2024-05-18 10:58:45.158037','2024-05-18 10:58:45.158037',1,0),(3,'New reply to feedback message with ID: 2','2024-05-18 11:12:45.081004','2024-05-18 11:12:45.081004',3,0),(4,'New reply to feedback message with ID: 5','2024-05-18 11:13:55.096955','2024-05-18 11:13:55.096955',1,0),(5,'New reply to feedback message with ID: 4','2024-05-18 11:19:07.090067','2024-05-18 11:19:07.090067',1,0),(6,'New feedback message from instructor: Staff object (1)','2024-05-19 07:53:08.930051','2024-05-19 07:53:08.930051',1,0),(7,'New reply to feedback message with ID: 6','2024-05-19 07:54:14.180788','2024-05-19 07:54:14.180788',1,0);
/*!40000 ALTER TABLE mistech_notificationsf ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_payment`
--

DROP TABLE IF EXISTS mistech_payment;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_payment (
  pay_id int NOT NULL AUTO_INCREMENT,
  price decimal(10,2) NOT NULL,
  payment_date datetime(6) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  b_id_id int NOT NULL,
  c_id_id int NOT NULL,
  st_id_id int NOT NULL,
  PRIMARY KEY (pay_id),
  KEY mistech_payment_b_id_id_650d4948_fk_mistech_batch_b_id (b_id_id),
  KEY mistech_payment_c_id_id_65d5d6ab_fk_mistech_course_c_id (c_id_id),
  KEY mistech_payment_st_id_id_4c4455bf_fk_mistech_student_st_id (st_id_id),
  CONSTRAINT mistech_payment_b_id_id_650d4948_fk_mistech_batch_b_id FOREIGN KEY (b_id_id) REFERENCES mistech_batch (b_id),
  CONSTRAINT mistech_payment_c_id_id_65d5d6ab_fk_mistech_course_c_id FOREIGN KEY (c_id_id) REFERENCES mistech_course (c_id),
  CONSTRAINT mistech_payment_st_id_id_4c4455bf_fk_mistech_student_st_id FOREIGN KEY (st_id_id) REFERENCES mistech_student (st_id)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_payment`
--

LOCK TABLES mistech_payment WRITE;
/*!40000 ALTER TABLE mistech_payment DISABLE KEYS */;
INSERT INTO mistech_payment VALUES (1,6000.00,'2024-05-17 17:10:17.496825','2024-05-17 17:10:17.496825','2024-05-17 17:10:17.503800',1,1,10),(2,3800.00,'2024-05-17 17:18:51.271635','2024-05-17 17:18:51.272704','2024-05-17 17:18:51.287465',1,1,10),(3,1000.00,'2024-05-17 17:21:36.227659','2024-05-17 17:21:36.227659','2024-05-17 17:21:36.242337',1,1,10),(4,3700.00,'2024-05-17 17:47:48.286359','2024-05-17 17:47:48.286359','2024-05-17 17:47:48.301384',1,1,10),(5,3700.00,'2024-05-17 17:48:19.084494','2024-05-17 17:48:19.084494','2024-05-17 17:48:19.099070',1,1,10),(6,8000.00,'2024-05-17 17:59:45.716840','2024-05-17 17:59:45.716840','2024-05-17 17:59:45.731757',1,1,10),(7,4000.00,'2024-05-17 18:28:11.381541','2024-05-17 18:28:11.381541','2024-05-17 18:28:11.395554',1,1,10),(8,8000.00,'2024-05-18 01:55:24.070962','2024-05-18 01:55:24.070962','2024-05-18 01:55:24.078963',1,1,10),(9,8000.00,'2024-05-18 03:54:18.294690','2024-05-18 03:54:18.294690','2024-05-18 03:54:18.310069',1,1,3),(10,3000.00,'2024-09-30 08:04:48.694024','2024-09-30 08:04:48.694024','2024-09-30 08:04:48.694024',1,1,10);
/*!40000 ALTER TABLE mistech_payment ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_sessionyr`
--

DROP TABLE IF EXISTS mistech_sessionyr;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_sessionyr (
  yr_id int NOT NULL AUTO_INCREMENT,
  session_start date NOT NULL,
  session_end date NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  PRIMARY KEY (yr_id)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_sessionyr`
--

LOCK TABLES mistech_sessionyr WRITE;
/*!40000 ALTER TABLE mistech_sessionyr DISABLE KEYS */;
INSERT INTO mistech_sessionyr VALUES (1,'2023-12-01','2024-07-30','2024-02-20 03:10:04.137313','2024-02-20 03:10:04.137313'),(2,'2023-10-03','2024-04-09','2024-02-20 03:10:43.891828','2024-02-20 03:10:43.891828'),(3,'2024-02-22','2025-03-31','2024-02-20 03:11:14.274038','2024-02-20 03:11:14.274038');
/*!40000 ALTER TABLE mistech_sessionyr ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_staff`
--

DROP TABLE IF EXISTS mistech_staff;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_staff (
  sf_id int NOT NULL AUTO_INCREMENT,
  middle_name varchar(50) DEFAULT NULL,
  dob date NOT NULL,
  adrz varchar(255) DEFAULT NULL,
  gender varchar(10) NOT NULL,
  nic varchar(20) NOT NULL,
  sf_idNo varchar(50) DEFAULT NULL,
  nationality varchar(50) DEFAULT NULL,
  civil_status varchar(10) DEFAULT NULL,
  mobileNo varchar(12) NOT NULL,
  resiNo varchar(11) DEFAULT NULL,
  edu_qualification varchar(10) DEFAULT NULL,
  prof_qualification varchar(255) DEFAULT NULL,
  other_qualification varchar(255) DEFAULT NULL,
  position varchar(20) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  admin_id bigint NOT NULL,
  fcm_token longtext NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (sf_id),
  UNIQUE KEY admin_id (admin_id),
  UNIQUE KEY sf_idNo (sf_idNo),
  CONSTRAINT mistech_staff_admin_id_e839c34f_fk_mistech_customuser_id FOREIGN KEY (admin_id) REFERENCES mistech_customuser (id)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_staff`
--

LOCK TABLES mistech_staff WRITE;
/*!40000 ALTER TABLE mistech_staff DISABLE KEYS */;
INSERT INTO mistech_staff VALUES (1,'Priyantha','1975-02-08','Minuwangoda','M','197589876789','SF_IT_01','Sri Lankan','M','0714417757','0337687656','AL','Degree','Following Diploma in English','Instructor','2024-02-19 01:06:34.750481','2024-02-19 01:06:34.760658',2,''),(2,'Pushpakumara','1976-03-12','Gampaha','M','197698789098','SF_REF_01','Sri Lankan','M','0779975243','0332456787','AL','Degree','Following Diploma in English','Instructor','2024-02-19 01:10:44.340062','2024-02-19 01:10:44.340062',3,''),(3,'San','1990-03-19','Horana','F','199087678987','SF_IT_02','Sri Lankan','UM','0771667608','0115748944','AL','Degree','Following Master Degree','Instructor','2024-02-19 01:12:53.692847','2024-05-17 05:18:04.267908',4,''),(4,'Quleen','1986-01-05','Trincomalee','F','86374876789V','SF_Eng_01','US','M','0783418133','0268909878','AL','Degree','following PHD','Instructor','2024-02-22 06:27:25.053373','2024-02-22 06:27:25.059638',10,''),(5,'Madhuranga','1990-12-08','Galle','M','1990898767876','SF_REF_02','Sri Lankan','M','0778333748','0983456938','AL','Masters','following PHD','Examiner','2024-02-23 05:11:27.000751','2024-02-23 05:11:27.008057',11,''),(6,'M','1976-10-06','Gampaha','M','197687678987','Dir_01','Sri Lankan','M','0763456789','0337678987','AL','Mphil','Following PhD','Principal','2024-03-06 02:55:57.785704','2024-03-06 02:55:57.792838',14,''),(7,'Tishan','1991-12-03','Veyangoda','M','199187656782','SF_Civil_01','Sri Lankan','UM','0768771980','0317678987','AL','Degree','Following Masters Degree','Instructor','2024-03-06 17:42:04.003551','2024-03-06 17:42:04.019697',15,''),(8,'ab','2000-01-02','Colombo','F','200009945678','SF_Eng_02','Sri Lankan','M','0712345679','0112345678','AL','Degree','Diploma in IT','Instructor','2024-05-18 23:38:43.443655','2024-05-18 23:38:43.451561',19,'');
/*!40000 ALTER TABLE mistech_staff ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_student`
--

DROP TABLE IF EXISTS mistech_student;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_student (
  st_id int NOT NULL AUTO_INCREMENT,
  middle_name varchar(50) DEFAULT NULL,
  dob date NOT NULL,
  adrz varchar(255) DEFAULT NULL,
  gender varchar(10) NOT NULL,
  nic varchar(20) NOT NULL,
  st_idNo varchar(100) DEFAULT NULL,
  nationality varchar(50) DEFAULT NULL,
  mobileNo varchar(12) NOT NULL,
  resiNo varchar(10) DEFAULT NULL,
  civil_status varchar(10) DEFAULT NULL,
  edu_qualification varchar(10) DEFAULT NULL,
  prof_qualification varchar(10) DEFAULT NULL,
  other_qualification varchar(255) DEFAULT NULL,
  guardian_name varchar(100) DEFAULT NULL,
  guardian_contNo varchar(20) DEFAULT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  admin_id bigint NOT NULL,
  b_id_id int NOT NULL,
  c_id_id int NOT NULL,
  tr_id_id int NOT NULL,
  yr_id_id int NOT NULL,
  fcm_token longtext NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (st_id),
  UNIQUE KEY nic (nic),
  UNIQUE KEY admin_id (admin_id),
  UNIQUE KEY st_idNo (st_idNo),
  KEY mistech_student_b_id_id_61391db9_fk_mistech_batch_b_id (b_id_id),
  KEY mistech_student_c_id_id_9e2bbbff_fk_mistech_course_c_id (c_id_id),
  KEY mistech_student_tr_id_id_3d53899b_fk_mistech_trade_tr_id (tr_id_id),
  KEY mistech_student_yr_id_id_e6525eff_fk_mistech_sessionyr_yr_id (yr_id_id),
  CONSTRAINT mistech_student_admin_id_e9c8dc27_fk_mistech_customuser_id FOREIGN KEY (admin_id) REFERENCES mistech_customuser (id),
  CONSTRAINT mistech_student_b_id_id_61391db9_fk_mistech_batch_b_id FOREIGN KEY (b_id_id) REFERENCES mistech_batch (b_id),
  CONSTRAINT mistech_student_c_id_id_9e2bbbff_fk_mistech_course_c_id FOREIGN KEY (c_id_id) REFERENCES mistech_course (c_id),
  CONSTRAINT mistech_student_tr_id_id_3d53899b_fk_mistech_trade_tr_id FOREIGN KEY (tr_id_id) REFERENCES mistech_trade (tr_id),
  CONSTRAINT mistech_student_yr_id_id_e6525eff_fk_mistech_sessionyr_yr_id FOREIGN KEY (yr_id_id) REFERENCES mistech_sessionyr (yr_id)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_student`
--

LOCK TABLES mistech_student WRITE;
/*!40000 ALTER TABLE mistech_student DISABLE KEYS */;
INSERT INTO mistech_student VALUES (1,'Melani','2002-04-14','Trincomalee','F','200298909872','ST_Eng_01','UK','0763423898','0268790765','UM','AL','NVQ3','Following Certificate in IT','Berenjer','0268790765','2024-02-20 04:12:37.136464','2024-02-20 04:12:37.143292',5,3,2,2,3,''),(2,'Nishadhi','2002-12-22','Kiridiwela','F','200239878767','ST_IT_01','Sri Lankan','0771667608','0338976536','UM','AL','NVQ3','Following Certificate in English','Saumya','0338976536','2024-02-20 04:16:33.346985','2024-05-17 06:22:15.756581',6,1,1,1,1,''),(3,'Devitha','2002-07-04','Yakkala','M','200298767351','ST_IT_02','Sri Lankan','771667608','0339387343','UM','AL','NVQ3','Following Certificate in English','Indrawimala','0339387343','2024-02-20 04:20:30.539424','2024-03-02 13:24:52.307146',7,1,1,1,1,''),(4,'Nilanka','2002-06-21','Matale','F','200289345125','ST_IT_03','Sri Lankan','0765312876','0663898767','UM','AL','NVQ2','Following Certificate in English','Jayasundara','0663898767','2024-02-20 05:21:10.494376','2024-02-22 06:23:48.731935',8,4,1,1,1,''),(5,'Madhuwanthi','2002-09-30','Kurunagala','F','200290983909','ST_Eng_02','Sri Lankan','0778298190','0602987890','UM','AL','NVQ2','Following Certificate in IT','Wijesooriya','0602987890','2024-02-22 06:21:27.856387','2024-03-02 13:27:29.874604',9,3,2,2,3,''),(6,'Dushan','2002-10-12','Yakkala','M','200234587678','ST_REF_01','Sri Lankan','0771752273','0337876789','M','AL','NVQ3','Diploma in English','Dayani t','0337876789','2024-03-02 13:35:55.278176','2024-05-17 14:47:38.738264',12,2,3,3,1,''),(7,'sanjana','2002-12-03','Meerigama','M','200298789878','ST_IT_04','Sri Lankan','0771752275','0312878987','UM','AL','NVQ4','Completed Diploma in IT','Dismanthi','0312878987','2024-03-02 13:41:17.618003','2024-03-02 13:41:17.628173',13,4,1,1,1,''),(8,'De','2002-11-12','Colombo','F','200298765456','ST_IT_05','Sri Lankan','+967738891','0113456789','M','AL','Dip','Following PhD','Exr','0113456789','2024-03-29 19:29:16.433957','2024-05-17 14:22:25.967007',16,4,1,1,1,''),(9,'V','2002-12-10','Colombo','M','200212345678','ST_IT_06','Sri Lankan','+947773596','0119234567','M','AL','Dip','Following PhD','Etc','0119234567','2024-03-29 19:33:25.923636','2024-05-17 14:21:18.788760',17,4,1,1,1,''),(10,'KH','2002-01-01','Kaluthara','F','200098989889','ST_IT_07','Sri Lankan','0771667608','0115748944','UM','AL','NVQ4','Diploma in English','Thilakarathne','0115748944','2024-05-17 06:31:09.309790','2024-05-17 14:52:42.005951',18,1,1,1,1,''),(11,'ex','1999-05-29','Gampaha','M','199978765678','ST_Eng_03','Sri Lankan','0732567657','0332898876','UM','OL','NVQ5','Diploma in English','Etc','0332898876','2024-05-18 23:44:26.951856','2024-05-18 23:44:26.960659',20,3,2,2,1,'');
/*!40000 ALTER TABLE mistech_student ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_studentresult`
--

DROP TABLE IF EXISTS mistech_studentresult;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_studentresult (
  sr_id int NOT NULL AUTO_INCREMENT,
  sub_exam_marks double NOT NULL,
  sub_asgn_marks double NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  st_id_id int NOT NULL,
  sub_id_id int NOT NULL,
  PRIMARY KEY (sr_id),
  KEY mistech_studentresult_st_id_id_78f64e5c_fk_mistech_student_st_id (st_id_id),
  KEY mistech_studentresul_sub_id_id_a490da19_fk_mistech_s (sub_id_id),
  CONSTRAINT mistech_studentresul_sub_id_id_a490da19_fk_mistech_s FOREIGN KEY (sub_id_id) REFERENCES mistech_subject (sub_id),
  CONSTRAINT mistech_studentresult_st_id_id_78f64e5c_fk_mistech_student_st_id FOREIGN KEY (st_id_id) REFERENCES mistech_student (st_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_studentresult`
--

LOCK TABLES mistech_studentresult WRITE;
/*!40000 ALTER TABLE mistech_studentresult DISABLE KEYS */;
/*!40000 ALTER TABLE mistech_studentresult ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_subject`
--

DROP TABLE IF EXISTS mistech_subject;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_subject (
  sub_id int NOT NULL AUTO_INCREMENT,
  sub_code varchar(255) NOT NULL,
  sub_name varchar(255) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  c_id_id int NOT NULL,
  PRIMARY KEY (sub_id),
  UNIQUE KEY sub_code (sub_code),
  UNIQUE KEY sub_name (sub_name),
  KEY mistech_subject_c_id_id_17d68608_fk_mistech_course_c_id (c_id_id),
  CONSTRAINT mistech_subject_c_id_id_17d68608_fk_mistech_course_c_id FOREIGN KEY (c_id_id) REFERENCES mistech_course (c_id)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_subject`
--

LOCK TABLES mistech_subject WRITE;
/*!40000 ALTER TABLE mistech_subject DISABLE KEYS */;
INSERT INTO mistech_subject VALUES (1,'K72S004U01','Use the computer and manage files within standard operating systems','2024-02-19 09:16:29.021426','2024-02-19 09:16:29.021426',1),(2,'G50S024U01','Deal with customer for Automobile Air Conditioner repairing and / or servicing','2024-02-19 11:09:28.553466','2024-02-19 11:09:28.553466',3),(3,'K72S004U02','Perform word processing','2024-02-19 23:39:38.960540','2024-02-19 23:39:38.960540',1),(4,'K72S004U03','Prepare spreadsheets','2024-02-19 23:41:37.452183','2024-02-19 23:41:37.452183',1),(5,'G50S024U02','Prepare estimates','2024-02-19 23:42:11.437819','2024-02-19 23:42:11.437819',3),(6,'L001','Listening','2024-02-22 06:29:07.805793','2024-02-22 06:29:07.805793',2),(7,'K72S004U04','Prepare presentation resources','2024-03-18 18:59:50.350859','2024-03-18 18:59:50.350859',1),(8,'K72S004U05','Perform basic operations of cloud computing including internet and email services','2024-03-18 19:00:22.967872','2024-03-18 19:00:22.967872',1),(9,'K72S004U06','Handle relational database','2024-03-18 19:01:02.931857','2024-03-18 19:01:02.931857',1),(10,'K72S004U07','Conduct routine maintenance services of computer system and peripherals','2024-03-18 19:01:37.416619','2024-03-18 19:01:37.416619',1),(11,'K72S004U08','Produce print page layout and multimedia objects','2024-03-18 19:02:27.616039','2024-03-18 19:02:27.616039',1),(12,'K72S004U09','Analyze, design and develop information system','2024-03-18 19:03:01.216964','2024-03-18 19:03:01.216964',1),(13,'K72S004U10','Handle relational databases using standard SQL','2024-03-18 19:03:31.866281','2024-03-18 19:03:31.866281',1);
/*!40000 ALTER TABLE mistech_subject ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_subject_sf_id`
--

DROP TABLE IF EXISTS mistech_subject_sf_id;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_subject_sf_id (
  id bigint NOT NULL AUTO_INCREMENT,
  subject_id int NOT NULL,
  staff_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY mistech_subject_sf_id_subject_id_staff_id_0c5c9fe0_uniq (subject_id,staff_id),
  KEY mistech_subject_sf_id_staff_id_7dedf3de_fk_mistech_staff_sf_id (staff_id),
  CONSTRAINT mistech_subject_sf_i_subject_id_a16d265a_fk_mistech_s FOREIGN KEY (subject_id) REFERENCES mistech_subject (sub_id),
  CONSTRAINT mistech_subject_sf_id_staff_id_7dedf3de_fk_mistech_staff_sf_id FOREIGN KEY (staff_id) REFERENCES mistech_staff (sf_id)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_subject_sf_id`
--

LOCK TABLES mistech_subject_sf_id WRITE;
/*!40000 ALTER TABLE mistech_subject_sf_id DISABLE KEYS */;
INSERT INTO mistech_subject_sf_id VALUES (1,1,1),(2,1,2),(3,2,2),(4,3,1),(5,3,3),(6,4,3),(7,5,2),(8,6,4),(9,7,1),(10,7,3),(11,8,1),(12,9,3),(13,10,1),(14,11,1),(15,11,3),(16,12,3),(17,13,3);
/*!40000 ALTER TABLE mistech_subject_sf_id ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_task`
--

DROP TABLE IF EXISTS mistech_task;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_task (
  tk_id int NOT NULL AUTO_INCREMENT,
  tk_name varchar(255) NOT NULL,
  tk_date date NOT NULL,
  `status` varchar(15) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  mod_id_id int NOT NULL,
  sf_id_id bigint NOT NULL,
  tk_wk int unsigned NOT NULL,
  PRIMARY KEY (tk_id),
  UNIQUE KEY tk_name (tk_name),
  KEY mistech_task_mod_id_id_ae2058f9_fk_mistech_module_mod_id (mod_id_id),
  KEY mistech_task_sf_id_id_6c701bfb_fk_mistech_customuser_id (sf_id_id),
  CONSTRAINT mistech_task_mod_id_id_ae2058f9_fk_mistech_module_mod_id FOREIGN KEY (mod_id_id) REFERENCES mistech_module (mod_id),
  CONSTRAINT mistech_task_sf_id_id_6c701bfb_fk_mistech_customuser_id FOREIGN KEY (sf_id_id) REFERENCES mistech_customuser (id),
  CONSTRAINT mistech_task_chk_1 CHECK ((`tk_wk` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_task`
--

LOCK TABLES mistech_task WRITE;
/*!40000 ALTER TABLE mistech_task DISABLE KEYS */;
INSERT INTO mistech_task VALUES (1,'Start up and turn off the computer','2023-11-30','completed','2024-03-19 07:50:31.377994','2024-03-19 07:50:31.377994',1,4,1),(2,'Customize computer and desktop settings','2023-12-07','completed','2024-03-19 17:15:04.147392','2024-03-19 17:15:04.147392',1,4,2),(3,'Create folders and files','2023-12-11','completed','2024-03-21 09:43:28.453784','2024-03-21 09:43:28.453784',1,4,2),(4,'Perform Folder/File operations','2023-12-12','completed','2024-03-21 09:45:09.520795','2024-03-21 09:45:09.520795',1,4,2),(5,'Set attributes of files folders','2023-12-13','not_completed','2024-03-21 09:45:35.589284','2024-03-21 09:45:35.589284',1,4,2),(9,'task 1','2024-01-08','complete','2024-05-18 23:59:33.175975','2024-05-18 23:59:33.175975',1,2,1),(10,'task2','2024-03-02','not_complete','2024-05-19 00:00:08.390518','2024-05-19 00:00:08.390518',2,2,2),(11,'task3','2024-05-09','complete','2024-05-19 07:48:53.892161','2024-05-19 07:48:53.892161',2,2,2);
/*!40000 ALTER TABLE mistech_task ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mistech_trade`
--

DROP TABLE IF EXISTS mistech_trade;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE mistech_trade (
  tr_id int NOT NULL AUTO_INCREMENT,
  tr_name varchar(255) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  PRIMARY KEY (tr_id),
  UNIQUE KEY tr_name (tr_name)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mistech_trade`
--

LOCK TABLES mistech_trade WRITE;
/*!40000 ALTER TABLE mistech_trade DISABLE KEYS */;
INSERT INTO mistech_trade VALUES (1,'Information Communication &  Technolog','2024-02-18 16:13:06.132426','2024-03-07 03:47:04.051615'),(2,'Languages','2024-02-18 17:35:19.231758','2024-02-18 17:35:19.231758'),(3,'Refrigeration & Air Conditioning','2024-02-18 17:35:30.366900','2024-02-18 17:35:30.366900'),(4,'Building & Construction','2024-02-18 17:35:45.348461','2024-02-18 17:35:45.348461'),(5,'Electrical,Electronics & Telecommunication','2024-05-18 23:47:17.156735','2024-05-18 23:47:17.156735');
/*!40000 ALTER TABLE mistech_trade ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-30 20:50:02
