import os

from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory
)

from .routes import api_bp


# Создаём Flask-приложение
app = Flask(__name__)


# Подключаем API
app.register_blueprint(api_bp)


# Получаем путь к корню проекта.
# app.py находится в backend/,
# поэтому поднимаемся на одну папку выше.
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# =========================================================
# Frontend
# =========================================================

# Главная страница
@app.route("/")
def index_page():
    return send_from_directory(
        os.path.join(BASE_DIR, "html"),
        "index.html"
    )


# HTML-файлы
@app.route("/html/<path:filename>")
def serve_html(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "html"),
        filename
    )


# CSS-файлы
@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "css"),
        filename
    )


# JavaScript-файлы
@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "js"),
        filename
    )


# =========================================================
# Обработка ошибок API
# =========================================================

def api_error(message, status_code):
    """
    Формирует единый JSON-ответ для ошибки API.
    """

    return jsonify({
        "error": message
    }), status_code


# Ошибка 400
@app.errorhandler(400)
def handle_bad_request(error):
    if request.path.startswith("/api/"):
        return api_error(
            "Bad request",
            400
        )

    return error


# Ошибка 404
@app.errorhandler(404)
def handle_not_found(error):
    if request.path.startswith("/api/"):
        return api_error(
            "Resource not found",
            404
        )

    return error


# Ошибка 405
@app.errorhandler(405)
def handle_method_not_allowed(error):
    if request.path.startswith("/api/"):
        return api_error(
            "Method not allowed",
            405
        )

    return error


# Ошибка 500
@app.errorhandler(500)
def handle_internal_error(error):
    if request.path.startswith("/api/"):
        return api_error(
            "Internal server error",
            500
        )

    return error


# =========================================================
# Запуск приложения
# =========================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )