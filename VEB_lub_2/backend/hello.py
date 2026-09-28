# from flask import Flask, jsonify

# app = Flask(__name__)

# # 1. Настройка для главной страницы ВК (просто корень сайта)
# @app.route("/")
# def vk_main_page():
#     return "Привет! Это главная страница ВКонтакте. Пожалуйста, войдите в аккаунт."

# # 2. Настройка для страницы сообщений
# @app.route("/im")
# def vk_messages():
#     return "Тут отображаются ваши личные сообщения (диалоги)."

# # 3. А ВОТ ТАК НАСТРОЕН ТОТ САМЫЙ FEED, о котором мы говорили:
# @app.route("/feed", methods=["GET"])
# def vk_news_feed():
#     # Здесь в реальной жизни сервер лезет в базу данных и достает посты друзей.
#     # Но для примера мы просто вернем список постов в формате JSON.
#     news = [
#         {"author": "Дуров", "text": "Вернул стену!"},
#         {"author": "Паблик с мемами", "text": "Кот смотрит на Flask-сервер"}
#     ]
#     return jsonify(news)

# if __name__ == "__main__":
#     app.run(port=5000)


from flask import Flask, request, jsonify

app = Flask(__name__)

# Имитируем базу данных в памяти — просто список словарей
STUDENTS = [
    {"isu_id": 111, "name": "Алексей", "group": "M3301"},
    {"isu_id": 222, "name": "Мария", "group": "M3302"}
]

# Маршрут, который использует request.args (Query-параметры) и jsonify
@app.route("/search")
def search_student():
    # 1. Ловим параметр 'group' из ссылки. Если его нет, вернется None
    target_group = request.args.get("group")
    
    if not target_group:
        return jsonify({"error": "Передайте параметр group, например: /search?group=M3301"}), 400

    # 2. Фильтруем наш список обычным циклом Python
    filtered = []
    for s in STUDENTS:
        if s["group"] == target_group:
            filtered.append(s)
            
    # 3. Возвращаем отфильтрованный список в формате JSON
    return jsonify(filtered), 200

if __name__ == "__main__":
    app.run(debug=True)
