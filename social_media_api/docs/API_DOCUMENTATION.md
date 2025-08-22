# Social Media API Documentation

## Overview
This is a comprehensive Social Media API built with Django and Django REST Framework. The API provides functionality for user authentication, posts management, comments system, user following relationships, and personalized content feeds.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Posts Endpoints

### List Posts
- **URL:** `/api/posts/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Retrieve a paginated list of all posts

**Query Parameters:**
- `page` (int): Page number for pagination
- `page_size` (int): Number of items per page (default: 10)
- `search` (string): Search posts by title or content
- `author` (int): Filter posts by author ID
- `ordering` (string): Order by field (options: `created_at`, `-created_at`, `updated_at`, `-updated_at`, `title`, `-title`)

**Example Request:**
```bash
GET /api/posts/?search=django&page=1&page_size=5
```

**Example Response:**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Getting Started with Django",
            "content": "Django is a powerful web framework...",
            "author": {
                "id": 1,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe"
            },
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "comment_count": 5,
            "likes_count": 12,
            "is_liked": false
        }
    ]
}
```

### Create Post
- **URL:** `/api/posts/`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Create a new post

**Request Body:**
```json
{
    "title": "My New Post",
    "content": "This is the content of my new post..."
}
```

**Example Response:**
```json
{
    "id": 26,
    "title": "My New Post",
    "content": "This is the content of my new post...",
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe"
    },
    "created_at": "2024-01-15T15:45:00Z",
    "updated_at": "2024-01-15T15:45:00Z",
    "comment_count": 0,
    "likes_count": 0,
    "is_liked": false,
    "comments": []
}
```

### Retrieve Post
- **URL:** `/api/posts/{id}/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Retrieve a specific post with all its comments

**Example Response:**
```json
{
    "id": 1,
    "title": "Getting Started with Django",
    "content": "Django is a powerful web framework...",
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "comment_count": 2,
    "likes_count": 8,
    "is_liked": true,
    "comments": [
        {
            "id": 1,
            "author": {
                "id": 2,
                "username": "jane_smith",
                "first_name": "Jane",
                "last_name": "Smith"
            },
            "content": "Great post! Very helpful.",
            "created_at": "2024-01-15T11:00:00Z",
            "updated_at": "2024-01-15T11:00:00Z"
        }
    ]
}
```

### Update Post
- **URL:** `/api/posts/{id}/`
- **Method:** `PATCH` or `PUT`
- **Authentication:** Required
- **Permissions:** Only the author can update their post
- **Description:** Update a post

**Request Body (PATCH):**
```json
{
    "title": "Updated Title"
}
```

### Delete Post
- **URL:** `/api/posts/{id}/`
- **Method:** `DELETE`
- **Authentication:** Required
- **Permissions:** Only the author can delete their post
- **Description:** Delete a post

**Response:** `204 No Content`

### My Posts
- **URL:** `/api/posts/my_posts/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Get posts created by the current user

### Post Comments
- **URL:** `/api/posts/{id}/comments/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Get all comments for a specific post

### Like Post
- **URL:** `/api/posts/{id}/like/`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Like a specific post

**Path Parameters:**
- `id` (int): ID of the post to like

**Example Request:**
```bash
POST /api/posts/1/like/
```

**Example Response (Success):**
```json
{
    "message": "Post liked successfully"
}
```

**Error Responses:**
- `400 Bad Request`: If you have already liked this post
```json
{
    "message": "You have already liked this post"
}
```

### Unlike Post
- **URL:** `/api/posts/{id}/unlike/`
- **Method:** `DELETE`
- **Authentication:** Required
- **Description:** Remove like from a specific post

**Path Parameters:**
- `id` (int): ID of the post to unlike

**Example Request:**
```bash
DELETE /api/posts/1/unlike/
```

**Example Response (Success):**
```json
{
    "message": "Post unliked successfully"
}
```

**Error Responses:**
- `400 Bad Request`: If you have not liked this post
```json
{
    "message": "You have not liked this post"
}
```

## Comments Endpoints

### List Comments
- **URL:** `/api/comments/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Retrieve a paginated list of comments

**Query Parameters:**
- `post` (int): Filter comments by post ID
- `author` (int): Filter comments by author ID
- `search` (string): Search comments by content
- `ordering` (string): Order by field (options: `created_at`, `-created_at`, `updated_at`, `-updated_at`)

**Example Response:**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/comments/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "post": 1,
            "author": {
                "id": 2,
                "username": "jane_smith",
                "first_name": "Jane",
                "last_name": "Smith"
            },
            "content": "Great post! Very helpful.",
            "created_at": "2024-01-15T11:00:00Z",
            "updated_at": "2024-01-15T11:00:00Z"
        }
    ]
}
```

### Create Comment
- **URL:** `/api/comments/`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Create a comment on a post

**Request Body:**
```json
{
    "post": 1,
    "content": "This is my comment on the post"
}
```

### Update Comment
- **URL:** `/api/comments/{id}/`
- **Method:** `PATCH` or `PUT`
- **Authentication:** Required
- **Permissions:** Only the author can update their comment
- **Description:** Update a comment

### Delete Comment
- **URL:** `/api/comments/{id}/`
- **Method:** `DELETE`
- **Authentication:** Required
- **Permissions:** Only the author can delete their comment
- **Description:** Delete a comment

### My Comments
- **URL:** `/api/comments/my_comments/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Get comments created by the current user

## User Following Endpoints

### Follow User
- **URL:** `/api/auth/follow/{user_id}/`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Follow a specific user by their ID

**Path Parameters:**
- `user_id` (int): ID of the user to follow

**Example Request:**
```bash
POST /api/auth/follow/5/
```

**Example Response (Success):**
```json
{
    "status": "followed",
    "detail": "You are now following username123"
}
```

**Error Responses:**
- `400 Bad Request`: If trying to follow yourself or already following the user
- `404 Not Found`: If the user doesn't exist

### Unfollow User
- **URL:** `/api/auth/unfollow/{user_id}/`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Unfollow a specific user by their ID

**Path Parameters:**
- `user_id` (int): ID of the user to unfollow

**Example Request:**
```bash
POST /api/auth/unfollow/5/
```

**Example Response (Success):**
```json
{
    "status": "unfollowed", 
    "detail": "You have unfollowed username123"
}
```

**Error Responses:**
- `400 Bad Request`: If trying to unfollow yourself or not currently following the user
- `404 Not Found`: If the user doesn't exist

## Feed Endpoints

### Get Feed
- **URL:** `/api/feed/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Retrieve posts from users that the current user follows, ordered by creation date (most recent first)

**Query Parameters:**
- `page` (int): Page number for pagination
- `page_size` (int): Number of items per page (default: 10)
- `ordering` (string): Order by field (default: `-created_at`)

**Example Request:**
```bash
GET /api/feed/?page=1&page_size=10
```

**Example Response:**
```json
{
    "count": 25,
    "results": [
        {
            "id": 15,
            "title": "Latest Update from User I Follow",
            "content": "This is a post from someone I follow...",
            "author": {
                "id": 5,
                "username": "followed_user",
                "first_name": "Followed",
                "last_name": "User"
            },
            "created_at": "2024-01-15T16:30:00Z",
            "updated_at": "2024-01-15T16:30:00Z",
            "comment_count": 3
        },
        {
            "id": 12,
            "title": "Another Post from Feed",
            "content": "This is another post from my feed...",
            "author": {
                "id": 7,
                "username": "another_user",
                "first_name": "Another",
                "last_name": "User"
            },
            "created_at": "2024-01-15T15:20:00Z",
            "updated_at": "2024-01-15T15:20:00Z",
            "comment_count": 1
        }
    ]
}
```

**Notes:**
- Only posts from users you follow are included
- Your own posts are not included in the feed
- If you're not following anyone, the feed will be empty
- Posts are ordered by creation date (newest first)

## Notifications Endpoints

### List Notifications
- **URL:** `/api/notifications/`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Retrieve all notifications for the current user

**Query Parameters:**
- `page` (int): Page number for pagination
- `page_size` (int): Number of items per page (default: 10)

**Example Request:**
```bash
GET /api/notifications/
```

**Example Response:**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/notifications/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "actor": {
                "id": 5,
                "username": "jane_doe",
                "profile_picture": null
            },
            "verb": "liked your post",
            "target_url": "/api/posts/3/",
            "timestamp": "2024-01-15T14:30:00Z",
            "time_since": "2 hours ago",
            "read": false
        },
        {
            "id": 2,
            "actor": {
                "id": 7,
                "username": "john_smith",
                "profile_picture": null
            },
            "verb": "started following you",
            "target_url": "/api/users/john_smith/",
            "timestamp": "2024-01-15T12:15:00Z",
            "time_since": "4 hours ago",
            "read": false
        },
        {
            "id": 3,
            "actor": {
                "id": 8,
                "username": "alice_brown",
                "profile_picture": null
            },
            "verb": "commented on your post",
            "target_url": "/api/posts/2/comments/15/",
            "timestamp": "2024-01-15T11:45:00Z",
            "time_since": "5 hours ago",
            "read": true
        }
    ]
}
```

**Notes:**
- Notifications are ordered by timestamp (newest first)
- `read` field indicates whether the notification has been marked as read
- `time_since` provides human-readable time difference
- `target_url` provides a direct link to the related object

### Mark Notification as Read
- **URL:** `/api/notifications/{id}/read/`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Mark a specific notification as read

**Path Parameters:**
- `id` (int): ID of the notification to mark as read

**Example Request:**
```bash
POST /api/notifications/1/read/
```

**Example Response:**
```json
{
    "message": "Notification marked as read"
}
```

**Error Responses:**
- `404 Not Found`: If the notification doesn't exist or doesn't belong to the user
```json
{
    "error": "Notification not found"
}
```

### Mark All Notifications as Read
- **URL:** `/api/notifications/mark-all-read/`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Mark all unread notifications for the current user as read

**Example Request:**
```bash
POST /api/notifications/mark-all-read/
```

**Example Response:**
```json
{
    "message": "5 notifications marked as read"
}
```

## Notification Types

The API automatically creates notifications for the following events:

### 1. Post Likes
- **Trigger:** When someone likes your post
- **Verb:** "liked your post"
- **Target:** The liked post
- **Note:** No notification is created when you like your own post

### 2. New Followers
- **Trigger:** When someone starts following you
- **Verb:** "started following you"  
- **Target:** The user who followed you
- **Note:** No notification is created when you follow yourself (which is prevented)

### 3. Post Comments
- **Trigger:** When someone comments on your post
- **Verb:** "commented on your post"
- **Target:** The comment object
- **Note:** No notification is created when you comment on your own post

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid data provided",
    "details": {
        "title": ["This field is required."],
        "content": ["Ensure this field has at least 10 characters."]
    }
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Pagination

All list endpoints support pagination with the following format:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/posts/?page=3",
    "previous": "http://localhost:8000/api/posts/?page=1",
    "results": [...]
}
```

## Search and Filtering

### Posts Search and Filter Options:
- **Search by title/content:** `?search=keyword`
- **Filter by author:** `?author=1`
- **Custom title filter:** `?title=keyword`
- **Custom content filter:** `?content=keyword`
- **Ordering:** `?ordering=-created_at` (prefix with `-` for descending)

### Comments Search and Filter Options:
- **Search by content:** `?search=keyword`
- **Filter by post:** `?post=1`
- **Filter by author:** `?author=1`
- **Ordering:** `?ordering=created_at`

## Usage Examples

### 1. Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is my first post on the social media platform!"
  }'
```

### 2. Get All Posts with Search
```bash
curl -X GET "http://localhost:8000/api/posts/?search=Django&page=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Add a Comment to a Post
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post! Thanks for sharing."
  }'
```

### 4. Get My Posts Only
```bash
curl -X GET http://localhost:8000/api/posts/my_posts/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 5. Get Comments for a Specific Post
```bash
curl -X GET http://localhost:8000/api/posts/1/comments/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. Follow a User
```bash
curl -X POST http://localhost:8000/api/auth/follow/5/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 7. Unfollow a User
```bash
curl -X POST http://localhost:8000/api/auth/unfollow/5/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 8. Get Your Personalized Feed
```bash
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 9. Get Your Feed with Pagination
```bash
curl -X GET "http://localhost:8000/api/feed/?page=1&page_size=5" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 10. Like a Post
```bash
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 11. Unlike a Post
```bash
curl -X DELETE http://localhost:8000/api/posts/1/unlike/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 12. Get Your Notifications
```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 13. Mark a Notification as Read
```bash
curl -X POST http://localhost:8000/api/notifications/1/read/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 14. Mark All Notifications as Read
```bash
curl -X POST http://localhost:8000/api/notifications/mark-all-read/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Data Validation Rules

### Posts:
- `title`: Required, minimum 5 characters, maximum 200 characters
- `content`: Required, minimum 10 characters

### Comments:
- `content`: Required, minimum 1 character
- `post`: Required, must be a valid post ID

## Status Codes

- `200 OK`: Successful GET request
- `201 Created`: Successful POST request (resource created)
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently, there are no rate limits implemented, but it's recommended to implement them in production environments.

## Conclusion

This API provides a robust foundation for a social media platform with comprehensive features including:

- **User Authentication**: JWT-based authentication system
- **Posts Management**: Full CRUD operations for posts with search and filtering
- **Comments System**: Nested comments on posts with full management capabilities
- **User Following**: Follow/unfollow functionality to build user networks
- **Personalized Feed**: Dynamic content feed showing posts from followed users
- **Likes System**: Users can like/unlike posts with real-time like counts
- **Notifications System**: Real-time notifications for user interactions including likes, follows, and comments
- **Proper Authorization**: Role-based permissions ensuring users can only modify their own content
- **Pagination**: Efficient handling of large datasets
- **Search & Filtering**: Powerful search capabilities across posts and comments

All endpoints follow REST conventions and return consistent JSON responses. The API is designed to scale and can be extended with additional features like media uploads, direct messaging, and advanced notification preferences.

## New Features Added

### Likes Functionality
- Users can like and unlike posts
- Posts display like counts and whether the current user has liked them
- Unique constraint prevents multiple likes from the same user
- Automatic notification creation when someone likes your post

### Notifications System
- Real-time notifications for user interactions
- Support for different notification types (likes, follows, comments)
- Mark notifications as read/unread
- Bulk mark all notifications as read
- Human-readable timestamps and target URLs
- Efficient querying with proper indexing and relationships