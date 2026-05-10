-- Hotel Management System — MySQL 8.x DDL (CSC380-style schema from project doc)
-- Run after: CREATE DATABASE hotel_management; USE hotel_management;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS invoice;
DROP TABLE IF EXISTS reservation_room;
DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS guest;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS hotel;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE hotel (
    hotel_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    address VARCHAR(300) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone VARCHAR(40) NOT NULL,
    PRIMARY KEY (hotel_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE room (
    room_id INT NOT NULL AUTO_INCREMENT,
    room_number VARCHAR(50) NOT NULL,
    floor INT NOT NULL,
    room_type ENUM('Single', 'Double', 'Suite') NOT NULL DEFAULT 'Single',
    price_per_night DECIMAL(10, 2) NOT NULL,
    max_capacity INT NOT NULL,
    status ENUM('Available', 'Occupied', 'Maintenance') NOT NULL DEFAULT 'Available',
    hotel_id INT NOT NULL,
    PRIMARY KEY (room_id),
    UNIQUE KEY uk_hotel_room_number (hotel_id, room_number),
    CONSTRAINT fk_room_hotel FOREIGN KEY (hotel_id) REFERENCES hotel (hotel_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_room_floor CHECK (floor >= 0),
    CONSTRAINT chk_room_capacity CHECK (max_capacity >= 1),
    CONSTRAINT chk_room_price CHECK (price_per_night >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE guest (
    guest_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(40) NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    PRIMARY KEY (guest_id),
    UNIQUE KEY uk_guest_email (email),
    UNIQUE KEY uk_guest_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE reservation (
    reservation_id INT NOT NULL AUTO_INCREMENT,
    booking_date DATE NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    status ENUM('confirmed', 'checked-in', 'checked-out', 'cancelled') NOT NULL DEFAULT 'confirmed',
    guest_id INT NOT NULL,
    PRIMARY KEY (reservation_id),
    CONSTRAINT fk_reservation_guest FOREIGN KEY (guest_id) REFERENCES guest (guest_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_reservation_dates CHECK (check_in_date <= check_out_date),
    CONSTRAINT chk_booking_vs_checkin CHECK (booking_date <= check_in_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE reservation_room (
    reservation_id INT NOT NULL,
    room_id INT NOT NULL,
    price_at_booking DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (reservation_id, room_id),
    CONSTRAINT fk_rr_reservation FOREIGN KEY (reservation_id) REFERENCES reservation (reservation_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_rr_room FOREIGN KEY (room_id) REFERENCES room (room_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_rr_price CHECK (price_at_booking >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE invoice (
    invoice_id INT NOT NULL AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    PRIMARY KEY (invoice_id),
    UNIQUE KEY uk_invoice_reservation (reservation_id),
    CONSTRAINT fk_invoice_reservation FOREIGN KEY (reservation_id) REFERENCES reservation (reservation_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_invoice_total CHECK (total_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE employee (
    employee_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    salary DECIMAL(12, 2) NOT NULL,
    hire_date DATE NOT NULL,
    hotel_id INT NOT NULL,
    PRIMARY KEY (employee_id),
    CONSTRAINT fk_employee_hotel FOREIGN KEY (hotel_id) REFERENCES hotel (hotel_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_employee_salary CHECK (salary >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Optional demo seed (uncomment if desired)
/*
INSERT INTO hotel (name, address, city, phone) VALUES
    ('Grand Plaza', '1 Main St', 'Riyadh', '+966500000001');
INSERT INTO room (room_number, floor, room_type, price_per_night, max_capacity, status, hotel_id) VALUES
    ('101', 1, 'Single', 199.99, 1, 'Available', 1),
    ('102', 1, 'Double', 299.99, 2, 'Available', 1);
INSERT INTO guest (first_name, last_name, email, phone, nationality) VALUES
    ('Ada', 'Lovelace', 'ada@example.com', '+966500000002', 'UK');
*/
