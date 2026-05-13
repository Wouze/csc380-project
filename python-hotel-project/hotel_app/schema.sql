-- Modified MySQL Workbench Forward Engineering for Hotel Management

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Drop existing tables to allow safe recreation
DROP TABLE IF EXISTS reservation_room;
DROP TABLE IF EXISTS invoice;
DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS guest;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS hotel;


-- -----------------------------------------------------
-- Table hotel
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS hotel (
  hotel_id INT(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NULL DEFAULT NULL,
  address VARCHAR(255) NULL DEFAULT NULL,
  city VARCHAR(100) NULL DEFAULT NULL,
  phone VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (hotel_id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table employee
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS employee (
  employee_id INT(11) NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(100) NULL DEFAULT NULL,
  last_name VARCHAR(100) NULL DEFAULT NULL,
  role VARCHAR(100) NULL DEFAULT NULL,
  salary DECIMAL(10,2) NULL DEFAULT NULL,
  hire_date DATE NULL DEFAULT NULL,
  hotel_id INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (employee_id),
  INDEX hotel_id (hotel_id ASC),
  CONSTRAINT employee_ibfk_1
    FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table guest
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS guest (
  guest_id INT(11) NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(100) NULL DEFAULT NULL,
  last_name VARCHAR(100) NULL DEFAULT NULL,
  email VARCHAR(255) NULL DEFAULT NULL,
  phone VARCHAR(20) NULL DEFAULT NULL,
  nationality VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (guest_id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table reservation
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS reservation (
  reservation_id INT(11) NOT NULL AUTO_INCREMENT,
  booking_date DATE NULL DEFAULT NULL,
  check_in_date DATE NULL DEFAULT NULL,
  check_out_date DATE NULL DEFAULT NULL,
  status VARCHAR(50) NULL DEFAULT NULL,
  guest_id INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (reservation_id),
  INDEX guest_id (guest_id ASC),
  CONSTRAINT reservation_ibfk_1
    FOREIGN KEY (guest_id)
    REFERENCES guest (guest_id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table invoice
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS invoice (
  invoice_id INT(11) NOT NULL AUTO_INCREMENT,
  reservation_id INT(11) NULL DEFAULT NULL,
  total_amount DECIMAL(10,2) NULL DEFAULT NULL,
  payment_method VARCHAR(50) NULL DEFAULT NULL,
  payment_status VARCHAR(50) NULL DEFAULT NULL,
  issue_date DATE NULL DEFAULT NULL,
  PRIMARY KEY (invoice_id),
  INDEX reservation_id (reservation_id ASC),
  CONSTRAINT invoice_ibfk_1
    FOREIGN KEY (reservation_id)
    REFERENCES reservation (reservation_id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table room
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS room (
  room_id INT(11) NOT NULL AUTO_INCREMENT,
  room_number VARCHAR(20) NULL DEFAULT NULL,
  floor INT(11) NULL DEFAULT NULL,
  room_type VARCHAR(50) NULL DEFAULT NULL,
  price_per_night DECIMAL(10,2) NULL DEFAULT NULL,
  max_capacity INT(11) NULL DEFAULT NULL,
  status VARCHAR(50) NULL DEFAULT NULL,
  hotel_id INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (room_id),
  INDEX hotel_id (hotel_id ASC),
  CONSTRAINT room_ibfk_1
    FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table reservation_room
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS reservation_room (
  reservation_id INT(11) NOT NULL,
  room_id INT(11) NOT NULL,
  PRIMARY KEY (reservation_id, room_id),
  INDEX room_id (room_id ASC),
  CONSTRAINT reservation_room_ibfk_1
    FOREIGN KEY (reservation_id)
    REFERENCES reservation (reservation_id),
  CONSTRAINT reservation_room_ibfk_2
    FOREIGN KEY (room_id)
    REFERENCES room (room_id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
