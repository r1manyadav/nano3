# ENVIRONMENT_SETUP.md - Setup Your .env File

This guide explains how to set up your environment variables (.env file) for deployment.

---

## 📝 Step 1: Create .env File

### Option A: From Command Line

**Windows (PowerShell):**
```powershell
cd c:\Users\raman\Desktop\nano3\nano3
copy .env.example .env
notepad .env
```

**Linux/Mac:**
```bash
cd ~/nano3
cp .env.example .env
nano .env
```

### Option B: Manual Copy
1. Open `.env.example` in your editor
2. Save it as `.env` in the same directory
3. Edit and fill in the values

---

## 🔑 Environment Variables Explained

### Basic Configuration

```env
# Application Mode
FLASK_ENV=production          # Keep as 'production' for live site
FLASK_DEBUG=False             # Always False in production
PORT=5000                     # Port your app runs on
```

### Database Configuration

**For SQLite (Testing only):**
```env
DATABASE_URL=sqlite:///nano_test_platform.db
```

**For PostgreSQL (Production - RECOMMENDED):**
```env
DATABASE_URL=postgresql://nano_user:your_password@localhost:5432/nano_test_platform
```

**For PostgreSQL with Docker:**
```env
DATABASE_URL=postgresql://nano_user:your_password@postgres:5432/nano_test_platform
```

**For PostgreSQL on Remote Server:**
```env
DATABASE_URL=postgresql://nano_user:your_password@your-db-host.com:5432/nano_test_platform
```

### Security Keys

Generate random secure keys:

```python
# Run this in Python
import secrets
print(secrets.token_hex(32))
```

Then copy the output to these variables:

```env
JWT_SECRET_KEY=abc123def456ghi789jkl012mno345pqr
SECRET_KEY=xyz789abc456def123ghi012jkl345mno
```

### CORS Settings (Frontend Access)

```env
# Development (local testing)
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:8000

# Production (your domain)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### File Upload Settings (Optional)

```env
MAX_CONTENT_LENGTH=50    # Max upload size in MB
```

---

## 🚀 Complete .env Examples

### Example 1: LOCAL DEVELOPMENT (SQLite)

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

DATABASE_URL=sqlite:///nano_test_platform.db

JWT_SECRET_KEY=dev-key-12345678901234567890123456
SECRET_KEY=dev-secret-12345678901234567890123456

CORS_ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:8000

MAX_CONTENT_LENGTH=50
```

### Example 2: LOCAL WITH POSTGRESQL

```env
FLASK_ENV=development
FLASK_DEBUG=False
PORT=5000

DATABASE_URL=postgresql://nano_user:nano_password@localhost:5432/nano_test_platform

JWT_SECRET_KEY=local-prod-key-1234567890123456789012
SECRET_KEY=local-prod-secret-123456789012345678901

CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000

MAX_CONTENT_LENGTH=50
```

### Example 3: DOCKER COMPOSE

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000

# Important: Use 'postgres' (service name in docker-compose) instead of localhost
DATABASE_URL=postgresql://nano_user:change_this_password_123@postgres:5432/nano_test_platform

JWT_SECRET_KEY=docker-jwt-key-1234567890123456789012
SECRET_KEY=docker-secret-key-123456789012345678901

CORS_ORIGINS=http://localhost,http://127.0.0.1

MAX_CONTENT_LENGTH=50
```

### Example 4: PRODUCTION SERVER

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000

# PostgreSQL connection on same server
DATABASE_URL=postgresql://nano_user:your_strong_password@localhost:5432/nano_test_platform

# Generate truly random keys!
JWT_SECRET_KEY=generate-random-32-char-hex-string-here
SECRET_KEY=generate-random-32-char-hex-string-here

# Your actual domain
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

MAX_CONTENT_LENGTH=50
```

### Example 5: RENDER.COM DEPLOYMENT

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=10000

# Render provides DATABASE_URL automatically
# Don't set it manually - Render will override it

JWT_SECRET_KEY=generate-random-secure-key-here
SECRET_KEY=generate-random-secure-key-here

CORS_ORIGINS=https://yourdomain.com,https://nano-test-platform.onrender.com

MAX_CONTENT_LENGTH=50
```

---

## 🔒 Security Best Practices

### DO:
- ✅ Use strong, random keys (32+ characters)
- ✅ Use HTTPS only in production (CORS_ORIGINS with https://)
- ✅ Use strong database passwords
- ✅ Keep .env file private (in .gitignore)
- ✅ Use secure connection to database server
- ✅ Different .env for each environment (dev/prod)

### DON'T:
- ❌ Use default/simple passwords
- ❌ Commit .env to git
- ❌ Share .env files via email/chat
- ❌ Use localhost in production URLs
- ❌ Use same keys across environments
- ❌ Hardcode credentials in code

---

## 🗄️ PostgreSQL Connection Details

### Create PostgreSQL Database

```sql
-- As PostgreSQL admin user
CREATE USER nano_user WITH PASSWORD 'your_strong_password';
CREATE DATABASE nano_test_platform OWNER nano_user;
```

### Connection String Format

```
postgresql://username:password@host:port/database_name
```

**Examples:**
```
postgresql://nano_user:mypassword@localhost:5432/nano_test_platform
postgresql://nano_user:mypassword@db.example.com:5432/nano_test_platform
postgresql://nano_user:mypassword@postgres:5432/nano_test_platform  # Docker
```

### Common Connection Issues

| Issue | Solution |
|-------|----------|
| "Connection refused" | Check database is running |
| "Authentication failed" | Verify username/password |
| "Database does not exist" | Create database first |
| "Name or service not known" | Check host/port |

---

## 🧪 Verify Your .env

After creating .env, test the connection:

```bash
# For SQLite (automatic, no test needed)

# For PostgreSQL
psql -U nano_user -d nano_test_platform -h localhost -c "SELECT 1"
# Should return: 1 (success)
```

---

## 📋 .env File Checklist

Before deployment, verify:

- [ ] .env file exists in project root
- [ ] DATABASE_URL is set correctly
- [ ] JWT_SECRET_KEY has 32+ random characters
- [ ] SECRET_KEY has 32+ random characters
- [ ] CORS_ORIGINS matches your domain
- [ ] FLASK_ENV is "production"
- [ ] FLASK_DEBUG is False
- [ ] .env is in .gitignore (don't commit)
- [ ] Password is secure (not simple)
- [ ] All required variables are set

---

## 🆘 Common Configuration Issues

### Issue: "Module not found" or "Import error"
```
Solution: Make sure all packages in requirements.txt are installed
pip install -r backend/requirements.txt
```

### Issue: "Database connection error"
```
Check:
1. DATABASE_URL is correct
2. PostgreSQL is running
3. Password is correct
4. Network/firewall allows connection
```

### Issue: "CORS error in browser"
```
Solution: Update CORS_ORIGINS to match your frontend URL
CORS_ORIGINS=https://yourdomain.com
Restart app after change
```

### Issue: "403 Forbidden" when uploading files
```
Solution: Check file upload size
MAX_CONTENT_LENGTH=50  # Increase if needed
```

---

## 🎯 Next Steps

1. ✅ Create .env file from .env.example
2. ✅ Fill in all required variables
3. ✅ Test database connection
4. ✅ Test locally if possible
5. ✅ Deploy with confidence!

---

## 📞 Quick Reference

**Generate secure key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Test PostgreSQL connection:**
```bash
psql postgresql://user:password@host:5432/dbname -c "SELECT 1"
```

**View current .env:**
```bash
cat backend/.env  # Or open in editor
```

**Don't forget:**
- `.env` should NOT be committed to git
- Different environments need different `.env` files
- Keep backups of your `.env` credentials
- Update CORS_ORIGINS when getting your domain

---

Now that .env is ready, see **QUICK_START_DEPLOY.md** to deploy! 🚀
