#!/usr/bin/env python
"""
Deployment preparation script for Django Social Media API
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"📋 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main deployment preparation function"""
    print("🚀 Django Social Media API - Deployment Preparation")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Set production environment
    os.environ['DEBUG'] = 'False'
    
    # Commands to run
    commands = [
        ("python manage.py check", "Running Django system checks"),
        ("python manage.py check --deploy", "Running deployment-specific checks"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
        ("python manage.py showmigrations", "Checking migration status"),
    ]
    
    success_count = 0
    total_commands = len(commands)
    
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"\n⚠️  Warning: {description} failed")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 DEPLOYMENT PREPARATION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {success_count}/{total_commands}")
    print(f"❌ Failed: {total_commands - success_count}/{total_commands}")
    
    if success_count == total_commands:
        print("\n🎉 All checks passed! Your application is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Set environment variables on your hosting platform")
        print("2. Push your code to your repository")
        print("3. Deploy using your chosen hosting service")
        print("4. Run migrations on production: python manage.py migrate")
    else:
        print("\n⚠️  Some checks failed. Please review the errors above before deploying.")
    
    print(f"\n📚 For detailed deployment instructions, see: DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
