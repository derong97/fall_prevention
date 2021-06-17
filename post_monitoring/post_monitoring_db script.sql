CREATE SCHEMA `post_monitoring_db` ;

CREATE TABLE `post_monitoring_db`.`current_patient_logs`(
  `bed_number` INT NULL,
  `timestamp_start` TIMESTAMP NULL,
  `timestamp_end`  TIMESTAMP NULL,
  `accompanied` INT NULL,
  `hfr_count` INT NULL);


CREATE TABLE `post_monitoring_db`.`discharged_patient_logs` (
  `bed_number` INT NULL,
  `timestamp_start` TIMESTAMP NULL,
  `timestamp_end`  TIMESTAMP NULL,
  `accompanied` INT NULL,
  `hfr_count` INT NULL,
  `date_first` TIMESTAMP NULL,
  `date_last` TIMESTAMP NULL);