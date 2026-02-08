#!/bin/bash
# Production Deployment Script for Linux/Unix Servers

set -e  # Exit on error

echo "======================================"
echo "Nano Test Platform - Production Deploy"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/var/www/nano_test_platform"
VENV_DIR="/var/www/nano_test_platform/venv"
LOG_DIR="/var/log/nano_test_platform"
APP_USER="www-data"

# Step 1: Check environment
echo -e "\n${YELLOW}[1/8] Checking Prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 not found${NC}"
    exit 1
fi
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Prerequisites OK${NC}"

# Step 2: Create directories
echo -e "\n${YELLOW}[2/8] Creating Directories...${NC}"
mkdir -p "$APP_DIR" "$VENV_DIR" "$LOG_DIR"
mkdir -p "$APP_DIR/instance"
mkdir -p "$APP_DIR/uploads"
echo -e "${GREEN}✓ Directories created${NC}"

# Step 3: Create virtual environment
echo -e "\n${YELLOW}[3/8] Creating Virtual Environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
echo -e "${GREEN}✓ Virtual environment ready${NC}"

# Step 4: Install dependencies
echo -e "\n${YELLOW}[4/8] Installing Dependencies...${NC}"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip setuptools wheel
pip install -r "$APP_DIR/requirements.txt"
pip install gunicorn
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 5: Set permissions
echo -e "\n${YELLOW}[5/8] Setting Permissions...${NC}"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"
chown -R "$APP_USER:$APP_USER" "$LOG_DIR"
chmod 755 "$APP_DIR"
chmod 755 "$LOG_DIR"
echo -e "${GREEN}✓ Permissions set${NC}"

# Step 6: Initialize database
echo -e "\n${YELLOW}[6/8] Initializing Database...${NC}"
cd "$APP_DIR"
python3 << EOF
from app import app, db
from models import Teacher
with app.app_context():
    db.create_all()
    # Create default teacher if not exists
    if not Teacher.query.filter_by(teacher_id='admin').first():
        teacher = Teacher(teacher_id='admin', name='Administrator')
        teacher.set_password('change_this_password')
        db.session.add(teacher)
        db.session.commit()
        print("✓ Default admin account created")
    else:
        print("✓ Database tables exist")
EOF
echo -e "${GREEN}✓ Database initialized${NC}"

# Step 7: Start application
echo -e "\n${YELLOW}[7/8] Starting Application...${NC}"
cd "$APP_DIR"
source "$VENV_DIR/bin/activate"

# Create systemd service file
sudo tee /etc/systemd/system/nano_test_platform.service > /dev/null <<EOF
[Unit]
Description=Nano Test Platform
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --workers 4 --worker-class sync --bind 0.0.0.0:5000 --access-logfile $LOG_DIR/access.log --error-logfile $LOG_DIR/error.log wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable nano_test_platform
sudo systemctl start nano_test_platform
echo -e "${GREEN}✓ Application started${NC}"

# Step 8: Verify deployment
echo -e "\n${YELLOW}[8/8] Verifying Deployment...${NC}"
sleep 2
if curl -s http://localhost:5000/api/health | grep -q "OK"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "Check logs: sudo journalctl -u nano_test_platform -n 50"
    exit 1
fi

echo -e "\n${GREEN}======================================"
echo -e "Deployment Complete!"
echo -e "======================================${NC}"
echo ""
echo "Application Info:"
echo "  URL: http://your-domain.com"
echo "  Service: nano_test_platform (systemd)"
echo "  Logs: $LOG_DIR/"
echo ""
echo "Useful Commands:"
echo "  View logs: sudo journalctl -u nano_test_platform -f"
echo "  Restart: sudo systemctl restart nano_test_platform"
echo "  Stop: sudo systemctl stop nano_test_platform"
echo "  Status: sudo systemctl status nano_test_platform"
echo ""
