#!/usr/bin/env python
"""
Script to set up PostgreSQL database for production.
Run this script to create the database and user for your Django app.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create PostgreSQL database and user for the Django app."""
    
    # Database configuration
    db_name = os.environ.get('DB_NAME', 'social_media_api')
    db_user = os.environ.get('DB_USER', 'social_media_user')
    db_password = os.environ.get('DB_PASSWORD', 'your_password_here')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    
    # Connect to PostgreSQL server
    try:
        # Connect as superuser to create database and user
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user='postgres',  # Default superuser
            password=os.environ.get('POSTGRES_PASSWORD', ''),
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create user
        try:
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}';")
            print(f"User '{db_user}' created successfully.")
        except psycopg2.errors.DuplicateObject:
            print(f"User '{db_user}' already exists.")
        
        # Create database
        try:
            cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
            print(f"Database '{db_name}' created successfully.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{db_name}' already exists.")
        
        # Grant privileges
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
        cursor.execute(f"ALTER USER {db_user} CREATEDB;")
        
        cursor.close()
        conn.close()
        
        print("Database setup completed successfully!")
        
    except psycopg2.Error as e:
        print(f"Error setting up database: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_database()