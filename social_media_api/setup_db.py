#!/usr/bin/env python
"""
Database setup script for the Social Media API.
This script helps set up the database and apply migrations.
"""
import os
import sys
import subprocess

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def setup_database():
    """Set up the database and apply migrations."""
    print("Setting up the database...")
    
    # Install required packages
    print("Installing required packages...")
    run_command("pip install -r requirements.txt")
    
    # Apply migrations
    print("\nApplying migrations...")
    run_command("python manage.py migrate")
    
    # Create a superuser if it doesn't exist
    print("\nCreating a superuser...")
    try:
        run_command("python manage.py createsuperuser --noinput --username admin --email admin@example.com")
        print("Superuser created with username 'admin' and email 'admin@example.com'")
        print("Please set a password using: python manage.py changepassword admin")
    except:
        print("Superuser already exists or could not be created.")
    
    # Load initial data (if any)
    # Uncomment the following line if you have fixtures to load
    # run_command("python manage.py loaddata initial_data.json")
    
    print("\nDatabase setup complete!")

if __name__ == "__main__":
    setup_database()
