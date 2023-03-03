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
                            "user_id": result[1]})
        
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
        first_name = request.form["first_name"]
        d_birth = request.form["d_birth"]
        city = request.form["city"]

        result = filling_profile(create_connection(), users_id, username, first_name, d_birth, city)

        if result[0] == 'successful':
            return jsonify({"answer": "successful"})
        
        elif result[0] == 'username_is_taken':
            return jsonify({"answer": "username_is_taken"})
        
        else:
            return jsonify({"answer": "error"})
        


