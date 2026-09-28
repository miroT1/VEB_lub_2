import json
from pathlib import Path


# Корень проекта.
# storage.py находится в:
# project/backend/storage.py
#
# Поэтому parent -> backend
# parent.parent -> корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent


# Файл с данными студентов
FILE_PATH = BASE_DIR / "students.json"


def load_data():
    """
    Загружает список студентов из students.json.

    Если файла нет или JSON повреждён,
    возвращается пустой список.
    """

    if not FILE_PATH.exists():
        return []


    try:
        with FILE_PATH.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


    # В файле должен находиться именно список студентов
    if not isinstance(data, list):
        return []


    return data


def save_data(data):
    """
    Сохраняет список студентов в students.json.
    """

    with FILE_PATH.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )