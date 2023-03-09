from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes

crypto_key = "Y3V1ba3FWwnd6u0O3ReoGzqNMBfBrw3DNIXOGfHJozlxyMwn2MSiK4TCJqAPgOn1" # Random 512-bit key
# phone_number_value = 9958932523
# crypto_key = (hashlib.sha256(repr(phone_number_value).encode())).hexdigest()
# print(crypto_key)

def encrypt(plain_text, password):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)
    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    result = {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')}
    
    return result

    



def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    
    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted

#-------------TEST ENCODE AND DECODE----------------------------------#

# enc_res = encrypt(str(9958932523), crypto_key)
# print(enc_res)
# enc_res1 = encrypt(str(9958932523), crypto_key)
# print(enc_res1)
# decrypt_res = decrypt(enc_res, crypto_key)
# decrypt_res1 = decrypt(enc_res1, crypto_key)

# print(bytes.decode(decrypt_res))
# print(bytes.decode(decrypt_res1))
