# Blog API System

A fully functional blog system built with Django REST Framework, featuring user authentication, blog posts, comments, likes, bookmarks, and promotional content.

## Features

### 🔐 Authentication & User Management

- Custom User model with email-based authentication
- JWT token authentication
- User roles (user/admin)
- Password reset functionality
- User profiles with bio and photo

### 📝 Blog Posts

- Create, read, update, delete blog posts
- Draft, published, and archived status
- Slug-based URLs
- Featured images
- Read time estimation
- Admin-only post management

### 💬 Comments

- Nested/threaded comments
- Comment approval system
- Reply functionality

### ❤️ Likes & Bookmarks

- Like/unlike blog posts
- Bookmark/unbookmark posts
- Like and bookmark counts
- User-specific like and bookmark lists

### 🔔 Notifications

- Real-time notifications for likes, comments, and bookmarks
- Mark notifications as read/unread
- Bulk notification management

### 📢 Promotions

- Separate promotional content system
- Similar to blog posts but for promotional material

## API Endpoints

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/users/forgot-password/` - Password reset

### User Management

- `GET /api/users/<user_id>/` - Get user details
- `PUT /api/users/update/` - Update user profile
- `GET /api/bookmarks/` - Get user bookmarks
- `POST /api/bookmarks/create/` - Create bookmark
- `DELETE /api/bookmarks/<post_id>/delete/` - Remove bookmark
- `GET /api/likes/` - Get user likes
- `POST /api/likes/create/` - Create like
- `DELETE /api/likes/<post_id>/delete/` - Remove like

### Blog Posts

- `GET /api/posts/published/` - List published posts
- `GET /api/posts/admin/` - Admin: List all posts
- `GET /api/posts/<slug>/` - Get post by slug
- `POST /api/posts/` - Create new post
- `PUT /api/posts/<post_id>/` - Update post
- `DELETE /api/posts/<post_id>/delete/` - Delete post
- `PUT /api/posts/<post_id>/status/` - Update post status (admin)

### Likes

- `POST /api/posts/<post_id>/like/` - Like a post
- `DELETE /api/posts/<post_id>/unlike/` - Unlike a post
- `GET /api/posts/<post_id>/like-count/` - Get like count

### Bookmarks

- `POST /api/posts/<post_id>/bookmark/` - Bookmark a post
- `DELETE /api/posts/<post_id>/unbookmark/` - Remove bookmark
- `GET /api/posts/<post_id>/bookmark-count/` - Get bookmark count

### Comments

- `GET /api/posts/<post_id>/comments/` - List comments
- `POST /api/posts/<post_id>/comments/` - Create comment
- `DELETE /api/comments/<comment_id>/delete/` - Delete comment

### Notifications

- `GET /api/notifications/` - List notifications
- `POST /api/notifications/<notification_id>/read/` - Mark as read
- `POST /api/notifications/read-all/` - Mark all as read

### Promotions

- `GET /api/promotions/` - List published promotions
- `POST /api/promotions/create/` - Create promotion
- `GET /api/promotions/<slug>/` - Get promotion by slug
- `PUT /api/promotions/<promotion_id>/update/` - Update promotion
- `DELETE /api/promotions/<promotion_id>/delete/` - Delete promotion

## Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Models

### User Model

- `email` - Unique email address
- `username` - Username
- `bio` - User biography
- `photo` - Profile picture
- `role` - User role (user/admin)
- `created_at` - Account creation date

### BlogPost Model

- `author` - Post author (User)
- `title` - Post title
- `slug` - URL slug
- `content` - Post content
- `excerpt` - Post excerpt
- `status` - Post status (draft/published/archived)
- `read_time` - Estimated reading time
- `featured_image` - Post image
- `created_at` - Creation date
- `updated_at` - Last update date
- `published_at` - Publication date

### Comment Model

- `blog_post` - Related blog post
- `author` - Comment author
- `parent` - Parent comment (for replies)
- `content` - Comment content
- `is_approved` - Approval status
- `created_at` - Creation date

### Notification Model

- `recipient` - Notification recipient
- `sender` - Notification sender
- `notification_type` - Type (like/comment/bookmark/review)
- `blog_post` - Related blog post
- `comment` - Related comment
- `message` - Notification message
- `is_read` - Read status
- `created_at` - Creation date

### Bookmark & Like Models

- `user` - User who bookmarked/liked
- `blog_post` - Bookmarked/liked post
- `created_at` - Creation date

### Promotion Model

- `author` - Promotion author
- `slogan` - Promotion slogan
- `content` - Promotion content
- `slug` - URL slug
- `status` - Status (draft/published/archived)
- `created_at` - Creation date

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Permissions

- **AllowAny**: Public endpoints (published posts, comments)
- **IsAuthenticated**: User-specific actions (create posts, like, bookmark)
- **IsAdminUser**: Admin-only actions (manage all posts, approve comments)

## Development

### Adding New Features

1. Create/update models in the appropriate app
2. Create serializers for the models
3. Create views for the endpoints
4. Add URL patterns
5. Update admin interface
6. Test the endpoints

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Test Data

```bash
python manage.py shell
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
