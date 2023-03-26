from flask import Blueprint, request, json, jsonify
from flask import Flask
from db import *

application = Flask(__name__)

@application.route("/")
def hello():
   return "<h1>Hello!</h1>"

# Авторизация пользователя
@application.route('/authorisation', methods=["GET", "POST"])
def url_authorisation():

    if request.method =="POST":

        phone_number = request.form["phone_number"]
        verification_code = request.form["verification_code"]

        result = user_authorisation(create_connection(), phone_number, verification_code)

        if result[0] == 'successful':
            
            return jsonify({"answer": "successful", 
                            "user_id": result[1],
                            "user_account_status" : result[2]})
        
        elif result[0] == 'verification_code_not_found':
            return jsonify({"answer": "verification_code_not_found"})
        
        else:
            return jsonify({"answer": "error"})
        
# Проверка username
@application.route('/check_username_availability', methods=["GET", "POST"])
def url_check_username_availability():

    if request.method =="POST":

        username = request.form["username"]

        result = check_username_availability(create_connection(), username)

        if result[0] == "True":
            return jsonify({"answer": "successful",
                            "username": "True"})
        
        elif result[0] == "False":
            return jsonify({"answer": "successful",
                            "username": "False"})
        
        else:
            return jsonify({"answer": "error"})
        
# Выбор города        
@application.route('/city_selection', methods=["GET", "POST"])
def url_city_selection():

    if request.method == "GET":
        result = city_selection(create_connection())

        return result 
    
    else:
        return jsonify({"answer": "error"})        

# Заполнение профиля данными пользователя
@application.route('/api/user_profile/filling_profile', methods=["GET", "POST"])
def url_filling_profile():

    if request.method == "POST":

        users_id = request.form["users_id"]
        username = request.form["username"]
        name_surname = request.form["name_surname"]
        d_birth = request.form["d_birth"]
        city = request.form["city"]
        

        result = filling_profile(create_connection(), users_id, username, name_surname, d_birth, city)

        if result[0] == 'successful':
            return jsonify({"answer": "successful"})
        
        elif result[0] == 'username_is_taken':
            return jsonify({"answer": "username_is_taken"})
        
        else:
            return jsonify({"answer": "error"})
        
# Добавление данных из поля "Обо мне"        
@application.route('/api/user_profile/add_about', methods=["GET", "POST"])
def url_add_about():

    if request.method == "POST":
        users_id = request.form["users_id"]
        about = request.form["about"]
        
        result = add_about(create_connection(), users_id, about)
        
        if result[0] == 'successful':
            return jsonify({"answer": "successful"})
        
        else:
            return jsonify({"answer": "error"})

# Вывод данных пользователя на экран профиля
@application.route('/api/user_profile/show_profile', methods=["GET", "POST"])
def url_show_profile():

    if request.method == "POST":
        users_id = request.form["users_id"]

        result = user_profile(create_connection(), users_id)

        return result
    
    else:
        return jsonify({"answer": "error"})
    
# Сохранение фото
@application.route('/api/user_profile/image/add_image', methods=["GET", "POST"])
def url_add_image():

    if request.method == "POST":

        users_id = request.form["users_id"]
        bin_photo = request.form["photo"]

        result = add_image(create_connection(), users_id, bin_photo)

        if result[0] == 'successful':
            return jsonify({"answer": "image_was_upload"})

        else:
            return jsonify({"answer": "error"})

# Удаление фото
@application.route('/api/user_profile/image/delete_image', methods=["GET", "POST"])
def url_delete_image():

    if request.method == "POST":

        users_id = request.form["users_id"]

        result = delete_image(create_connection(), users_id)

        if result[0] == 'successful':
            return jsonify({"answer": "image_was_deleted"})

        else:
            return jsonify({"answer": "error"})

# Отправка геолокации
@application.route('/api/save/location', methods=["GET", "POST"])
def url_save_users_location():
    
    if request.method == "POST":
        user_id = request.form["user_id"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        result = save_user_location(create_connection(), user_id, latitude, longitude)

        return result

    else:
        return jsonify({"answer": "error"})

# Получение геолокации других пользователей
@application.route('/api/stream/location', methods=["GET", "POST"])
def url_stream_users_location():

    if request.method == "POST":
        user_id = request.form["user_id"]

        result = get_users_location(create_connection(), user_id)
        return jsonify({"answer": "successful",
                        "locations_data": result})

    else:
        return jsonify({"answer": "error"})

# Сoхранение геометки
@application.route('/api/user_profile/image/save_geometca', methods=["GET", "POST"])
def url_save_geometca():

    if request.method == "POST":
        users_id = request.form["users_id"]

        result = save_icon_geometca(create_connection(), users_id)

        if result[0] == 'metca_was_saved':
            return jsonify({"answer": f"{result[0]}"}) 

        else:
            return jsonify({"answer": "error"})
        
# Полечение геометки
@application.route('/api/user_profile/image/get_geometca', methods=["GET", "POST"])
def url_get_geometca():

    if request.method == "POST":
        users_id = request.form["users_id"]

        result = get_geometca(create_connection(), users_id)

        if len(result) != 0:
            return jsonify ({"answer": f"{result}"})

        else:
            return jsonify({"answer": "error"})