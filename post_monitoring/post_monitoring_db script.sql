CREATE SCHEMA `post_monitoring_db` ;

CREATE TABLE `post_monitoring_db`.`current_patient_logs`(
  `bed_number` INT NULL,
  `timestamp_start` DATETIME NULL,
  `timestamp_end` DATETIME NULL,
  `accompanied` INT NULL,
  `hfr_count` INT NULL);


CREATE TABLE `post_monitoring_db`.`discharged_patient_logs` (
  `bed_number` INT NULL,
  `timestamp_start` DATETIME NULL,
  `timestamp_end` DATETIME NULL,
  `accompanied` INT NULL,
  `hfr_count` INT NULL,
  `date_first` DATE NULL,
  `date_last` DATE NULL);