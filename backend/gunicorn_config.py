# Gunicorn Configuration for Production
# Usage: gunicorn -c gunicorn_config.py wsgi:app

import multiprocessing
import os

# Server Socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1  # Formula: (2 * CPU) + 1
worker_class = "sync"  # For CPU-bound: use "sync", for I/O-bound: use "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stdout
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process Naming
proc_name = "nano_test_platform"

# Server Mechanics
daemon = False
pidfile = "/var/run/nano_test_platform.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (set these if using HTTPS directly with Gunicorn)
keyfile = None
certfile = None
ssl_version = None

# Application
pythonpath = None
raw_env = []

# Server Hooks
def on_starting(server):
    print("Nano Test Platform Server Starting...")

def when_ready(server):
    print("Nano Test Platform Server Ready!")
    print(f"Listening on http://0.0.0.0:5000")
    print(f"Workers: {server.num_workers}")

def on_exit(server):
    print("Nano Test Platform Server Shutting Down...")
