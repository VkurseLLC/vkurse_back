from flask import Blueprint, request, json, jsonify
from flask import Flask
from db import *

application = Flask(__name__)


@application.route("/")
def hello():
   return "<h1>Hello!</h1>"

@application.route('/authorisation', methods=["GET", "POST"])
def sendphonenumber():

    if request.method =="POST":

        phone_number = request.form["phone_number"]
        verification_code = request.form["verification_code"]

        connection = create_connection()

        result = user_authorisation(connection, phone_number, verification_code)

        if result[0] == 'successful':
            
            return jsonify({"answer": "successful", 
                            "user_id": result[1]})
        
        elif result[0] == 'verification_code_not_found':
            return jsonify({"answer": "verification_code_not_found"})
        
        else:
            return jsonify({"answer": "error"})