#This script decrypts password or api key from encrypted .bin file

from cryptography.fernet import Fernet

akey = b'PasteCipheredTextFromEncryptedFileForPasswordsScriptHere'
skey = b'PasteCipheredTextFromEncryptedFileForPasswordsScriptHere'
akey_file = '/path/to/keyfolder/accesskeyfile.bin'
skey_file = '/path/to/keyfolder/secretkeyfile.bin'

#Function
def decrypt_key(key, key_file):
    cipher_suite = Fernet(key)
    with open(key_file, 'rb') as key_file:
        for line in key_file:
            encryptedpwd = line
    unciphered_text = (cipher_suite.decrypt(encryptedpwd))
    plain_text_encryptedpassword = bytes(unciphered_text).decode("utf-8")
    return plain_text_encryptedpassword

#Decrypt and display password(s)
access_key = decrypt_key(akey, akey_file)
secret_key = decrypt_key(skey, skey_file)

print("Access key is: {0}".format(access_key))
print("Secret key is: {0}".format(secret_key))