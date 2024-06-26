-- Switch to or create the database if it doesn't exist
USE arcgis_urls_db;
CREATE DATABASE IF NOT EXISTS arcgis_urls_db;

-- Ensure the table arcgis_urls exists with appropriate structure
CREATE TABLE IF NOT EXISTS arcgis_urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(1024) NOT NULL  -- Adjusted to VARCHAR(1024) to handle longer URLs
);

-- Check for duplicates in the current arcgis_urls table
SELECT url, COUNT(*) AS count
FROM arcgis_urls
GROUP BY url
HAVING count > 1;

-- Create a temporary table to hold unique URLs
CREATE TABLE temp_arcgis_urls AS
SELECT MIN(id) AS id, url
FROM arcgis_urls
GROUP BY url;

-- Drop the original arcgis_urls table to remove duplicates
DROP TABLE arcgis_urls;

-- Rename the temporary table to the original table name
ALTER TABLE temp_arcgis_urls RENAME TO arcgis_urls;

-- Verify that duplicates have been successfully removed
SELECT * FROM arcgis_urls;

-- Check again for any remaining duplicates
SELECT url, COUNT(*) AS count
FROM arcgis_urls
GROUP BY url
HAVING count > 1;
