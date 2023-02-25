from flask import Blueprint, request, json, jsonify
from flask import Flask
from db import *

application = Flask(__name__)

# 
@application.route("/")
def hello():
   return "<h1>Hello!</h1>"

@application.route('/sendphonenumber', methods=["GET", "POST"])
def sendphonenumber():

    if request.method =="POST":

        phone_number = request.form["phone_number"]

        result = save_phone_number(create_connection(), phone_number)

        if result == 'successful':
            return jsonify(["successful"])