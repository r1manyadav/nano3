# DEPLOY_COMMANDS.md - Copy & Paste Deployment Commands

Use these ready-to-go commands for your chosen deployment method.

---

## 📋 Before Any Deployment

```bash
# Step 1: Create .env file
cd c:\Users\raman\Desktop\nano3\nano3
copy .env.example .env

# Step 2: Generate random keys (copy output to .env)
python -c "import secrets; print(secrets.token_hex(32))"

# Step 3: Edit .env with your values
notepad .env
```

---

## ⚡ METHOD 1: Docker Compose (Easiest - 5 minutes)

### For Local Testing / Development

```bash
# Navigate to project
cd c:\Users\raman\Desktop\nano3\nano3

# Create .env
copy .env.example .env

# Edit .env (set DATABASE_URL, JWT_SECRET_KEY, SECRET_KEY)
notepad .env

# Build and start
docker-compose build
docker-compose up -d

# Check if running
docker-compose ps

# View logs
docker-compose logs -f backend

# Stop when done
docker-compose down
```

### Access
```
http://localhost:5000
```

### Troubleshooting
```bash
# View all logs
docker-compose logs

# Restart specific service
docker-compose restart backend

# Remove containers
docker-compose down -v
```

---

## 🖥️ METHOD 2: VPS Deployment (Ubuntu/Debian)

### Install and Configure

```bash
# SSH into your server
ssh root@your_server_ip

# Update system
apt-get update && apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt-get install -y docker-compose

# Add user to docker group (run subsequent commands as root)
usermod -aG docker $USER

# Clone project
git clone <your-repo-url> /home/nano-app
cd /home/nano-app

# Create environment
cp .env.example .env
nano .env
# Edit DATABASE_URL, JWT_SECRET_KEY, SECRET_KEY, CORS_ORIGINS

# Start app
docker-compose up -d

# View logs
docker-compose logs -f app

# Check health
curl http://localhost:5000/api/health
```

### Add SSL Certificate (Free - Let's Encrypt)

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Get certificate
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificates in: /etc/letsencrypt/live/yourdomain.com/
```

### Auto-Restart on Server Reboot

```bash
# Create systemd service
cat > /etc/systemd/system/nano-app.service << EOF
[Unit]
Description=Nano Test Platform
After=docker.service
Requires=docker.service

[Service]
Restart=always
RestartSec=10
WorkingDirectory=/home/nano-app
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
EOF

# Enable service
systemctl daemon-reload
systemctl enable nano-app
systemctl start nano-app

# Check status
systemctl status nano-app
```

### Access
```
https://yourdomain.com
```

### Manage

```bash
# View logs
docker-compose logs -f app

# Stop
docker-compose down

# Start
docker-compose up -d

# Update code
git pull
docker-compose up -d --build
```

---

## 🚀 METHOD 3: Render.com (Free - No Credit Card)

### Step-by-Step in Render Dashboard

```
1. Sign up at https://render.com (with GitHub)
2. Create new Web Service
   - Select repository
   - Name: nano-test-platform
   - Environment: Python 3
   - Build Command: pip install -r backend/requirements.txt
   - Start Command: gunicorn --chdir backend app:app --workers 4
   - Instance: Free

3. Add Environment Variables:
   FLASK_ENV=production
   JWT_SECRET_KEY=<generate random key>
   SECRET_KEY=<generate random key>
   
4. Add PostgreSQL:
   - New → PostgreSQL
   - Connect to Web Service
   - Render sets DATABASE_URL automatically

5. Click "Deploy"
```

### Alternative: Via Command Line (if you prefer)

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy
render deploy --name nano-test-platform
```

### Access
```
https://nano-test-platform.onrender.com
```

---

## 🔄 METHOD 4: Railway.app (Free Trial)

```bash
# 1. Sign up at https://railway.app (with GitHub)
# 2. Create new project
# 3. Select your repository
# 4. Railway auto-detects Flask
# 5. Add PostgreSQL plugin
# 6. Set environment variables in dashboard
# 7. Deploy button
```

Access: `https://your-project.railway.app`

---

## ⚠️ Troubleshooting Commands

### Docker Issues

```bash
# See what's running
docker ps
docker-compose ps

# Stop everything
docker-compose down

# Full restart
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Connect to running container
docker-compose exec backend bash

# Remove unused images/volumes
docker system prune -a
```

### Database Connection

```bash
# Test PostgreSQL connection
psql postgresql://user:password@host:5432/database

# Inside Docker
docker-compose exec postgres psql -U nano_user -d nano_test_platform -c "SELECT 1"

# SQLite (check file exists)
ls -la backend/instance/nano_test_platform.db
```

### Port Issues

```bash
# Check what's using port 5000
lsof -i :5000  # Mac/Linux

# Kill process
kill -9 <PID>

# Use different port (edit docker-compose.yml)
# Change "5000:5000" to "8000:5000"
```

### Server Issues

```bash
# Check service status
systemctl status nano-app

# View logs
journalctl -u nano-app -f

# Restart service
systemctl restart nano-app

# Check ports
netstat -tlnp | grep python
```

---

## 🧪 Test Your Deployment

```bash
# Test API is responding
curl http://localhost:5000/api/health
# Should return: {"status":"ok"}

# Test with authentication
curl -X POST http://localhost:5000/api/auth/teacher-login \
  -H "Content-Type: application/json" \
  -d '{"teacher_id":"nano123","password":"nano123"}'

# Test CORS headers
curl -i -X OPTIONS http://localhost:5000/api/health
# Should see: Access-Control-Allow-Origin header
```

---

## 📊 Monitor Your App

```bash
# Docker logs (real-time)
docker-compose logs -f app

# Server logs
journalctl -u nano-app -f | head -100

# Database logs
docker-compose logs postgres

# View specific number of lines
docker-compose logs --tail=50 app
```

---

## 🔐 Initial Setup (After First Deployment)

```bash
# Connect to container/server
docker-compose exec backend bash
# OR
ssh user@your_server

# Create superuser/admin
python -c "
from app import app, db
from models import Teacher
with app.app_context():
    teacher = Teacher(username='admin', email='admin@example.com')
    teacher.set_password('your_secure_password')
    db.session.add(teacher)
    db.session.commit()
    print('Admin created!')
"

# Check users
python -c "
from app import app
from models import Teacher
with app.app_context():
    teachers = Teacher.query.all()
    for t in teachers:
        print(f'Username: {t.username}, Email: {t.email}')
"
```

---

## 📝 Generate Keys & Secrets

```bash
# Python method
python -c "import secrets; print(secrets.token_hex(32))"

# Bash method
openssl rand -hex 32

# Online (https://generate-random.org/)
# Select: Hex, 64 characters = 32 bytes

# Use generated output for:
# JWT_SECRET_KEY=<paste here>
# SECRET_KEY=<paste here>
```

---

## 🔄 Update Deployment

### Docker Compose

```bash
# Pull latest code
git pull origin main

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose down
docker-compose up -d

# Check
docker-compose logs -f
```

### VPS Service

```bash
# SSH into server
ssh user@server

cd /path/to/nano-app
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs -f app
```

### Render / Railway

Just push to GitHub, they auto-deploy!

```bash
# Local
git add .
git commit -m "Update code"
git push origin main

# Render/Railway auto-redeploys automatically
```

---

## 🆘 Emergency Commands

```bash
# Stop all Docker containers
docker-compose down

# Force clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Check all services working
docker-compose ps
docker-compose logs

# Reset VPS service
systemctl restart nano-app
systemctl status nano-app
```

---

## ✅ Success Verification

Run these after deploying:

```bash
# Test API
curl -s http://localhost:5000/api/health | grep -o "ok"
# Should return: ok

# Test frontend loads
curl -s http://localhost:5000/ | grep -o "<!DOCTYPE"
# Should return: <!DOCTYPE

# Test database
python -c "from app import db; db.session.execute('SELECT 1')" && echo "DB OK"
# Should return: DB OK

# Test logs for errors
docker-compose logs app | grep -i error
# Should return: nothing or only warnings
```

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Build Docker | `docker-compose build` |
| Start app | `docker-compose up -d` |
| Stop app | `docker-compose down` |
| View logs | `docker-compose logs -f` |
| SSH to server | `ssh user@hostname` |
| Restart service | `systemctl restart nano-app` |
| Generate key | `python -c "import secrets; print(secrets.token_hex(32))"` |
| Test API | `curl http://localhost:5000/api/health` |

---

**All ready! Choose your method and start deploying!** 🚀
