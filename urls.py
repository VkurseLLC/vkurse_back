from flask import Blueprint, request, json, jsonify
from flask import Flask
from db import *

application = Flask(__name__)

@application.route("/")
def hello():
   return "<h1>Hello!</h1>"

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
        
@application.route('/filling_profile', methods=["GET", "POST"])
def url_filling_profile():

    if request.method == "POST":

        users_id = request.form["users_id"]
        username = request.form["username"]
        name_surname = request.form["name_surname"]
        d_birth = request.form["d_birth"]
        city = request.form["city"]
        photo = request.form["photo"]

        result = filling_profile(create_connection(), users_id, username, name_surname, d_birth, city, photo)

        if result[0] == 'successful':
            return jsonify({"answer": "successful"})
        
        elif result[0] == 'username_is_taken':
            return jsonify({"answer": "username_is_taken"})
        
        else:
            return jsonify({"answer": "error"})
        
@application.route('/add_about', methods=["GET", "POST"])
def url_add_about():

    if request.method == "POST":
        users_id = request.form["users_id"]
        about = request.form["about"]
        
        result = add_about(create_connection(), users_id, about)
        
        if result[0] == 'successful':
            return jsonify({"answer": "successful"})
        
        else:
            return jsonify({"answer": "error"})
        
@application.route('/city_selection', methods=["GET", "POST"])
def url_city_selection():

    if request.method == "GET":
        result = city_selection(create_connection())

        return jsonify({"answer": f"{result}"})
    
    else:
        return jsonify({"answer": "error"})

@application.route('/user_profile', methods=["GET", "POST"])
def url_user_profile():

    if request.method == "GET":
        users_id = request.form["users_id"]

        result = user_profile(create_connection(), users_id)

        return result
    
    else:
        return jsonify({"answer": "error"})

# @application.route('/save_photo', methods=["GET", "POST"])
# def url_take_photo():

#     if request.method == "GET":
        

