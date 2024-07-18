#!/bin/bash

# Database and user details
DB_NAME='tech_for_all'
DB_USER='user_tech_care_for_all'
DB_PASS='12345678'

# Drop the database if it exists
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"

# Drop the user if it exists
sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"

# Create the user with superuser privileges and the specified password
sudo -u postgres psql -c "CREATE USER $DB_USER WITH SUPERUSER PASSWORD '$DB_PASS';"

# Create the database with the specified user as the owner
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER;"

# Additional SQL commands to set user properties and privileges
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Database and user recreated successfully!"