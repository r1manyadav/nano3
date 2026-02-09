# Nano Test Platform

A complete web-based testing platform with teacher dashboard and student testing interface.

## Project Structure

```
nano3/
├── backend/              # Flask Python backend
│   ├── app.py           # Main Flask application
│   ├── models.py        # Database models
│   ├── wsgi.py          # WSGI entry point
│   ├── requirements.txt  # Python dependencies
│   ├── .env.example     # Environment variables template
│   └── uploads/         # User file uploads directory
├── frontend/            # HTML/CSS/JS frontend
│   ├── index.html       # Student home page
│   ├── teacher-dashboard.html
│   ├── api.js          # Frontend API client
│   └── style.css       # Styling
├── Dockerfile          # Docker containerization
├── docker-compose.yml  # Multi-container setup
└── nginx.conf         # Nginx reverse proxy config
```

## Quick Start - Deployment Ready

See [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md) for complete step-by-step deployment instructions.

## Features

- Teacher login and authentication
- Student test administration
- Real-time test scoring
- Image upload support
- JWT-based security
- PostgreSQL database support
- Docker deployment ready

## Deployment Options

1. **Docker Compose** (Recommended for beginners)
2. **Traditional VPS/Server**
3. **PaaS Platforms** (Heroku, Render, Railway, etc.)

---

For detailed deployment instructions, see [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)
