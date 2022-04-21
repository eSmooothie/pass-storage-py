import os
import sys
import subprocess
import logging

from rsa import DecryptionError
try:
    import rsa
except ImportError as e:
    logging.error("at Encryption.py. {0}".format(e))
    logging.info("Trying to install RSA module")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'rsa'])
    print("Try to rerun the command.")
    sys.exit(0)

class Cryptography:
    
    def __init__(self):
        # retrieve keys
        logging.info("Retrieving encryption key.")
        file_path = os.path.realpath(__file__)
        proj_path = file_path.replace("encryption.py","")

        try:
            with open(proj_path+"public_key.pem","rb") as f:
                public_key_pkcs1pem = f.read()
                self.public_key = rsa.PublicKey.load_pkcs1(public_key_pkcs1pem)
                 
            with open(proj_path+"private_key.pem","rb") as f:
                private_key_pkcs1pem = f.read()
                self.__private_key = rsa.PrivateKey.load_pkcs1(private_key_pkcs1pem)
                
        except FileNotFoundError:
            # generate key pair
            self.public_key, self.__private_key = rsa.newkeys(2048)
            # write keys into file
            with open("public_key.pem","w") as f:
                # encode keys
                public_key_pkcs1pem = self.public_key.save_pkcs1().decode('utf-8')
                
                # write keys
                f.write(public_key_pkcs1pem)
                
            with open("private_key.pem","w") as f:
                # encode keys
                private_key_pkcs1pem = self.__private_key.save_pkcs1().decode('utf-8')
                
                # write keys
                f.write(private_key_pkcs1pem)
        except Exception as e: 
            logging.error("at Encryption.__init__(). {0}".format(e))  
            sys.exit(1)
            
    def encrypt(self, message):
        try:
            return rsa.encrypt(message.encode(), self.public_key)
        except Exception as e:
            logging.error("at Encryption.encrypt(). Error: {0}".format(e))
            sys.exit(1)
    
    def decrypt(self, encrpyt_message):
        try:
            return rsa.decrypt(encrpyt_message, self.__private_key).decode()
        except DecryptionError as err:
            logging.error("at Encryption.decrypt(). Error: {0} PRV_KEY: {1}".format(err, self.__private_key))
            print("Error: {0}".format(err))
            sys.exit(1)


