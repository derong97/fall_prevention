CREATE SCHEMA `post_monitoring_db` ;

CREATE TABLE `post_monitoring_db`.`current_patient_logs`(
  `bed_number` INT NULL,
  `date` VARCHAR(16) NULL,
  `time_start` VARCHAR(16) NULL,
  `time_end` VARCHAR(16) NULL,
  `accompanied` INT NULL,
  `hfr_count` BIGINT NULL);


CREATE TABLE `post_monitoring_db`.`discharged_patient_logs` (
  `bed_number` INT NULL,
  `date` VARCHAR(16) NULL,
  `time_start` VARCHAR(16) NULL,
  `time_end` VARCHAR(16) NULL,
  `accompanied` INT NULL,
  `hfr_count` BIGINT NULL,
  `date_first` VARCHAR(16) NULL,
  `date_last` VARCHAR(16) NULL);