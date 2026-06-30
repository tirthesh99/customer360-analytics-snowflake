/*==============================================================
Project : Customer 360 Analytics Platform using Snowflake
File    : 01_Create_Database.sql
Author  : Tirthesh Kode
Purpose : Create the project database and set it as the active database.
Date    : 2026-06-25
==============================================================*/

-- Create project database
CREATE OR REPLACE DATABASE CUSTOMER360_DB;

-- Set active database
USE DATABASE CUSTOMER360_DB;

-- Verify active database
SELECT CURRENT_DATABASE();