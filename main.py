import tkinter as tk
from hashlib import sha256
from PIL import Image, ImageTk
import os
from distutils.cmd import Command
from tkinter import CENTER, PhotoImage, Tk,Label, Button, Entry,Frame,END, Toplevel
from db_operations import DbOperations
from password_manager import *


# GUI
root = tk.Tk()
root.title("Password Manager")

# Set the window size
root.geometry("800x600")

# Load and display the background image
bg_image = Image.open("lock.png")  
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


label = tk.Label(root, text="Locker", font=("Algerian", 24, "bold"),bg='orange')
label.pack(pady=50)

user_database = {
    "user1": None,  
    "user2": None,  
}

# File to store the password set status and hashed password
password_status_file = "password_status.txt"
password_hash_file = "password_hash.txt"

def encrypt_password(password):
    return sha256(password.encode()).hexdigest()

def set_password(username, password):
    user_database[username] = encrypt_password(password)

def change_password(username, old_password, new_password):
    encrypted_old_password = encrypt_password(old_password)
    if user_database.get(username) == encrypted_old_password:
        user_database[username] = encrypt_password(new_password)
        return True
    return False

def login(username, password):
    encrypted_password = encrypt_password(password)
    return user_database.get(username) == encrypted_password

def save_password_status_to_file(status):
    with open(password_status_file, "w") as file:
        file.write(str(status))

def read_password_status_from_file():
    if os.path.exists(password_status_file):
        with open(password_status_file, "r") as file:
            return bool(file.read().strip())
    return False

def save_password_hash_to_file(password_hash):
    with open(password_hash_file, "w") as file:
        file.write(password_hash)

def read_password_hash_from_file():
    if os.path.exists(password_hash_file):
        with open(password_hash_file, "r") as file:
            return file.read().strip()
    return None


stored_hash = read_password_hash_from_file()
if stored_hash is not None:
    user_database["user1"] = stored_hash

def show_message(message):
    info_label.config(text=message)

def enter(e):
    global root  # Declare root as a global variable
    password = entry_password.get()

    if login("user1", password):
        # Destroy the lock window
        root.destroy()

        if __name__ == "__main__":
            # create table if doesn't exist
            db_class = DbOperations()
            db_class.create_table()

            # create tkinter window
            root = Tk()
            root_class = root_window(root, db_class)
            root.mainloop()
    else:
        show_message("Invalid password")

def on_login_click():
    global root  # Declare root as a global variable
    password = entry_password.get()

    if login("user1", password):
        # Destroy the lock window
        root.destroy()

        if __name__ == "__main__":
            # create table if doesn't exist
            db_class = DbOperations()
            db_class.create_table()

            # create tkinter window
            root = Tk()
            root_class = root_window(root, db_class)
            root.mainloop()
    else:
        show_message("Invalid password")


def on_change_password_click():
    def confirm_change_password():
        old_password = entry_old_password.get()
        new_password = entry_new_password.get()

        if change_password("user1", old_password, new_password):
            show_message("Password changed successfully!")
            change_password_window.destroy()
        else:
            show_message("Invalid password")

    change_password_window = tk.Toplevel(root)
    change_password_window.title("Change Password")
    change_password_window.geometry("600x300")

    label_old_password = tk.Label(change_password_window, text="Old Password:",font=("Ariel",15),bg='yellow')
    label_old_password.pack(pady=1)
    entry_old_password = tk.Entry(change_password_window, show="*",font=("Ariel",15),bg='lightgray')
    entry_old_password.pack(pady=15)

    label_new_password = tk.Label(change_password_window, text="Set Password:",font=("Ariel",15),bg='yellow')
    label_new_password.pack(pady=1)
    entry_new_password = tk.Entry(change_password_window, show="*",font=("Ariel",15),bg='lightgray',)
    entry_new_password.pack(pady=5)

    button_change_password = tk.Button(change_password_window, text="Change Password", command=confirm_change_password,font=("Ariel",15),bg='lightgreen', padx=10, pady=5)
    button_change_password.pack()

def on_set_password_click():
    if not read_password_status_from_file():
        def confirm_set_password():
            new_password = entry_new_password.get()

            set_password("user1", new_password)
            show_message("Password set successfully!")
            save_password_status_to_file(True)  


            hashed_password = encrypt_password(new_password)
            save_password_hash_to_file(hashed_password)
            user_database["user1"] = hashed_password

            button_set_password.config(state=tk.DISABLED)  
            set_password_window.destroy()

        set_password_window = tk.Toplevel(root)
        set_password_window.title("Set Password")
        set_password_window.geometry("400x200")

        label_new_password = tk.Label(set_password_window, text="New Password:",font=("Ariel,15"),bg='yellow')
        label_new_password.pack(pady=10)
        entry_new_password = tk.Entry(set_password_window, show="*",font=("Ariel",15),bg='lightgray')
        entry_new_password.pack(pady=10)

        button_set_password = tk.Button(set_password_window, text="Set Password", command=confirm_set_password, padx=10, pady=5,font=("Ariel",15),bg='lightgreen')
        button_set_password.pack()
    else:
        show_message("Password already set!")



label_password = tk.Label(root,font=("Ariel",15),bg='#E61FA4', text="Enter Password:")
label_password.pack(pady=25)

entry_password = tk.Entry(root,font=("Ariel",20),bg='lightgray' ,show="*",width=25,)
entry_password.pack(pady=3)

button_login = tk.Button(root, text="Login", command=on_login_click,bg="lightgreen",font=("Ariel",10), padx=15, pady=7,width=30)
button_login.pack(pady=3)

button_change_password = tk.Button(root, text="Change Password", command=on_change_password_click,bg="yellow",font=("Ariel",10), padx=15, pady=7,width=25)
button_change_password.pack(pady=3)

button_set_password = tk.Button(root, text="Set Password", command=on_set_password_click,bg="aqua",font=("Ariel",10), padx=15, pady=7,width=20)
button_set_password.pack()

info_label = tk.Label(root, text="", fg="red",font=("Ariel" ,15))
info_label.pack()

root.bind('<Return>',enter)


if read_password_status_from_file():
   button_set_password.config(state=tk.DISABLED)

root.mainloop()