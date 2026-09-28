import re
import uuid
from datetime import date

from . import storage


# Поля, которые обязательно должны присутствовать
REQUIRED_FIELDS = (
    "fullName",
    "group",
    "ISU",
)


def validate_student(data):
    """
    Проверяет корректность данных студента.

    Возвращает:
        None, если данные корректные;
        строку с описанием ошибки, если данные некорректные.
    """

    # Проверяем, что пришёл объект
    if not isinstance(data, dict):
        return "Request body must be a JSON object"


    # Проверяем наличие обязательных полей
    for field in REQUIRED_FIELDS:
        if field not in data:
            return f"Missing required field: {field}"


    # -----------------------------------------------------
    # Проверка ФИО
    # -----------------------------------------------------

    full_name = data["fullName"]

    if not isinstance(full_name, str):
        return "fullName must be a string"

    full_name = full_name.strip()
    names = full_name.split()

    if len(names) < 2:
        return "fullName must contain at least two words"

    if any(len(word) < 2 for word in names):
        return "Each word in fullName must contain at least two characters"


    # -----------------------------------------------------
    # Проверка группы
    # -----------------------------------------------------

    group = data["group"]

    if not isinstance(group, str):
        return "group must be a string"

    if not re.fullmatch(r"[A-Za-z]\d{4}", group):
        return "group must have format like P3223"


    # -----------------------------------------------------
    # Проверка ИСУ
    # -----------------------------------------------------

    isu = data["ISU"]

    if not isinstance(isu, str):
        return "ISU must be a string"

    if not re.fullmatch(r"\d{6}", isu):
        return "ISU must contain exactly 6 digits"


    # -----------------------------------------------------
    # Проверка номера общежития
    # -----------------------------------------------------

    dorm_number = data.get("dormNumber")

    if dorm_number is not None:
        if isinstance(dorm_number, bool) or not isinstance(dorm_number, int):
            return "dormNumber must be an integer"

        if dorm_number < 1:
            return "dormNumber must be greater than 0"


    # -----------------------------------------------------
    # Проверка номера комнаты
    # -----------------------------------------------------

    room = data.get("room")

    if room is not None:
        if isinstance(room, bool) or not isinstance(room, int):
            return "room must be an integer"

        if room < 1:
            return "room must be greater than 0"


    # -----------------------------------------------------
    # Проверка даты заселения
    # -----------------------------------------------------

    date_arrived = data.get("dateArrived")

    if date_arrived not in (None, ""):
        if not isinstance(date_arrived, str):
            return "dateArrived must be a string"

        try:
            date.fromisoformat(date_arrived)
        except ValueError:
            return "dateArrived must have format YYYY-MM-DD"


    # -----------------------------------------------------
    # Проверка isForeign
    # -----------------------------------------------------

    is_foreign = data.get("isForeign", False)

    if not isinstance(is_foreign, bool):
        return "isForeign must be boolean"


    # -----------------------------------------------------
    # Проверка notes
    # -----------------------------------------------------

    notes = data.get("notes", "")

    if not isinstance(notes, str):
        return "notes must be a string"


    return None


# =========================================================
# GET
# Получение списка студентов с фильтрацией
# =========================================================

def get_all_requests(group=None, dormitory=None):
    students = storage.load_data()


    # Фильтр по группе

    if group is not None:
        students = [
            student
            for student in students
            if student.get("group") == group
        ]


    # Фильтр по общежитию

    if dormitory is not None:
        students = [
            student
            for student in students
            if str(student.get("dormNumber")) == str(dormitory)
        ]


    return students


# =========================================================
# GET
# Получение одного студента по ID
# =========================================================

def get_request_by_id(student_id):
    students = storage.load_data()

    for student in students:
        if student.get("ID") == student_id:
            return student

    return None


# =========================================================
# POST
# Создание студента
# =========================================================

def create_request(data):
    # Проверяем входные данные

    error = validate_student(data)

    if error is not None:
        return None, error, 422


    students = storage.load_data()


    # Проверяем уникальность ИСУ

    if any(student.get("ISU") == data["ISU"] for student in students):
        return None, "Student with this ISU already exists", 409


    # Создаём новый объект, чтобы не изменять
    # исходный словарь запроса напрямую

    student = {
        "ID": str(uuid.uuid4()),
        "fullName": data["fullName"].strip(),
        "group": data["group"].strip(),
        "ISU": data["ISU"],
        "dormNumber": data.get("dormNumber"),
        "room": data.get("room"),
        "dateArrived": data.get("dateArrived"),
        "isForeign": data.get("isForeign", False),
        "notes": data.get("notes", "")
    }


    # Нормализация ФИО

    names = student["fullName"].split()

    student["fullName"] = " ".join(
        word.capitalize()
        for word in names
    )


    # Нормализация группы

    student["group"] = (
        student["group"][0].upper()
        + student["group"][1:]
    )


    # Если общежитие не указано,
    # комната и дата заселения тоже должны быть пустыми

    if student["dormNumber"] is None:
        student["room"] = None
        student["dateArrived"] = None


    # Если дата заселения не указана,
    # комната также не используется

    if student["dateArrived"] in (None, ""):
        student["dateArrived"] = None
        student["room"] = None


    students.append(student)

    storage.save_data(students)

    return student, None, 201


# =========================================================
# PATCH
# Изменение существующего студента
# =========================================================

def update_request(student_id, data):
    # Проверяем, что пришёл объект JSON

    if not isinstance(data, dict):
        return None, "Request body must be a JSON object", 400


    students = storage.load_data()


    # Ищем студента

    student_index = -1

    for index, student in enumerate(students):
        if student.get("ID") == student_id:
            student_index = index
            break


    # Если студент не найден

    if student_index == -1:
        return None, "Student not found", 404


    current_student = students[student_index]


    # ID нельзя изменить через PATCH

    if "ID" in data and data["ID"] != student_id:
        return None, "ID cannot be changed", 400


    # Создаём копию существующего студента
    # и применяем переданные изменения

    updated_student = current_student.copy()

    data = data.copy()
    data.pop("ID", None)

    updated_student.update(data)


    # Проверяем итоговый объект целиком

    error = validate_student(updated_student)

    if error is not None:
        return None, error, 422


    # Проверяем уникальность ИСУ

    if any(
        student.get("ISU") == updated_student["ISU"]
        and student.get("ID") != student_id
        for student in students
    ):
        return None, "Student with this ISU already exists", 409


    # Нормализация ФИО

    updated_student["fullName"] = " ".join(
        word.capitalize()
        for word in updated_student["fullName"].strip().split()
    )


    # Нормализация группы

    updated_student["group"] = (
        updated_student["group"][0].upper()
        + updated_student["group"][1:]
    )


    # Связь общежития, комнаты и даты

    if updated_student["dormNumber"] is None:
        updated_student["room"] = None
        updated_student["dateArrived"] = None

    if updated_student["dateArrived"] in (None, ""):
        updated_student["dateArrived"] = None
        updated_student["room"] = None


    students[student_index] = updated_student

    storage.save_data(students)

    return updated_student, None, 200


# =========================================================
# DELETE
# Удаление студента
# =========================================================

def delete_request(student_id):
    students = storage.load_data()


    # Ищем студента

    student_index = -1

    for index, student in enumerate(students):
        if student.get("ID") == student_id:
            student_index = index
            break


    # Студент не найден

    if student_index == -1:
        return False


    # Удаляем найденного студента

    students.pop(student_index)

    storage.save_data(students)

    return True