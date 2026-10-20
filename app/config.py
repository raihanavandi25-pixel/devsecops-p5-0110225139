"""Konfigurasi aplikasi. Nilai sensitif dibaca dari environment variable."""
import os


class Config:
    DATABASE = os.environ.get("TASKTRACKER_DB", "tasks.db")
    MAX_TITLE_LENGTH = 100
    ALLOWED_STATUS = ("todo", "doing", "done")


class TestConfig(Config):
    DATABASE = ":memory:"
    TESTING = True
