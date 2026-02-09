# QUICK_START_DEPLOY.md - Fastest Deployment in 5 Minutes

Choose ONE method below based on where you want to deploy:

---

## 🚀 Method 1: LOCAL TESTING (Docker on Your Computer)

**Time: 5 minutes | Easiest for testing**

```bash
# 1. Install Docker
# Windows/Mac: Download Docker Desktop from https://www.docker.com/products/docker-desktop
# Linux: sudo apt-get install docker.io docker-compose-plugin

# 2. Create .env file
cd C:\Users\raman\Desktop\nano3\nano3
copy .env.example .env

# 3. Edit .env (optional - defaults are fine for local testing)
# Change DATABASE_URL if needed

# 4. Start everything
docker-compose up -d

# 5. Access your app
# Open browser: http://localhost:5000
# Backend API: http://localhost:5000/api/health

# 6. View logs
docker-compose logs -f backend

# 7. Stop when done
docker-compose down
```

✅ **Your app is running at http://localhost:5000**

---

## 🌐 Method 2: VPS/LINUX SERVER (DigitalOcean, Linode, AWS, etc.)

**Time: 15-30 minutes | Best for production**

### Step 1: Connect to Your Server
```bash
ssh root@your_server_ip
```

### Step 2: Run Setup Script (Automated)
```bash
apt-get update
apt-get install -y curl
curl -O https://your-domain.com/setup.sh
bash setup.sh
```

### Step 3: Manual Setup (If script not available)

```bash
# Update system
sudo apt-get update && apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install -y docker-compose

# Clone your project
git clone <your-repo-url> /home/nano-app
cd /home/nano-app

# Create .env
cp .env.example .env
nano .env
# Change these:
# DATABASE_URL=postgresql://nano_user:your_strong_password@localhost:5432/nano_test_platform
# JWT_SECRET_KEY=<generate random 32 char string>
# SECRET_KEY=<generate random 32 char string>
# CORS_ORIGINS=https://yourdomain.com

# Start with Docker Compose
docker-compose up -d

# Setup SSL (Free with Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# View logs
docker-compose logs -f app
```

✅ **Your app is running at https://yourdomain.com**

---

## 🆓 Method 3: FREE Hosting (Render.com - NO CREDIT CARD NEEDED)

**Time: 10 minutes | Best free option**

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in:
   - Name: `nano-test-platform`
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `gunicorn --chdir backend app:app --workers 4`

### Step 3: Add Environment Variables
In Render dashboard, add:
```
FLASK_ENV=production
JWT_SECRET_KEY=<generate random key>
SECRET_KEY=<generate random key>
```

### Step 4: Add Free PostgreSQL
1. Click "New +" → "PostgreSQL"
2. Connect to your Web Service
3. Render automatically sets DATABASE_URL

### Step 5: Deploy
Click "Deploy" and wait (2-5 minutes)

✅ **Your app is running at https://nano-test-platform.onrender.com**

---

## 🔧 Generate Random Security Keys

```bash
# Option 1: Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 2: Online
Visit: https://generate-random.org/
Generate 32 character hex string
```

Copy output to JWT_SECRET_KEY and SECRET_KEY in .env

---

## 📋 Troubleshooting

### "Port 5000 already in use"
```bash
# Find what's using it
lsof -i :5000

# Kill it
kill -9 <PID>

# Or use different port - edit docker-compose.yml
```

### "Database connection error"
```bash
# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Check if PostgreSQL is running (if using it)
docker-compose ps
docker-compose logs postgres
```

### "CORS error in browser console"
```bash
# Update CORS_ORIGINS in .env
CORS_ORIGINS=https://yourdomain.com

# Restart
docker-compose restart app
```

### "500 error when accessing app"
```bash
# Check backend logs
docker-compose logs app

# Check database exists
docker-compose exec postgres psql -U nano_user -d nano_test_platform -c "\dt"
```

---

## ✨ Working App Checklist

- [ ] App loads at http://localhost:5000 (or your domain)
- [ ] Can reach /api/health endpoint (returns 200)
- [ ] Login page displays
- [ ] No CORS errors in browser console
- [ ] Database is connected
- [ ] File uploads work (if testing image upload)

---

## 🎯 Next Steps

1. **Local Testing**: Use Method 1 to test locally
2. **Deploy**: Choose Method 2 (VPS) or Method 3 (Free)
3. **Production**: Domain + SSL + Database backup
4. **Monitor**: Check logs regularly, set up uptime monitoring

---

## 📞 Need Help?

Check **DEPLOYMENT_READY.md** for detailed guides per method.

Questions? Common issues in Troubleshooting section above.
