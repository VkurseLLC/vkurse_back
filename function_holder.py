import base64
import datetime
from datetime import date
from PIL import Image, ImageDraw, ImageFilter
import io

# Преобразователь строки в словать(использовать только для закодированных строк с помощью фукнкции encode() )
def str_to_dict(value):
    value = value.replace('{', '')
    value = value.replace('}', '')
    value = value.replace(':', '')
    value = value.replace(',', '')
    value = value.replace("'", '')

    keys_val = []
    for elements in value.split():
        keys_val.append(elements)

    new_dict= {}
    for i in range(len(keys_val)-1):
        if keys_val[i] == 'cipher_text':
            new_dict.setdefault(keys_val[i], keys_val[i+1])
        elif keys_val[i] == 'salt':
            new_dict.setdefault(keys_val[i], keys_val[i+1])
        elif keys_val[i] == 'nonce':
            new_dict.setdefault(keys_val[i], keys_val[i+1])
        elif keys_val[i] == 'tag':
            new_dict.setdefault(keys_val[i], keys_val[i+1])

    return new_dict
#----------------------------------------------------------------------
# Калькулятор возраста
def age_calc(d_birth):
    day = int(d_birth[8:])
    month = int(d_birth[5:7])
    year = int(d_birth[:4])
    today = date.today()
    return today.year - year - ((today.month, today.day) < (month, day))
#------------------------------------------------------------------------
# Преобразование изображения для сохранения в БД
def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return base64.b64encode(blob_data)
#------------------------------------------------------------------------
# Преобразование изображения для вывода
def convert_to_image(data):
    image = data[0][0]
    binary_data = base64.b64decode(image)
    image = Image.open(io.BytesIO(binary_data))
    return image
#------------------------------------------------------------------------
# Наложение фотографии профиля на иконку маркера
def geometca_photo(user_photo):
    backgroung = Image.open('img\icon_background.png')
    user_photo = Image.open(user_photo)

    user_photo.thumbnail(size=(384,384))
    mask_im = Image.new("L", (384,384), 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((40,40,344,344), fill=255)
    mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))

    backgroung.paste(user_photo, (64, 64), mask_im_blur)
    return backgroung
#-------------------------------------------------------------------------