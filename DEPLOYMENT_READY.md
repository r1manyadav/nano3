# DEPLOYMENT_READY.md - Complete Step-by-Step Deployment Guide

Your application is now clean and ready for deployment! Follow this guide to deploy your Nano Test Platform.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Option 1: Docker Compose (Easiest - Local/VPS)](#option-1-docker-compose-easiest)
3. [Option 2: Traditional Server Deployment](#option-2-traditional-server-deployment)
4. [Option 3: Free PaaS Platforms](#option-3-free-paas-platforms)
5. [Configuration Guide](#configuration-guide)
6. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

- [ ] Clean workspace completed ✓
- [ ] All test files removed ✓
- [ ] Environment variables template created ✓
- [ ] Docker files ready ✓
- [ ] Frontend files clean ✓

### What You Need

- **For Docker**: Install Docker and Docker Compose
- **For VPS**: Linux server with Python 3.11+
- **Database**: PostgreSQL (recommended) or SQLite (for testing)
- **Domain**: (Optional) A domain name for your website

---

## Option 1: Docker Compose (EASIEST)

### Step 1: Install Docker and Docker Compose

**Windows/Mac:**
- Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Install and start it

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

### Step 2: Create Environment File

Navigate to your project root and create `.env` file:

```bash
# Windows (PowerShell)
copy .env.example .env

# Or Linux/Mac
cp .env.example .env
```

Edit `.env` file with your values:

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000

# For local testing, you can use:
DATABASE_URL=sqlite:///nano_test_platform.db

# Or for PostgreSQL (recommended):
DATABASE_URL=postgresql://nano_user:nano_password@db:5432/nano_test_platform

# Generate random keys:
JWT_SECRET_KEY=abc123def456ghi789jkl012mno345pqr
SECRET_KEY=xyz789abc456def123ghi012jkl345mno

CORS_ORIGINS=http://localhost,http://192.168.1.100
```

**Generate Random Secret Keys:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Verify docker-compose.yml

Check that your `docker-compose.yml` exists and is correct:

```yaml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend/uploads:/app/uploads
    depends_on:
      - db
      
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: nano_user
      POSTGRES_PASSWORD: nano_password
      POSTGRES_DB: nano_test_platform
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  db_data:
```

### Step 4: Build and Run

```bash
# Build the Docker images
docker-compose build

# Start all containers (runs in foreground, shows logs)
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop containers
docker-compose down
```

### Step 5: Access Your Application

- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:5000 (served from backend)
- **Health Check**: http://localhost:5000/api/health

### Step 6: Initialize Database (First Time Only)

```bash
# Connect to backend container
docker-compose exec backend bash

# Inside container, create admin user if needed
python
>>> from models import db, Teacher
>>> teacher = Teacher(username='teacher1', email='teacher@example.com')
>>> teacher.set_password('password123')
>>> db.session.add(teacher)
>>> db.session.commit()
>>> exit()
```

---

## Option 2: Traditional Server Deployment

### Step 1: Server Setup (Ubuntu/Debian)

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3.11 python3-pip postgresql nginx git curl

# Install Python virtual environment
sudo apt-get install -y python3.11-venv

# Create application user
sudo useradd -m -s /bin/bash nano-app
sudo su - nano-app
```

### Step 2: Clone and Setup Project

```bash
# Download your project
git clone <your-repo-url> nano3
cd nano3

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
pip install gunicorn
```

### Step 3: Configure PostgreSQL Database

```bash
# As root user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE USER nano_user WITH PASSWORD 'nano_password';
CREATE DATABASE nano_test_platform OWNER nano_user;
ALTER ROLE nano_user SET client_encoding TO 'utf8';
ALTER ROLE nano_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE nano_user SET default_transaction_deferrable TO on;
ALTER ROLE nano_user SET default_transaction_level TO 'read committed';
\q

# Test connection
psql -U nano_user -d nano_test_platform -h localhost
\q
```

### Step 4: Create Environment File

```bash
cd ~/nano3
nano backend/.env

# Add this:
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://nano_user:nano_password@localhost:5432/nano_test_platform
JWT_SECRET_KEY=<generate-random-key>
SECRET_KEY=<generate-random-key>
CORS_ORIGINS=https://yourdomain.com
```

### Step 5: Test Application

```bash
cd ~/nano3
source venv/bin/activate
cd backend
python app.py
# Should see: Running on http://localhost:5000
```

Press `Ctrl+C` to stop.

### Step 6: Create Systemd Service

```bash
# As sudo/root
sudo nano /etc/systemd/system/nano-app.service

# Add this:
[Unit]
Description=Nano Test Platform
After=network.target

[Service]
User=nano-app
WorkingDirectory=/home/nano-app/nano3
ExecStart=/home/nano-app/nano3/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 0.0.0.0:5000 \
    --access-logfile /var/log/nano-app-access.log \
    --error-logfile /var/log/nano-app-error.log \
    backend.app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 7: Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable nano-app
sudo systemctl start nano-app

# Check status
sudo systemctl status nano-app

# View logs
sudo journalctl -u nano-app -f
```

### Step 8: Configure Nginx as Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/nano3

# Add this:
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/nano-app/nano3/backend/static/;
    }

    location /uploads/ {
        alias /home/nano-app/nano3/backend/uploads/;
    }
}

# Disable default
sudo rm /etc/nginx/sites-enabled/default

# Enable site
sudo ln -s /etc/nginx/sites-available/nano3 /etc/nginx/sites-enabled/

# Test Nginx config
sudo nginx -t

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Step 9: SSL/HTTPS Certificate (Free with Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto renewal
sudo systemctl enable certbot.timer
```

### Step 10: Verify Deployment

```bash
# Check services running
sudo systemctl status nano-app
sudo systemctl status nginx

# Check logs
sudo journalctl -u nano-app -n 50

# Test endpoint
curl http://localhost:5000/api/health
```

---

## Option 3: Free PaaS Platforms

### Option 3A: Render.com (Recommended - Free Tier)

#### Step 1: Prepare for Render

Your project already has a `Procfile`:
```
web: gunicorn backend.app:app
```

Update it if needed to:
```
release: cd backend && flask db upgrade
web: gunicorn --workers 4 --bind 0.0.0.0:$PORT backend.app:app
```

#### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Connect your GitHub repository

#### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Select your repository
3. Fill in details:
   - **Name**: nano-test-platform
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn --chdir backend app:app --workers 4`
   - **Instance Type**: Free

#### Step 4: Add Environment Variables

In the Environment section, add:
```
FLASK_ENV=production
DATABASE_URL=<Connect PostgreSQL>
JWT_SECRET_KEY=<Generate random key>
SECRET_KEY=<Generate random key>
```

#### Step 5: Add PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Connect it to your Web Service
3. Render will set DATABASE_URL automatically

#### Step 6: Deploy

- Click "Deploy"
- Watch the logs for any errors
- Once deployed, you get a free subdomain: `https://nano-test-platform.onrender.com`

---

### Option 3B: Railway.app (Free Trial)

1. Go to https://railway.app
2. Sign up and connect GitHub
3. Create new project
4. Add your repository
5. Railway auto-detects Flask and deploys
6. Add PostgreSQL plugin from Railway dashboard
7. Set environment variables in Railway dashboard

---

### Option 3C: Heroku (Limited Free, Paid)

```bash
# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create nano-test-platform

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set JWT_SECRET_KEY=<random-key>
heroku config:set SECRET_KEY=<random-key>

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

---

## Configuration Guide

### Database Connection Strings

**SQLite (Development/Testing):**
```
DATABASE_URL=sqlite:///nano_test_platform.db
```

**PostgreSQL (Production):**
```
DATABASE_URL=postgresql://username:password@hostname:5432/database_name
```

**PostgreSQL with Docker Compose:**
```
DATABASE_URL=postgresql://nano_user:nano_password@db:5432/nano_test_platform
```

### Generate Secure Keys

```python
# In Python terminal
import secrets

# Generate JWT Secret
jwt_key = secrets.token_hex(32)
print(f"JWT_SECRET_KEY={jwt_key}")

# Generate Secret Key
secret = secrets.token_hex(32)
print(f"SECRET_KEY={secret}")
```

Or use online: https://generate-random.org/

### CORS Configuration

**Development:**
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:8000
```

**Production:**
```
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## Troubleshooting

### Issue: "Connection refused" when accessing the site

**Solution:**
```bash
# Check if backend is running
docker-compose ps
# or
sudo systemctl status nano-app

# Check ports
netstat -tlnp | grep 5000

# Restart
docker-compose restart backend
# or
sudo systemctl restart nano-app
```

### Issue: "Database connection error"

**Solution:**
```bash
# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Test database connection
psql <connection-string>

# For Docker
docker-compose logs db
```

### Issue: "CORS error in browser"

**Solution:**
- Update CORS_ORIGINS in .env to match your domain
- Restart backend: `docker-compose restart backend`

### Issue: "Upload fails - permission denied"

**Solution:**
```bash
# Fix uploads folder permissions
docker-compose exec backend bash
chmod -R 777 /app/uploads

# Or on server
sudo chown -R nano-app:nano-app ~/nano3/backend/uploads
sudo chmod -R 755 ~/nano3/backend/uploads
```

### Issue: "Module not found" error

**Solution:**
```bash
# Rebuild Docker image (forces fresh build)
docker-compose build --no-cache backend

# Or reinstall Python packages
pip install -r backend/requirements.txt --force-reinstall
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Find what's using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
# Edit docker-compose.yml or Nginx config
```

---

## Maintenance

### Backup Database

```bash
# PostgreSQL backup
pg_dump -U nano_user nano_test_platform > backup.sql

# Restore
psql -U nano_user nano_test_platform < backup.sql
```

### View Logs

```bash
# Docker
docker-compose logs -f backend

# SystemD Service
journalctl -u nano-app -f

# Nginx
tail -f /var/log/nginx/access.log
```

### Update Application

```bash
# Git pull latest
git pull origin main

# Rebuild Docker
docker-compose build --no-cache
docker-compose up -d

# Or on server
cd ~/nano3
git pull
source venv/bin/activate
pip install -r backend/requirements.txt
sudo systemctl restart nano-app
```

---

## Useful Commands Reference

```bash
# Docker Compose
docker-compose up -d          # Start in background
docker-compose down           # Stop all containers
docker-compose logs -f        # View logs
docker-compose exec backend bash  # Connect to container

# SystemD Service
sudo systemctl start nano-app
sudo systemctl stop nano-app
sudo systemctl restart nano-app
sudo systemctl status nano-app

# Nginx
sudo nginx -t                 # Test config
sudo systemctl reload nginx   # Reload config
sudo systemctl restart nginx  # Restart service

# Database
psql -U nano_user -d nano_test_platform  # Connect to DB
\dt                          # List tables
\q                           # Quit
```

---

## Next Steps

1. **Choose your deployment method** (Docker Compose recommended for simplicity)
2. **Create .env file** with your configuration
3. **Deploy** following the specific option guide
4. **Test** by accessing your application
5. **Set up monitoring** and backups for production

---

## Support & Debugging

If you encounter issues:

1. Check logs: `docker-compose logs backend` or `systemctl status nano-app`
2. Verify .env variables are set correctly
3. Ensure database is running and accessible
4. Check firewall settings allow port 5000/80/443
5. Review troubleshooting section above

---

**Your application is ready to deploy! Choose an option above and follow the step-by-step guide. Docker Compose is recommended for fastest setup.**
