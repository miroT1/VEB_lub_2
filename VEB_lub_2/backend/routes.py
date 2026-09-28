from flask import Blueprint, jsonify, request

from . import service


# Создаём Blueprint для API.
# Все маршруты внутри него будут начинаться с /api
api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


# =========================================================
# Единый формат ошибки
# =========================================================

def error_response(message, status_code):
    return jsonify({
        "error": message
    }), status_code


# =========================================================
# GET /api/requests
# Получение списка студентов
#
# Примеры:
# /api/requests
# /api/requests?group=P3223
# /api/requests?dormitory=8
# /api/requests?group=P3223&dormitory=8
# =========================================================

@api_bp.route("/requests", methods=["GET"])
def get_requests():
    group = request.args.get("group")
    dormitory = request.args.get("dormitory")

    students = service.get_all_requests(
        group=group,
        dormitory=dormitory
    )

    return jsonify(students), 200


# =========================================================
# GET /api/requests/<student_id>
# Получение одного студента
# =========================================================

@api_bp.route("/requests/<student_id>", methods=["GET"])
def get_request(student_id):
    student = service.get_request_by_id(student_id)

    if student is None:
        return error_response(
            "Student not found",
            404
        )

    return jsonify(student), 200


# =========================================================
# POST /api/requests
# Создание студента
# =========================================================

@api_bp.route("/requests", methods=["POST"])
def post_request():
    data = request.get_json(silent=True)

    if data is None:
        return error_response(
            "Request body must contain valid JSON",
            400
        )

    result, error, code = service.create_request(data)

    if error is not None:
        return error_response(
            error,
            code
        )

    return jsonify(result), code


# =========================================================
# PATCH /api/requests/<student_id>
# Изменение студента
# =========================================================

@api_bp.route("/requests/<student_id>", methods=["PATCH"])
def patch_request(student_id):
    data = request.get_json(silent=True)

    if data is None:
        return error_response(
            "Request body must contain valid JSON",
            400
        )

    result, error, code = service.update_request(
        student_id,
        data
    )

    if error is not None:
        return error_response(
            error,
            code
        )

    return jsonify(result), code


# =========================================================
# DELETE /api/requests/<student_id>
# Удаление студента
# =========================================================

@api_bp.route("/requests/<student_id>", methods=["DELETE"])
def delete_request(student_id):
    success = service.delete_request(student_id)

    if not success:
        return error_response(
            "Student not found",
            404
        )

    return "", 204


# =========================================================
# QUERY /api/requests/<student_id>
# Обязательный QUERY-метод
# =========================================================

@api_bp.route("/requests/<student_id>", methods=["QUERY"])
def query_request(student_id):
    student = service.get_request_by_id(student_id)

    if student is None:
        return error_response(
            "Student not found",
            404
        )

    return jsonify(student), 200