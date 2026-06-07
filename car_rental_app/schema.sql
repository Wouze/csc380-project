SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `car_rental` DEFAULT CHARACTER SET utf8mb4;
USE `car_rental`;

CREATE TABLE IF NOT EXISTS `car_rental`.`branch` (
  `branch_id` INT(11) NOT NULL,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(100) NULL DEFAULT NULL,
  `phone` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`branch_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `car_rental`.`customer` (
  `customer_id` INT(11) NOT NULL,
  `first_name` VARCHAR(100) NULL DEFAULT NULL,
  `last_name` VARCHAR(100) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `phone` VARCHAR(20) NULL DEFAULT NULL,
  `nationality` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `car_rental`.`car` (
  `car_id` INT(11) NOT NULL,
  `license_plate` VARCHAR(20) NULL DEFAULT NULL,
  `model_year` INT(11) NULL DEFAULT NULL,
  `car_type` VARCHAR(50) NULL DEFAULT NULL,
  `daily_rate` DECIMAL(10,2) NULL DEFAULT NULL,
  `seats` INT(11) NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `branch_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`car_id`),
  INDEX `branch_id` (`branch_id` ASC),
  CONSTRAINT `car_ibfk_1`
    FOREIGN KEY (`branch_id`)
    REFERENCES `car_rental`.`branch` (`branch_id`)
    ON DELETE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `car_rental`.`rental` (
  `rental_id` INT(11) NOT NULL,
  `booking_date` DATE NULL DEFAULT NULL,
  `pick_up_date` DATE NULL DEFAULT NULL,
  `return_date` DATE NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `customer_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`rental_id`),
  INDEX `customer_id` (`customer_id` ASC),
  CONSTRAINT `rental_ibfk_1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `car_rental`.`customer` (`customer_id`)
    ON DELETE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `car_rental`.`payment` (
  `payment_id` INT(11) NOT NULL,
  `rental_id` INT(11) NULL DEFAULT NULL,
  `total_amount` DECIMAL(10,2) NULL DEFAULT NULL,
  `payment_method` VARCHAR(50) NULL DEFAULT NULL,
  `payment_status` VARCHAR(50) NULL DEFAULT NULL,
  `issue_date` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `rental_id` (`rental_id` ASC),
  CONSTRAINT `payment_ibfk_1`
    FOREIGN KEY (`rental_id`)
    REFERENCES `car_rental`.`rental` (`rental_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `car_rental`.`rental_car` (
  `rental_id` INT(11) NOT NULL,
  `car_id` INT(11) NOT NULL,
  PRIMARY KEY (`rental_id`, `car_id`),
  INDEX `car_id` (`car_id` ASC),
  CONSTRAINT `rental_car_ibfk_1`
    FOREIGN KEY (`rental_id`)
    REFERENCES `car_rental`.`rental` (`rental_id`)
    ON DELETE CASCADE,
  CONSTRAINT `rental_car_ibfk_2`
    FOREIGN KEY (`car_id`)
    REFERENCES `car_rental`.`car` (`car_id`)
    ON DELETE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
