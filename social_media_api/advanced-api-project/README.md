# Advanced Django REST Framework API

A RESTful API built with Django REST Framework that provides endpoints for managing authors and books with authentication, filtering, searching, and pagination.

## Features

- **Token-based Authentication**: Secure API endpoints with JWT authentication
- **CRUD Operations**: Full support for creating, reading, updating, and deleting authors and books
- **Filtering & Searching**: Filter books by author, publication year, and search by title or author name
- **Pagination**: Results are paginated for better performance
- **Comprehensive Tests**: Complete test coverage for all endpoints and features

## Prerequisites

- Python 3.8+
- Django 4.0+
- Django REST Framework 3.12+
- Django Filter

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd advanced-api-project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- **POST** `/api/token/` - Obtain authentication token
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

### Authors

- **GET** `/api/authors/` - List all authors
- **POST** `/api/authors/` - Create a new author (requires authentication)
- **GET** `/api/authors/{id}/` - Get author details
- **PUT** `/api/authors/{id}/` - Update author (requires authentication)
- **PATCH** `/api/authors/{id}/` - Partially update author (requires authentication)
- **DELETE** `/api/authors/{id}/` - Delete author (requires authentication)

### Books

- **GET** `/api/books/` - List all books
  - Query Parameters:
    - `author` or `author__id`: Filter by author ID
    - `author_name`: Filter by author name (contains, case-insensitive)
    - `min_year`, `max_year`: Filter by publication year range
    - `search`: Search in title or author name
    - `ordering`: Sort by field (e.g., `title`, `-publication_year`)
- **POST** `/api/books/` - Create a new book (requires authentication)
- **GET** `/api/books/{id}/` - Get book details
- **PUT** `/api/books/{id}/` - Update book (requires authentication)
- **PATCH** `/api/books/{id}/` - Partially update book (requires authentication)
- **DELETE** `/api/books/{id}/` - Delete book (requires authentication)

## Testing

Run the test suite with:

```bash
python manage.py test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
