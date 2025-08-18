# Tagging and Search

This document describes the tagging and search features added to the Django Blog.

## Models
- `Tag` (`blog/models.py`): unique `name`.
- `Post.tags`: `ManyToManyField(Tag, blank=True)`.

## Forms
- `PostForm` (`blog/forms.py`): adds `tags_csv` (comma-separated). On save, creates/fetches `Tag`s and assigns to the post.

## Views
- `PostListView`: supports query param `q` to search title/content/tags.
- `PostByTagListView`: lists posts filtered by tag name (case-insensitive) at `/tags/<name>/`.
- `SearchView`: alias view using the same template as list.

## URLs (`blog/urls.py`)
- `GET /posts/?q=...` — search via list view.
- `GET /tags/<name>/` — filter posts by tag.
- `GET /search/?q=...` — optional separate route (uses same template).

## Templates
- `blog/templates/blog/post_form.html`: uses `{{ form.as_p }}` which now includes `tags_csv`.
- `blog/templates/blog/post_list.html`: shows a search bar and displays tags per post.
- `blog/templates/blog/post_detail.html`: displays tags with links to tag page.

## Admin
- `Tag` registered in admin for management.

## How to Use
1. When creating or editing a post, enter tags as `comma, separated, list`.
2. On list page, use the search bar to filter by keywords or tag names.
3. Click a tag link to view all posts with that tag.

## Testing
- Create posts with tags; verify tags render on list and detail.
- Search by title/content keywords and by tag names; verify results.
- Visit `/tags/<name>/` for a tag and check filtered posts.
