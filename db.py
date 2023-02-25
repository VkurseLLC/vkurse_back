import mysql.connector
from mysql.connector import Error
from bot_config import *


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
        

def save_phone_number(connection, phome_number_value):
    with connection.cursor() as cursor:
        try:
            code = 12345
            cursor.executemany("INSERT INTO `phone_number_verification_codes` (`id`, `phone_number`, `verification_code`, `dt_create`) VALUES (NULL, %s, %s, NOW())", [(str(phome_number_value), str(code))])
            # connection.commit()
            return 'successful'
        
        except Error as e:
            print(f"Произошла ошибка сheck_user_block'{e}'")
            bot.send_message(chat_id, f"Произошла ошибка в create_connection'{e}'")
            return e