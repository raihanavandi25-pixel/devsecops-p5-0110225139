"""Endpoint REST API Task Tracker."""
from flask import Blueprint, current_app, jsonify, request

from . import models
from .validators import validate_status, validate_task_id, validate_title

bp = Blueprint("tasks", __name__)


def _db():
    return current_app.config["DATABASE"]


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/tasks")
def get_tasks():
    status = request.args.get("status")
    if status and not validate_status(status):
        return jsonify({"error": "status tidak valid"}), 400
    return jsonify(models.list_tasks(_db(), status))


@bp.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not validate_title(title):
        return jsonify({"error": "title tidak valid"}), 400
    task_id = models.add_task(_db(), title.strip())
    return jsonify({"id": task_id, "title": title.strip(), "status": "todo"}), 201


@bp.patch("/tasks/<int:task_id>")
def change_status(task_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if not validate_task_id(task_id) or not validate_status(status):
        return jsonify({"error": "input tidak valid"}), 400
    if not models.update_status(_db(), task_id, status):
        return jsonify({"error": "task tidak ditemukan"}), 404
    return jsonify({"id": task_id, "status": status})


@bp.delete("/tasks/<int:task_id>")
def remove_task(task_id):
    if not models.delete_task(_db(), task_id):
        return jsonify({"error": "task tidak ditemukan"}), 404
    return "", 204
