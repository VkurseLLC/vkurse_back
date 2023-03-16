import mysql.connector
from mysql.connector import Error
from bot_config import *
import hashlib
from encode_decode import *
import datetime
from datetime import date
from function_holder import *

# ---------------------------------------------------------------------------------- #

def create_connection():
    connection = None

    try:
        connection = mysql.connector.connect(
            host = '80.78.240.205',
            port = 13306,
            user = 'vkurse_editor', 
            password = 'T6XBwtgQ',
            database = 'vkurse_db')

        return connection

    except Error as e:
        print(f"Произошла ошибка в create_connection'{e}'")
        bot.send_message(chat_id, f"Произошла ошибка в create_connection\n\n{e}")
        return connection

# ---------------------------------------------------------------------------------- #

def user_authorisation(connection, phone_number_value, verification_code_value):
    with connection.cursor() as cursor:
        try:

            phone_number_value = phone_number_value.replace('+','')
            phone_number_value = phone_number_value.replace('(','')
            phone_number_value = phone_number_value.replace(')','')
            phone_number_value = phone_number_value.replace('-','')
            phone_number_value = phone_number_value.replace(' ','')

            phone_number_value  = (hashlib.sha256(repr(phone_number_value).encode())).hexdigest()
            phone_number_value_encode = encrypt(repr(phone_number_value), crypto_key)
            verification_code_value  = (hashlib.sha256(repr(int(verification_code_value)).encode())).hexdigest()

            cursor.execute("SELECT `id` FROM `phone_number_verification_codes` WHERE `phone_number` = %s AND verification_code = %s AND TIMEDIFF (NOW(), `dt_create`) <= '00:03:00' AND `used` = 0",
                            (str(phone_number_value), str(verification_code_value)))
            result = cursor.fetchall()
            print(f'result: {result}')
            
            if len(result) != 0: 

                cursor.execute("UPDATE `phone_number_verification_codes` SET `used` = 1 WHERE `id` = %s", (str(result[0][0]),))
                connection.commit()

                cursor.execute("SELECT `id` FROM `users` WHERE `phone_number` = %s", (str(phone_number_value),))
                result = cursor.fetchall()

                if len(result) != 0:
                    
                    cursor.execute("SELECT `id` FROM `users_account_data` WHERE `users_id` = %s", (int(result[0][0]),))
                    user_account_status = cursor.fetchall()

                    if len(user_account_status) != 0:
                        return ['successful', result[0][0], 'old_user']
                    
                    else:
                        return ['successful', result[0][0], 'new_user']
                
                else:
                    cursor.executemany("INSERT INTO users (id, phone_number, dt_reg) VALUES (NULL, %s, NOW())", [(str(phone_number_value), )])
                    connection.commit()

                    cursor.executemany("INSERT INTO `users_phone_number` (id, users_id, user_phone_number, dt_upd) VALUES (NULL, %s, %s, NOW())", [(int(result[0][0]), str(phone_number_value_encode))])

                    cursor.execute("SELECT `id` FROM `users` WHERE `phone_number` = %s", (str(phone_number_value),))
                    result = cursor.fetchall()

                    cursor.execute("SELECT `id` FROM `users_account_data` WHERE `users_id` = %s", (int(result[0][0]),))
                    user_account_status = cursor.fetchall()

                    if len(user_account_status) != 0:

                        return ['successful', result[0][0], 'old_user']
                    
                    else:

                        return ['successful', result[0][0], 'new_user']

            else:
                return ['verification_code_not_found']
        
        except Error as e:
            print(f"Произошла ошибка сheck_user_block'{e}'")
            bot.send_message(chat_id, f"Произошла ошибка в check_auth\n\n{e}")
            return ['error']

def check_username_availability(connection, username_value):
    with connection.cursor() as cursor:
        try:
            username_value = username_value.replace(' ','')
            
            # Делаем запрос на проверку занятости username
            cursor.execute("SELECT `users_id`, `username` FROM `users_username` WHERE `username` = %s ORDER BY `dt_upd` DESC", (str(username_value),))
            result = cursor.fetchall()
            
            # Если username не был найден в базе, то выводим True
            if len(result) == 0:
                return ['True']
            
            # Иначе делаем проверку на то, занят ли сейчас выбранный username у последнего держателя
            else:
                cursor.execute("SELECT `username` FROM `users_username` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(result[0][0]),))
                result = cursor.fetchall()

                if username_value != str(result[0][0]):
                    return ['True']

                else:
                    return ['False']
        
        except Error as e:
                print(f"Произошла ошибка check_username_availability: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в check_username_availability\n\n{e}")
                return ['error']
        
def filling_profile(connection, users_id, username, name_surname, d_birth, city, user_avatar):
    with connection.cursor() as cursor:

        try:

            check_username = check_username_availability(create_connection(), username)
            name_surname = encrypt(repr(name_surname), crypto_key)
            # surname = encrypt(repr(surname), crypto_key)
            d_birth = encrypt(repr(d_birth), crypto_key) 
            user_avatar = convert_to_binary_data(user_avatar)

            cursor.execute("SELECT `id` FROM `cities` WHERE `city_name` = %s", (str(city),))
            city_id = cursor.fetchall()[0][0]

            if check_username[0] == 'True':

                cursor.executemany("INSERT INTO `users_username` (`id`, `users_id`, `username`, `dt_upd`) VALUES (NULL, %s, %s, NOW())", [(int(users_id), str(username),)])

                cursor.executemany("INSERT INTO `users_account_data` (`id`, `users_id`, `name_surname`, `d_birth`, `dt_upd`) VALUES (NULL, %s, %s, %s, NOW())",
                                    [(int(users_id), str(name_surname), str(d_birth),)])
                
                # cursor.executemany("INSERT INTO `users_surname` (`id`, `users_id`, `user_surname`, `dt_upd`) VALUES (NULL, %s, %s)", [(int(users_id), str(surname),)])

                cursor.executemany("INSERT INTO `users_city` (`id`, `users_id`, `cities_id`, `dt_upd`) VALUES (NULL, %s, %s, NOW())", [(int(users_id), int(city_id),)])

                cursor.executemany("INSERT INTO `users_photo` (`id`, `users_id`, `user_avatar`, `dt_upd`) VALUES (NULL, %s , %s, NOW())", [(int(users_id), user_avatar)])

                
                connection.commit()

                return ['successful']
            
            else:
                return ['username_is_taken']


        except Error as e:
                print(f"Произошла ошибка filling_profile: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в filling_profile\n\n{e}")
                return ['error']
        
def city_selection(connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT `city_name` FROM `cities`")
            result = cursor.fetchall()
            city = []
            for cities in result:
                city.append(cities[0])

            return city
        
        except Error as e:
                print(f"Произошла ошибка city_selection: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в city_selection\n\n{e}")
                return ['error']
        
def user_profile(connection, user_id):
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT `name_surname` FROM `users_account_data` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(user_id),))
            result = cursor.fetchall()
            name_surname = bytes.decode(decrypt(str_to_dict(result[0][0]), crypto_key)).replace("'",'')
            # print(name_surname)
            cursor.execute("SELECT `d_birth` FROM `users_account_data` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(user_id),))
            result = cursor.fetchall()
            d_birth = bytes.decode(decrypt(str_to_dict(result[0][0]), crypto_key)).replace("'",'')
            age = age_calc(d_birth)
            # print(age)
            cursor.execute("SELECT `cities_id` FROM `users_city` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(user_id),))
            result = cursor.fetchall()
            cursor.execute("SELECT `city_name` FROM `cities` WHERE `id` = %s", (int(result[0][0]),))
            result = cursor.fetchall()
            city = result[0][0]
            # print(city)
            cursor.execute("SELECT `user_phone_number` FROM `users_phone_number` WHERE `id` = %s", (int(user_id),))
            result = cursor.fetchall()
            phone_number = bytes.decode(decrypt(str_to_dict(result[0][0]), crypto_key)).replace("'",'')
            # print('+7'+ phone_number)
            cursor.execute("SELECT `username` FROM `users_username` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(user_id),))
            result = cursor.fetchall()
            username = result[0][0]
            # print(username)
            cursor.execute("SELECT `user_about` FROM `users_about` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(user_id),))
            result = cursor.fetchall()
            about = result[0][0]
            # print(about)
            cursor.execute("SELECT `user_avatar` FROM `users_photo` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(user_id),))
            result = cursor.fetchall()
            photo = convert_to_image(result)
            print(photo)

            return [name_surname, str(age), city, '+7'+ phone_number, username, about, photo]
        except Error as e:
                print(f"Произошла ошибка user_profile: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в user_profile\n\n{e}")
                return ['error']
        
def add_about(connection, users_id, about):
    with connection.cursor() as cursor:
        try:
            cursor.executemany("INSERT INTO `users_about` (`id`, `users_id`, `user_about`, `dt_upd`) VALUES (NULL, %s, %s, NOW())", [(int(users_id), str(about),)])
            connection.commit()

            return ['successful']
        
        except Error as e:
                print(f"Произошла ошибка add_about: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в add_about\n\n{e}")
                return ['error']

def save_user_location(connection, user_id, latitude, longitude):
    with connection.cursor() as cursor:
        try:
            cursor.executemany("INSERT INTO `users_location` (`id`, `users_id`, `latitude`, `longitude`, `dt_upd`) VALUES (NULL, %s, %s, %s, NOW())", [(int(user_id), float(latitude), float(longitude))])
            connection.commit()
            connection.close()

            return {"answer": "successful"}
        
        except Error as e:
                connection.rollback()
                connection.close()
                print(f"Произошла ошибка template: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в save_user_location\n\n{e}")
                return {"answer": "error"}

def get_users_location(connection, user_id):
     with connection.cursor() as cursor:
        try:
            output_data = []

            cursor.execute("SELECT `latitude`, `longitude` FROM `users_location` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(user_id),))                     
            user_location = cursor.fetchall()

            if len(user_location) != 0:
                output_data.append({"type": "user_location", 
                                    "user_id": int(user_id),
                                    "latitude": user_location[0][0],
                                    "longitude": user_location[0][1]})

            cursor.execute("SELECT `friend_users_id` FROM `users_friends` WHERE `users_id` = %s AND `status` = 0 ORDER BY `dt_rec` DESC", (int(user_id),))
            list_friend = cursor.fetchall()

            if len(list_friend) != 0:
                for friend in list_friend:
                    cursor.execute("SELECT `latitude`, `longitude` FROM `users_location` WHERE `users_id` = %s ORDER BY `dt_upd` DESC", (int(friend[0]),))                     
                    friend_location = cursor.fetchall()

                    if len(friend_location) != 0:
                        output_data.append({"type": "friend_location", 
                                            "user_id": friend[0],
                                            "latitude": friend_location[0][0],
                                            "longitude": friend_location[0][1]})

            return output_data

        except Error as e:
                print(f"Произошла ошибка template: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в get_user_location\n\n{e}")
                return {"answer": "error"}


# # ---------------------------------------------------------------------------------- #

def template(connection):
    with connection.cursor() as cursor:
        try:
            pass
        
        except Error as e:
                print(f"Произошла ошибка template: {e}")
                bot.send_message(chat_id, f"Произошла ошибка в template\n\n{e}")
                return ['error']


# ("SELECT FROM WHERE ORDER BY `dt_upd` DESC", (,))
# ("INSERT INTO () VALUES ()"", [(,)])
# ---------------------------------------------------------------------------------- #


# ТЕСТОВЫЕ ЗАПРОСЫ:

# print(user_authorisation(create_connection(), '79287539056', 97173))

# print(user_authorisation(create_connection(), '+7 (928) 753-90-56', 97173))

# print(filling_profile(create_connection(), "2", "seemyown3", "Семён Альбеев", "2003-07-03", "Ростов-на-Дону", None)) # Заполнение профиля

# print(user_authorisation(create_connection(), '79958932523', 58937)) # Прооверка авторизации пользователя

# city_selection(create_connection())

# print(check_username_availability(create_connection(), "seemyownn"))

# print(get_user_id(create_connection(), "79958932523"))
print(user_profile(create_connection(), "2"))

# print(add_about(create_connection(), 2, "Обо мне"))