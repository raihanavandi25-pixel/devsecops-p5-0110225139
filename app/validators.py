"""Fungsi validasi input pengguna."""
from .config import Config


def validate_title(title):
    """Judul harus berupa string tidak kosong dan maksimal MAX_TITLE_LENGTH."""
    if not isinstance(title, str):
        return False
    title = title.strip()
    return 0 < len(title) <= Config.MAX_TITLE_LENGTH


def validate_status(status):
    """Status harus salah satu dari ALLOWED_STATUS."""
    return status in Config.ALLOWED_STATUS


def validate_task_id(task_id):
    """ID harus bilangan bulat positif."""
    return isinstance(task_id, int) and task_id > 0
