from tkinter import *
from tkinter import messagebox
import os

# Django and Flask are the most popular tools used to write an application server in Python
# TODO: Create a random directory name? (privacy) or upload it to a vps and call request for access
# TODO: Destroy the labels after shown for a few seconds. 
# TODO: Save notes into directory of username.
# TODO: If notes file already exist do not overwrite those notes. 
# TODO: Make it so the user can not resize the UI (Done for login, register, and startup!)
# TODO: Allow the user to enter their username lowercased and it will default to what they originally put. Ex: allowed input: ramonasuncion --> return RamonAsuncion (original)
# TODO: Change the place to where you write text to 'Text' input instead of textvariable. 
# TODO: Start working on protecting the password through hashing. 
# TODO: Add image of an eye for password viewer 
# TODO: Do not allow certain characters to become usernames (regex), such at dotfiles
# TODO: I should not be able to spam the register/login/save button and keep getting the label to show up. 
# TODO: File naming system is shit I need to fix that... Sometimes it says the file_name is not defined like wtf????
# TODO: Once I create a new file I need to somehow "refresh" the file system because it cant locate the newly made user... I have to restart the program to do that.
# Thread to run the sleep command on the text? Make it sleep? And then it disappers. Need to look more into threads. 

def register_user():
    username_info = username.get()
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
        
        Label(register_screen, text="Registration successful!", fg="#36BB00", font=("Lato", 12)).pack()
        
    except FileExistsError:
        Label(register_screen, text="User Already Created", fg="#F18300", font=("Lato", 12)).pack()
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
    
    Label(notes_screen, text="Text File Saved", fg="#36BB00", font=("Lato", 12)).pack()

def login_completed():
    global dashboard_screen
    dashboard_screen = Toplevel(main_screen)
    dashboard_screen.title("Dashboard")
    dashboard_screen.geometry("350x250")
    
    welcome_user = user_verify.get()
    
    Label(dashboard_screen, text="Welcome to the dashboard " + welcome_user + "!").pack() 
    Button(dashboard_screen, text="Create secret note", command=create_secret_notes).pack()
    Button(dashboard_screen, text="View secret note", command=view_notes).pack()
    Button(dashboard_screen, text="Delete secret note", command=delete_notes).pack()
    
    dashboard_screen.protocol("WM_DELETE_WINDOW", close_gui_windows)

# WM_DELETE_WINDOW 
def close_gui_windows():
    if messagebox.askokcancel("Warning", "Do you want to exit dashboard?"):
        # TODO: When person signout of their account it needs to exit out of the folder (testing --> not the most thought out way)
        
        
        # dashboard_screen.destory()
        # TODO: Go back to the main directory folder. ("..") can be risky due to it being access to full location where the folder is located.
        os.chdir("./")   

def delete_notes():
    global delete_file

    register_screen0 = Toplevel(main_screen)
    register_screen0.title("Delete")
    register_screen0.geometry("350x250")
    
    list_all_files = os.listdir()
    
    Label(register_screen0, text="Choose a filename to delete: ").pack()
    Label(register_screen0, text=list_all_files).pack()
    
    delete_file = StringVar()
    
    Entry(register_screen0, textvariable=delete_file).pack()
    Button(register_screen0, command=delete_notes_message, text="OK").pack()


def delete_notes_message():
    delete = delete_file.get()
    os.remove(delete)
    
    register_screen1 = Toplevel(main_screen)
    register_screen1.title("Notes")
    register_screen1.geometry("350x250")
    
    Label(register_screen1, text=delete+" has been removed").pack()


def create_secret_notes():
    global create_file_name
    global create_notes
    global notes_screen
    
    create_file_name = StringVar()
    create_notes = StringVar()
    
    notes_screen = Toplevel(main_screen)
    notes_screen.title("Make Notes")
    notes_screen.geometry("350x250")
    
    Label(notes_screen, text="Enter a filename: ").pack()
    Entry(notes_screen, textvariable=create_file_name).pack()
    Label(notes_screen, text="Enter secret notes: ").pack()
    Entry(notes_screen, textvariable=create_notes).pack()
    Button(notes_screen, text="Save", command=save_file).pack()

def choose_files():
    global file_name

    open_file_screen = Toplevel(main_screen)
    open_file_screen.title("Info")
    open_file_screen.geometry("350x250")
    
    list_all_files = os.listdir()
    
    Label(open_file_screen, text="Choose a filename below: ").pack()
    Label(open_file_screen, text=list_all_files).pack()
    
    file_name = StringVar()
    
    Entry(open_file_screen, textvariable=file_name).pack()
    Button(open_file_screen, command=view_notes, text="OK").pack()
    
def view_notes():    
    read_file_screen = Toplevel(main_screen)
    read_file_screen.title("Notes")
    read_file_screen.geometry("350x250")    
    
    read_notes = open(file_name.get(), "r")
    data = read_notes.read()
    
    Label(read_file_screen, text=data).pack()

def login_verify():
    get_username = user_verify.get()
    get_password = pass_verify.get()

    list_of_files = os.listdir()
    if get_username in list_of_files:
        file_name = str(get_username)
        print("Debug file name: " + file_name)
        os.chdir("./" + file_name)
        file_open = open(get_username, "r")
        verify = file_open.read().splitlines()
        if get_password in verify:
            login_completed()
        else:
            Label(login_screen, text="Password Error!", fg="#E81500", font=("Lato", 12)).pack()
    else:
        Label(login_screen, text="User not found!", fg="#E81500", font=("Lato", 12)).pack()


def login_page():
    global login_screen
    global entry_username1
    global entry_password1
    global user_verify
    global pass_verify
    
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("350x250")
    login_screen.resizable(0,0)

    
    Label(login_screen, text="Please enter your login details").pack()
    Label(login_screen, text="").pack()
    
    user_verify = StringVar()
    pass_verify = StringVar()

    Label(login_screen, text="Username").pack()
    entry_username1 = Entry(login_screen, textvariable=user_verify)
    entry_username1.pack()
    Label(login_screen, text="Password").pack()
    entry_password1 = Entry(login_screen, textvariable=pass_verify)
    entry_password1.pack()
    Label(login_screen, text="").pack()
    entry_password1.config(show="*")
    
    Button(login_screen, text="Show password!", height="1", width="12", command=lambda: password_show("show_login_password")).pack()
    Button(login_screen, text="Hide password!", height="1", width="12", command=lambda: password_show("hide_login_password")).pack()
    Button(login_screen, text="Login", height="1", width="10", command=login_verify).pack()

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
    global register_screen
    global username
    global password
    global entry_username
    global entry_password
    
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("350x250")
    register_screen.resizable(0,0)

    
    username = StringVar()
    password = StringVar()
    
    Label(register_screen, text="Please enter your details").pack()
    Label(register_screen, text="").pack()
    Label(register_screen, text="Username").pack()
    entry_username = Entry(register_screen, textvariable=username)
    entry_username.pack()
    Label(register_screen, text="Password").pack()
    entry_password = Entry(register_screen, textvariable=password)
    entry_password.pack()
    Label(register_screen, text="").pack() 
    entry_password.config(show="*")
    
    Button(register_screen, text="Show password!", height="1", width="12", command=lambda: password_show("show_register_password")).pack()
    Button(register_screen, text="Hide password!", height="1", width="12", command=lambda: password_show("hide_register_password")).pack()
    Button(register_screen, text="Register", height="1", width="10", command=register_user).pack()

    
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
