# MCQ Test Platform - Deployment Guide

## Deployment Options Comparison

| Platform | Cost | Ease | Scalability | Best For |
|----------|------|------|-------------|----------|
| **Render.com** | Free-$7/mo | ⭐⭐⭐⭐⭐ | Small-Medium | Quick deployment |
| **Railway.app** | Pay-as-you-go | ⭐⭐⭐⭐⭐ | Small-Medium | Easy setup |
| **PythonAnywhere** | Free-$5/mo | ⭐⭐⭐⭐ | Small | Python-focused |
| **Heroku** | Paid only | ⭐⭐⭐⭐ | Small-Medium | Mature platform |
| **AWS** | Varies | ⭐⭐⭐ | Unlimited | Enterprise |
| **DigitalOcean** | $6+/mo | ⭐⭐⭐ | Small-Large | VPS control |

---

## OPTION 1: Deploy on Render.com (Recommended - Easiest)

### Prerequisites
- GitHub account (create free at github.com)
- Render account (register at render.com)

### Step 1: Prepare Your Code for Git
```bash
cd c:\Users\raman\Desktop\nano\nano
git init
git add .
git commit -m "MCQ Test Platform - Initial setup"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Create repository named `nano-test-platform`
3. Don't initialize with README (we already have files)
4. Click "Create repository"

### Step 3: Push Code to GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/nano-test-platform.git
git branch -M main
git push -u origin main
```

### Step 4: Prepare Flask App for Production
Create [backend/production_config.py](backend/production_config.py):
```python
import os
from datetime import timedelta

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///nano_test_platform.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # App Settings
    DEBUG = False
    TESTING = False
```

### Step 5: Update Backend app.py for Production
Add at the top of [backend/app.py](backend/app.py) after imports:
```python
import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Load config
if os.getenv('FLASK_ENV') == 'production':
    from production_config import Config
    app.config.from_object(Config)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nano_test_platform.db'

# CORS for frontend
CORS(app)
```

### Step 6: Create requirements.txt (if not exists)
```bash
cd backend
pip freeze > requirements.txt
```

### Step 7: Create Procfile in Root Directory
File: `Procfile`
```
web: cd backend && python app.py
```

### Step 8: Create render.yaml
File: `render.yaml`
```yaml
services:
  - type: web
    name: nano-test-platform
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && gunicorn 'app:app'"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
```

### Step 9: Deploy on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account
5. Select `nano-test-platform` repository
6. Choose branch: `main`
7. Set Runtime: `Python`
8. Build Command: `pip install -r backend/requirements.txt`
9. Start Command: `cd backend && gunicorn 'app:app'`
10. Click "Create Web Service"

### Step 10: Update Frontend API URLs
After deployment, update [frontend/api.js](frontend/api.js):
```javascript
// Change this line:
const BASE_URL = 'http://localhost:5000/api';

// To this:
const BASE_URL = 'https://your-app-name.onrender.com/api';
```

Then push changes:
```bash
git add frontend/api.js
git commit -m "Update API URL for production"
git push origin main
```

---

## OPTION 2: Deploy on Railway.app (Very Easy)

### Step 1-3: Same as Render (Git setup)

### Step 2: Connect Railway
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select `nano-test-platform` repo

### Step 3: Configure Environment
1. Click "Add Variables"
2. Add these variables:
   ```
   FLASK_ENV = production
   SECRET_KEY = (generate a random string)
   DATABASE_URL = sqlite:///nano_test_platform.db
   ```

### Step 4: Finish Deployment
Railway auto-detects Python and deploys. Takes ~5 minutes.

View your app URL in the Railway dashboard.

---

## OPTION 3: Deploy on PythonAnywhere (Simple)

### Step 1: Create PythonAnywhere Account
- Go to https://www.pythonanywhere.com
- Sign up (free account available)

### Step 2: Upload Code
1. Click "Upload a file" 
2. Upload your project as a ZIP file
3. Or use Git: `git clone` directly in PythonAnywhere

### Step 3: Create New Web App
1. Click "Web" tab
2. Click "Add a new web app"
3. Choose "Python 3.11"
4. Choose "Flask"

### Step 4: Configure
1. Edit WSGI configuration file with:
```python
import sys
path = '/home/yourusername/nano'
if path not in sys.path:
    sys.path.append(path)

from backend.app import app as application
```

### Step 5: Reload
Click "Reload" button. Your app is live at `yourusername.pythonanywhere.com`

---

## OPTION 4: Deploy with PostgreSQL (Production-Grade)

### Prerequisites
- Consider using PostgreSQL instead of SQLite for better production support
- More robust for multiple concurrent users

### Step 1: Update Backend for PostgreSQL
In [backend/app.py](backend/app.py):
```python
import os

# Use PostgreSQL in production
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nano_test_platform.db'
```

### Step 2: Install PostgreSQL Driver
```bash
pip install psycopg2-binary
pip freeze > backend/requirements.txt
```

### Step 3: Database Migration
When deploying with fresh PostgreSQL:
```bash
# In production environment, run once:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## Post-Deployment Checklist

- [ ] **Update API URLs** - Change localhost:5000 to production URL
- [ ] **Test All Endpoints** - Run test suite against live API
- [ ] **Change Secret Key** - Use strong random key, not default
- [ ] **Enable HTTPS** - Most platforms auto-enable SSL
- [ ] **Test Student Login** - nano1/nano1 should work
- [ ] **Test Teacher Login** - nano123/nano123 should work
- [ ] **Check Database** - Seeded data should be present
- [ ] **Monitor Logs** - Set up error tracking
- [ ] **Backup Database** - Regular database backups
- [ ] **Domain Setup** - Add custom domain if needed

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution:** Ensure Procfile or start command includes `cd backend && python app.py`

### Issue: "CORS errors" when frontend calls API
**Solution:** Update CORS settings in [backend/app.py](backend/app.py):
```python
CORS(app, resources={r"/api/*": {"origins": ["your-deployed-url.com"]}})
```

### Issue: Database empty after deployment
**Solution:** Seed database after deployment:
```bash
# SSH into server and run:
python backend/seed_students.py
```

### Issue: "No module named 'flask'"
**Solution:** Ensure requirements.txt is correct and deploy process runs `pip install -r backend/requirements.txt`

---

## Recommended Deployment Path

**For beginners:** Render.com (5 minutes setup)
**For more control:** Railway.app (10 minutes setup)
**For lowest cost:** PythonAnywhere Free (15 minutes setup)
**For production:** AWS + PostgreSQL (1 hour setup)

---

## Quick Deploy Commands

### Render.com Quick Setup:
```bash
cd c:\Users\raman\Desktop\nano\nano
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/nano-test-platform.git
git push -u origin main
# Then connect via render.com dashboard
```

### Local Testing Before Deploy:
```bash
# Test with Gunicorn (production server)
cd backend
pip install gunicorn
gunicorn 'app:app'
# Visit http://localhost:8000
```

---

## Next Steps

1. **Choose a platform** from the options above
2. **Follow the deployment steps** for your chosen platform
3. **Update API URLs** in [frontend/api.js](frontend/api.js)
4. **Test all features** on the live deployment
5. **Set up monitoring** for error tracking

**Estimated Time:** 
- Render/Railway: 15-20 minutes
- PythonAnywhere: 20-25 minutes
- AWS/Production: 1-2 hours
