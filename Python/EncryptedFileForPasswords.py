#This script creates encrypted file to store password or other keys using binary files.
#Use this script in conjunction with the UpdateGoDaddyDNS script

from cryptography.fernet import Fernet

#Create key
key = Fernet.generate_key()
print("Encryption key: {0}".format(key))

#Encrypt password
cipher_suite = Fernet(key)
ciphered_text = cipher_suite.encrypt(b"EnterPasswordOrAPIKeyHere")
print("Ciphered text: {0}".format(ciphered_text)) #Must grab ciphered text from this step to use in the RetrieveEncryptedPassword program

#Write password to file
with open('/path/to/keyfolder/keyfile.bin', 'wb') as key_file:
    key_file.write(ciphered_text)

#VERY IMPORTANT: Remember to set .bin file(s) to 600 level permissions (sudo chmod 600 file.bin) so no other user can use bin file