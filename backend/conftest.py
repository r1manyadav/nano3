import pytest
import os
import sys

# Set environment BEFORE importing app
os.environ['FLASK_ENV'] = 'testing'
# Force in-memory database for tests via DATABASE_URL env var
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'


@pytest.fixture(scope="function")
def app():
    """Create and configure a test app."""
    from app import app as _app, db
    
    # Configure for in-memory database
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    _app.config['TESTING'] = True
    
    with _app.app_context():
        # Dispose of any existing engine connections
        db.engine.dispose()
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's CLI."""
    return app.test_cli_runner()
