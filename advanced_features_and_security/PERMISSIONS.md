# Django Permissions & Groups Setup Guide

## Custom Permissions on Book Model
- Added in `bookshelf/models.py`:
  - `can_view`: Can view book
  - `can_create`: Can create book
  - `can_edit`: Can edit book
  - `can_delete`: Can delete book

## Groups to Create (via Django Admin)
- **Editors**: can_view, can_create, can_edit
- **Viewers**: can_view
- **Admins**: can_view, can_create, can_edit, can_delete

## How to Assign Permissions to Groups
1. Go to Django admin (`/admin`).
2. Navigate to **Groups**.
3. Create groups: Editors, Viewers, Admins.
4. Assign the above permissions to each group by editing the group and selecting the permissions for the Book model.
5. Assign users to groups as needed.

## Permission Enforcement in Views
- All book views in `bookshelf/views.py` require the appropriate permission:
  - List: `@permission_required('bookshelf.can_view', raise_exception=True)`
  - Create: `@permission_required('bookshelf.can_create', raise_exception=True)`
  - Edit: `@permission_required('bookshelf.can_edit', raise_exception=True)`
  - Delete: `@permission_required('bookshelf.can_delete', raise_exception=True)`

## Testing Permissions
- Assign users to groups in admin.
- Log in as different users and try to access book views to confirm permissions are enforced.

## Notes
- Permissions and groups are managed via Django admin for flexibility.
- You can also script group/permission setup with a management command if desired.
