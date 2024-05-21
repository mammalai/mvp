import os
from datetime import timedelta

class TestConfig:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "2934948fn394fnqp4ifqp394fSRHF8EFH9WEFn9"
    JWT_SECRET_KEY = "super-secret"  # Change this!
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1) # you probably want to change this to a short time
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)