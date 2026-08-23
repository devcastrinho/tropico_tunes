from app import create_app
from app.extensions import db
from config import TestConfig


def test_home_loads():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        response = app.test_client().get("/")
        assert response.status_code == 200
        assert b"TR\xc3\x93PICO" in response.data


def test_admin_requires_login():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        response = app.test_client().get("/admin")
        assert response.status_code == 302
        assert "/login" in response.location

