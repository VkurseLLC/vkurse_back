import mysql.connector
from mysql.connector import Error
from bot_config import *
import hashlib

# create_connection
def create_connection():
    connection = None

    try:
        connection = mysql.connector.connect(
            host = '95.163.241.100',
            port = 3306,
            user = 'super_user', 
            password = '****9963AAdd',
            database = 'vkurse_database')

        print("Подключение к базе данных MySQL прошло успешно")
        return connection

    except Error as e:
        print(f"Произошла ошибка в create_connection'{e}'")
        bot.send_message(chat_id, f"Произошла ошибка в create_connection'{e}'")
        return connection

def сheck(connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT `phone_number` FROM `phone_number_verification_codes` WHERE `id` = 1")
            result = cursor.fetchall()

            if len(result) != 0:
                return result[0][0]
            else:
                return 'Noresult'
        
        except Error as e:
            print(f"Произошла ошибка сheck_user_block'{e}'")
            bot.send_message(chat_id, f"Произошла ошибка сheck_user_block'{e}'")
            return e
        
def user_authorisation(connection, phome_number_value, verification_code_value):
    with connection.cursor() as cursor:
        try:
            phome_number_value  = (hashlib.sha256(repr(phome_number_value).encode())).hexdigest()
            verification_code_value  = (hashlib.sha256(repr(verification_code_value).encode())).hexdigest()

            cursor.execute("SELECT `id` FROM `phone_number_verification_codes` WHERE `phone_number` = %s AND verification_code = %s", (str(phome_number_value), str(verification_code_value)))
            result = cursor.fetchall()

            if len(result) != 0: 

                cursor.execute("SELECT `id` FROM `users` WHERE `phone_number` = %s", (str(phome_number_value),))
                result = cursor.fetchall()

                if len(result) != 0:
                    return ['successful', result[0][0]]
                
                else:
                    cursor.executemany("INSERT INTO users (id, phone_number, dt_reg) VALUES (NULL, %s, NOW())", [(str(phome_number_value), )])
                    connection.commit()

                    cursor.execute("SELECT `id` FROM `users` WHERE `phone_number` = %s", (str(phome_number_value),))
                    result = cursor.fetchall()

                    return ['successful', result[0][0]]

            else:
                return ['verification_code_not_found']
        
        except Error as e:
            print(f"Произошла ошибка сheck_user_block'{e}'")
            bot.send_message(chat_id, f"Произошла ошибка в check_auth\n\n{e}")
            return ['error']


