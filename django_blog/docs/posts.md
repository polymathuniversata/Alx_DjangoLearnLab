# Blog Post Management (CRUD)

This document describes how blog post CRUD features work in the Django Blog.

## Views
- List: `PostListView` — `/posts/`
- Detail: `PostDetailView` — `/posts/<pk>/`
- Create: `PostCreateView` (login required) — `/posts/new/`
- Update: `PostUpdateView` (author only) — `/posts/<pk>/edit/`
- Delete: `PostDeleteView` (author only) — `/posts/<pk>/delete/`

## Forms
- `PostForm` (`blog/forms.py`) with fields: `title`, `content`.
- Author is set automatically in `PostCreateView.form_valid()`.

## Templates
Located in `blog/templates/blog/`:
- `post_list.html`, `post_detail.html`, `post_form.html`, `post_confirm_delete.html`

## Permissions
- Create: `LoginRequiredMixin`
- Edit/Delete: `UserPassesTestMixin` ensures only the post author can modify or delete.
- List/Detail: public.

## Navigation
- `base.html` includes a "Posts" link. List page shows a "New Post" link for authenticated users.

## Testing
1. Visit `/posts/` — should list posts (or say none).
2. Register/Login, then go to `/posts/new/` to create a post.
3. After saving, you should be redirected to the post detail page.
4. From the detail page, use Edit/Delete (visible only to the author).
5. Confirm non-authors cannot access edit/delete URLs.
