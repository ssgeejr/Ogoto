-- Initialize Ogoto KEV MySQL schema

-- Set or create the database
CREATE DATABASE IF NOT EXISTS ogoto;
USE ogoto;

-- Create the KEV catalog table with selected fields only
CREATE TABLE IF NOT EXISTS kev_catalog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cve_id VARCHAR(32) NOT NULL,
    vendor_project VARCHAR(255),
    product VARCHAR(255),
    vulnerability_name TEXT,
    date_added DATE,
    short_description TEXT,
    notes TEXT,
    UNIQUE KEY unique_cve (cve_id)
);
