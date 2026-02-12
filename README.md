# NexTalk Backend API

Django REST Framework backend for **NexTalk** — a social media application for connecting, sharing, and chatting.

## Features

- 🔐 JWT Authentication
- 👤 User Profiles
- 📝 Posts with Images/Videos
- ❤️ Likes and Comments
- 👥 Friend Requests & Follow System
- 💬 Real-time Chat (WebSocket)
- 🛡️ Admin Panel

## Tech Stack

- Django 5.2
- Django REST Framework
- Django Channels (WebSocket)
- PostgreSQL (production)
- JWT Authentication
- Deployed on Render

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoints

| Module   | Endpoint                | Method |
|----------|------------------------|--------|
| Auth     | `/api/auth/register/`  | POST   |
| Auth     | `/api/auth/login/`     | POST   |
| Auth     | `/api/auth/logout/`    | POST   |
| Auth     | `/api/auth/profile/`   | GET/PATCH |
| Posts    | `/api/posts/`          | GET/POST |
| Posts    | `/api/posts/<id>/`     | GET/PUT/DELETE |
| Posts    | `/api/posts/<id>/like/`| POST   |
| Friends  | `/api/friends/request/`| POST   |
| Friends  | `/api/friends/follow/<id>/` | POST |
| Chat     | `/api/chat/rooms/`     | GET    |
| Chat     | `/api/chat/messages/send/` | POST |
