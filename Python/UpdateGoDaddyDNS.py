#!/bin
#This script gets the current public IP of the network and updates GoDaddy DNS records
#to keep DNS records up to date

from pif import get_public_ip
from godaddypy import Client, Account
from cryptography.fernet import Fernet
import logging

#Constants
AKEY = b'EnterAccessKeyHashHere' #Access key hash
SKEY = b'EnterSecretKeyHashHere' #Secret key hash
AKEY_FILE = '/path/to/binary_key_folder/access_binary_key.file'
SKEY_FILE = '/path/to/binary_key_folder/secret_binary_key.file'
DOMAIN = 'EnterDomainHere'  #example.com
DOMAIN_NAME = 'EnterSubdomainNameHere'  #site
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"

#Add logging
logging.basicConfig(filename = "//path//to//log//folder//GoDaddyDNSUpdate.log", level = logging.INFO, format = LOG_FORMAT)
logger = logging.getLogger()

#Functions
#Decrypt DNS API keys
def decrypt_key(key, key_file):
    '''
    DOCSTRING: This function decrypts the api access and secret keys for GoDaddy API call
    INPUT: Binary key for password file and location of password file
    OUTPUT: Returns plaintext password
    '''
    
    cipher_suite = Fernet(key)
    with open(key_file, 'rb') as key_file:
        for line in key_file:
            encryptedpwd = line
    unciphered_text = (cipher_suite.decrypt(encryptedpwd))
    plain_text_encryptedpassword = bytes(unciphered_text).decode("utf-8")
    return plain_text_encryptedpassword

#Start logging
logger.debug('\n')
logger.debug("**********Starting GoDaddy DNS Update**********")

#Retrieve access and secret keys from encrypted file
logger.debug("Decrypting access key")
access_key = decrypt_key(AKEY, AKEY_FILE)
logger.debug("Decrypting secret key")
secret_key = decrypt_key(SKEY, SKEY_FILE)

#Set account information for GoDaddy API call
my_acct = Account(api_key=access_key, api_secret=secret_key)
client = Client(my_acct)

#Get public IP
logger.debug('Getting Public IP address of local network')
public_ip = get_public_ip()

#Get current DNS record
logger.debug("Getting current DNS record from GoDaddy")
dns_record = client.get_records(DOMAIN, record_type='A', name=DOMAIN_NAME)
godaddy_dns = dns_record[0]['data']

#Update DNS record only if public ip doesn't match DNS record
logger.debug("Checking if Public IP matches GoDaddy DNS record and updating if not")
if godaddy_dns != public_ip:
    client.update_record_ip(public_ip, DOMAIN,DOMAIN_NAME, 'A')
    logger.info("Updated Public IP address in GoDaddy from {0} to {1}. ".format(godaddy_dns, public_ip))
else:
    logger.info('Public IP address {0} did not change. GoDaddy DNS was not updated & DNS IP address is still: {1}'.format(public_ip, godaddy_dns))
