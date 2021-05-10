from tkinter import *
from tkinter import font
import os

# Django and Flask are the most popular tools used to write an application server in Python
# TODO: Create a random directory name? Date should be secu#E81500.
# TODO: Destroy the labels after shown for a few seconds. 
# TODO: Save notes into directory of username.
# TODO: If notes file already exist do not overwrite. 
# TODO: Make it so the user can not resize the UI
# Thread to run the sleep command on the text? Make it sleep? And then it disappers. Need to look more into threads. 

# Welcomes user once signed in, casting file name as a string, 

def register_user():
    username_info = username.get().lower()
    password_info = password.get()
    
    try:
        # TODO: Some names are not allowed to be folders because of they being characters. Also, don't allowed periods so they don't become hidden files: .gitignore
        os.makedirs(username_info)
        os.chdir(username_info)
        file = open(username_info, "w")
        file.write("Username:\n")
        file.write(username_info + "\n")
        file.write("Password:\n")
        file.write(password_info)
        file.close()
        
        Label(screen1, text="Registration successful!", fg="#36BB00", font=("Lato", 12)).pack()
    except FileExistsError:
        Label(screen1, text="User Already Created", fg="#F18300", font=("Lato", 12)).pack()
        # TODO: Make this exception unnecessary maybe by creating the file instead of trying to chdir when its not found? 
    except FileNotFoundError:
        pass
        
    entry_username.delete(0,END)
    entry_password.delete(0,END)

def save_file():
    get_file_name = create_file_name.get()
    get_notes = create_notes.get()
    
    data = open(get_file_name, "w")
    data.write(get_notes)
    data.close()
    
    Label(screen7, text="Text File Saved", fg="#36BB00", font=("Lato", 12)).pack()

def login_completed():
    screen6 = Toplevel(main_screen)
    screen6.title("Dashboard")
    screen6.geometry("350x250")
    
    welcome_user = user_verify.get()
    
    Label(screen6, text="Welcome to the dashboard " + welcome_user + "!").pack() 
    Button(screen6, text="Create secret note", command=create_secret_notes).pack()
    Button(screen6, text="View secret note", command=view_notes).pack()
    Button(screen6, text="Delete secret note", command=delete_notes).pack()


def delete_notes():
    global delete_file

    screen10 = Toplevel(main_screen)
    screen10.title("Delete")
    screen10.geometry("350x250")
    
    list_all_files = os.listdir()
    
    Label(screen10, text="Choose a filename to delete: ").pack()
    Label(screen10, text=list_all_files).pack()
    
    delete_file = StringVar()
    
    Entry(screen10, textvariable=delete_file).pack()
    Button(screen10, command=delete_notes_message, text="OK").pack()


def delete_notes_message():
    delete = delete_file.get()
    os.remove(delete)
    
    screen11 = Toplevel(main_screen)
    screen11.title("Notes")
    screen11.geometry("350x250")
    
    Label(screen11, text=delete + " has been removed").pack()


def create_secret_notes():
    global create_file_name
    global create_notes
    global screen7
    
    create_file_name = StringVar()
    create_notes = StringVar()
    
    screen7 = Toplevel(main_screen)
    screen7.title("Make Notes")
    screen7.geometry("350x250")
    
    Label(screen7, text="Enter a filename: ").pack()
    Entry(screen7, textvariable=create_file_name).pack()
    Label(screen7, text="Enter secret notes: ").pack()
    Entry(screen7, textvariable=create_notes).pack()
    Button(screen7, text="Save", command=save_file).pack()

def choose_files():
    global file_name

    screen8 = Toplevel(main_screen)
    screen8.title("Info")
    screen8.geometry("350x250")
    
    list_all_files = os.listdir()
    
    Label(screen8, text="Choose a filename below: ").pack()
    Label(screen8, text=list_all_files).pack()
    
    file_name = StringVar()
    
    Entry(screen8, textvariable=file_name).pack()
    Button(screen8, command=view_notes, text="OK").pack()
    
def view_notes():    
    screen9 = Toplevel(main_screen)
    screen9.title("Notes")
    screen9.geometry("350x250")    
    
    read_notes = open(file_name.get(), "r")
    data = read_notes.read()
    
    Label(screen9, text=data).pack()

def login_verify():
    get_username = user_verify.get().lower()
    get_password = pass_verify.get()

    list_of_files = os.listdir()
    if get_username in list_of_files:
        file_name = str(user_verify.get())
        print("Debug file name: " + file_name)
        os.chdir(file_name)
        file_open = open(get_username, "r")
        verify = file_open.read().splitlines()
        if get_password in verify:
            login_completed()
        else:
            Label(screen2, text="Password Error!", fg="#E81500", font=("Lato", 12)).pack()
    else:
        Label(screen2, text="User not found!", fg="#E81500", font=("Lato", 12)).pack()
    # TODO: When person signout of their account it needs to exit out of the folder 
    # os.chdir("..")   


def login_page():
    global screen2
    global entry_username1
    global entry_password1
    global user_verify
    global pass_verify
    
    screen2 = Toplevel(main_screen)
    screen2.title("Login")
    screen2.geometry("350x250")
    screen2.resizable(0,0)

    
    Label(screen2, text="Please enter your login details").pack()
    Label(screen2, text="").pack()
    
    user_verify = StringVar()
    pass_verify = StringVar()

    Label(screen2, text="Username").pack()
    entry_username1 = Entry(screen2, textvariable=user_verify)
    entry_username1.pack()
    Label(screen2, text="Password").pack()
    entry_password1 = Entry(screen2, textvariable=pass_verify)
    entry_password1.pack()
    Label(screen2, text="").pack()
    entry_password1.config(show="*")
    
    Button(screen2, text="Show password!", height="1", width="12", command=lambda: password_show("show_login_password")).pack()
    Button(screen2, text="Hide password!", height="1", width="12", command=lambda: password_show("hide_login_password")).pack()
    Button(screen2, text="Login", height="1", width="10", command=login_verify).pack()

def password_show(button_click):
    if button_click == "show_login_password":
        entry_password1.config(show="") 
    elif button_click == "hide_login_password":
        entry_password1.config(show="*")
    elif button_click == "show_register_password":
        entry_password.config(show="") 
    else:
        entry_password.config(show="*")
        
def register_page():
    global screen1
    global username
    global password
    global entry_username
    global entry_password
    
    screen1 = Toplevel(main_screen)
    screen1.title("Register")
    screen1.geometry("350x250")
    screen1.resizable(0,0)

    
    username = StringVar()
    password = StringVar()
    
    Label(screen1, text="Please enter your details").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Username").pack()
    entry_username = Entry(screen1, textvariable=username)
    entry_username.pack()
    Label(screen1, text="Password").pack()
    entry_password = Entry(screen1, textvariable=password)
    entry_password.pack()
    Label(screen1, text="").pack() 
    entry_password.config(show="*")
    
    Button(screen1, text="Show password!", height="1", width="12", command=lambda: password_show("show_register_password")).pack()
    Button(screen1, text="Hide password!", height="1", width="12", command=lambda: password_show("hide_register_password")).pack()
    Button(screen1, text="Register", height="1", width="10", command=register_user).pack()

    
def screen():
    global main_screen
    
    main_screen = Tk()
    main_screen.geometry("350x250")
    main_screen.title("Secret Notes")
    main_screen.iconphoto(True, PhotoImage(file="./assets/images/favicon.png"))
    main_screen.resizable(0,0)    
    
    Label(text="Secret Notes", bg="#4BA400", fg="#FFFFFF", width="300", height="2", font=("Lato", 14)).pack()
    Label(text="").pack()
    Button(text="Login", height="1", width="25", font=("Lato", 12), command=login_page).pack()
    Label(text="").pack()
    Button(text="Register", height="1", width="25", font=("Lato", 12), command=register_page).pack()
    
    
    main_screen.mainloop()
        
if __name__ == '__main__':
    screen()
