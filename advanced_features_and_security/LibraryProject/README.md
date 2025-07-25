# LibraryProject

A Django-based library management system demonstrating advanced features and security best practices.

## Features
- **Custom User Model**: Extends Django's `AbstractUser` with additional fields (`date_of_birth`, `profile_photo`).
- **Role-Based Access Control**: Uses Django groups and custom permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) for the `Book` model.
- **Permissions & Groups**: Editors, Viewers, and Admins groups with granular access control.
- **CRUD for Books**: Views are protected by custom permissions.
- **Profile Management**: UserProfile model for role assignment and extra user data.

## Setup
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the server**
   ```bash
   python manage.py runserver
   ```

## Permissions & Groups Usage
- See `PERMISSIONS.md` for details on setting up groups and permissions via Django admin.
- Assign users to groups (Editors, Viewers, Admins) for access control.

## Directory Structure
```
LibraryProject/
├── LibraryProject/         # Django project core (settings, urls, wsgi, asgi)
├── bookshelf/             # App with Book model and custom user
├── relationship_app/      # App with UserProfile and library relationships
├── manage.py
├── README.md
└── PERMISSIONS.md
```

## Notes
- All sensitive settings (e.g., secrets) should be managed securely.
- Code follows TDD, clean code, and security best practices as per project guidelines.

---
For more details, see code comments and the `PERMISSIONS.md` file.
