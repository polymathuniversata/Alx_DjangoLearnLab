# Comment System

This document explains how the blog comment system works.

## Overview
- Users can view comments on a post detail page.
- Only authenticated users can add comments.
- Only the comment author can edit or delete their comment.

## Models
- `Comment` in `blog/models.py` with fields:
  - `post` (FK to `Post`, `related_name='comments'`)
  - `author` (FK to `User`, `related_name='comments'`)
  - `content` (Text)
  - `created_at` (auto_now_add)
  - `updated_at` (auto_now)

## Forms
- `CommentForm` in `blog/forms.py` — provides a single `content` textarea.

## Views and URLs
- `PostDetailView` includes comments and a `comment_form` in context.
- Create: `CommentCreateView` — `POST /posts/<post_pk>/comments/new/` (name: `comment-create`)
- Update: `CommentUpdateView` — `/comments/<pk>/edit/` (name: `comment-edit`)
- Delete: `CommentDeleteView` — `/comments/<pk>/delete/` (name: `comment-delete`)

All redirect back to the parent post detail page on success.

## Templates
Located in `blog/templates/blog/`:
- `post_detail.html` — renders list of comments and inline form to add a comment.
- `comment_form.html` — used for create and update.
- `comment_confirm_delete.html` — delete confirmation page.

## Permissions
- Adding a comment requires login (`LoginRequiredMixin`).
- Editing/Deleting requires the current user to be the comment author (`UserPassesTestMixin`).

## How to Use
1. Go to a post detail page (`/posts/<pk>/`).
2. Scroll to the comments section.
3. If logged in, write a comment and submit.
4. As the author, you will see Edit/Delete links next to your comments.

## Testing Checklist
- Create a user and log in.
- Add a comment to a post. Verify it appears and you see a success message.
- Edit your comment via the Edit link. Confirm the update and success message.
- Delete your comment via the Delete link. Confirm it is removed.
- Log in as a different user and ensure you cannot edit/delete others' comments.
- Verify that non-authenticated users see a prompt to log in to comment.
