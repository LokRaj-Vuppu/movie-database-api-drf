# Movie Database API (WatchMate) 🎬

A **REST API** for a movie database built with **Django REST Framework**. Users can browse movies, post reviews, give ratings, and access detailed movie information — all secured with **JWT authentication**.

---

## Features

- Browse and search movies / watch list
- User registration and JWT-based login
- Post, update, and delete movie reviews
- Rate movies with a numeric score
- Filter and search movies using `django-filter`
- Throttling to limit API request rates
- Pagination on list endpoints
- Permission-based access (authenticated users only for reviews)
- CI/CD via GitHub Actions

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Django | Web framework |
| Django REST Framework | REST API |
| SimpleJWT | JWT authentication |
| django-filter | Query filtering and search |
| SQLite | Default development database |

---

## Project Structure

```
movie-database-api-drf/
├── .github/workflows/   # GitHub Actions CI
├── watchmate/           # Main Django project
│   ├── watchmate/       # Project settings and URLs
│   ├── watchlist_app/   # Movies, reviews, and ratings app
│   └── user_app/        # User registration and authentication
├── manage.py
└── README.md
```

---

## Getting Started

### Installation

```bash
git clone https://github.com/LokRaj-Vuppu/movie-database-api-drf.git
cd movie-database-api-drf

python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

pip install -r requirements.txt   # or: pip install django djangorestframework djangorestframework-simplejwt django-filter
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/account/register/` | Register new user |
| POST | `/account/login/` | Obtain JWT tokens |
| POST | `/account/token/refresh/` | Refresh access token |
| POST | `/account/logout/` | Logout (blacklist token) |

### Movies / Watch List

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/watch/list/` | List all movies |
| POST | `/watch/list/` | Add a new movie (admin) |
| GET | `/watch/<id>/` | Get movie details |
| PUT | `/watch/<id>/` | Update movie (admin) |
| DELETE | `/watch/<id>/` | Delete movie (admin) |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/watch/<id>/review/` | List reviews for a movie |
| POST | `/watch/<id>/review-create/` | Add a review (auth required) |
| GET | `/watch/review/<id>/` | Get a specific review |
| PUT | `/watch/review/<id>/` | Update your review |
| DELETE | `/watch/review/<id>/` | Delete your review |

> *(Update endpoints to match your exact `urls.py` if they differ)*

---

## Authentication Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/account/register/ \
  -d '{"username": "user1", "password": "pass123", "password2": "pass123", "email": "user1@example.com"}'

# 2. Login — get tokens
curl -X POST http://localhost:8000/account/login/ \
  -d '{"username": "user1", "password": "pass123"}'

# 3. Use access token
curl -X GET http://localhost:8000/watch/list/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Filtering & Search

Filter movies by platform, search by title:

```
GET /watch/list/?search=inception
GET /watch/list/?platform=Netflix
```

---

## Author

**LokRaj Vuppu** — [GitHub](https://github.com/LokRaj-Vuppu)
