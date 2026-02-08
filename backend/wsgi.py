"""
WSGI entry point for production servers (Gunicorn, uWSGI, etc.)
Used by: gunicorn wsgi:app
"""

from app import app

if __name__ == '__main__':
    # This will be called by Gunicorn, not directly
    app.run()
