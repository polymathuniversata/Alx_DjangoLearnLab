# Permissions and Groups Setup Guide

## Custom Permissions
- Defined in `Book` model (`bookshelf/models.py`):
  - `can_view`: Can view book
  - `can_create`: Can create book
  - `can_edit`: Can edit book
  - `can_delete`: Can delete book

## Groups
- Create groups in Django admin:
  - **Viewers**: Assign `can_view`
  - **Editors**: Assign `can_view`, `can_create`, `can_edit`
  - **Admins**: Assign all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`)

## Views
- All book-related views in `bookshelf/views.py` are protected with `@permission_required` decorators for the above permissions.
- Example: Only users with `can_edit` can access the edit view.

## How to Test
1. Create users and assign them to groups via Django admin.
2. Log in as each user and try to access book list, create, edit, and delete views.
3. Access will be granted or denied based on group permissions.

## Notes
- Permissions are enforced using Django's built-in decorators.
- Update group permissions in admin as needed for your use case.
