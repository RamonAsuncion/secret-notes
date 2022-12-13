# The most unsecure secret notes.

import os
import tkinter as tk
import sqlite3
import hashlib

class InterfaceWindow:
    def __init__(self):
        self.register_screen = None
        self.login_screen = None

class Interface(tk.Frame): # FIXME: bru the tk.Frame is needed for master. I guess the parent is Main?
    def __init__(self):
        """ Initialize the interface components of the application. """
        super().__init__()
        self.account_management = AccountManagement()

    def main_screen(self):
        """ Creates the interface for the main screen """
        self.master.title("Secret Notes")
        # self.master.iconphoto(True, tk.PhotoImage(file="./assets/images/main.png"))
        self.master.geometry("350x250")

        # Provide the login and register button to the user on the main page.
        tk.Label(text="Secret Notes", bg="#4BA400", fg="#FFFFFF", width="300", height="2", font=("Arial", 14)).pack()
        tk.Label(text="").pack()
        tk.Button(text="Login", height="1", width="25", font=("Arial", 12), command=self.login_page).pack()
        tk.Label(text="").pack()
        tk.Button(text="Register", height="1", width="25", font=("Arial", 12), command=self.register_page).pack()

    def register_page(self):
        """ Creates the interface for the registration screen """
        InterfaceWindow.register_screen = tk.Toplevel()
        InterfaceWindow.register_screen.title("Register")
        InterfaceWindow.register_screen.geometry("350x250")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(InterfaceWindow.register_screen, text="Please enter your details").pack()
        tk.Label(InterfaceWindow.register_screen, text="").pack()

        tk.Label(InterfaceWindow.register_screen, text="Username").pack()
        self.entry_username = tk.Entry(InterfaceWindow.register_screen, textvariable=self.username)
        self.entry_username.pack()

        tk.Label(InterfaceWindow.register_screen, text="Password").pack()
        self.entry_password = tk.Entry(InterfaceWindow.register_screen, textvariable=self.password)
        self.entry_password.pack()      

        tk.Label(InterfaceWindow.register_screen, text="").pack()
        self.entry_password.config(show="*")

        tk.Button(InterfaceWindow.register_screen, text="Register", height="1", width="10", command=self.send_credentials).pack()

    def login_page(self):
        """ Creates the interface for the login screen """
        # Creates the window for the login screen.
        InterfaceWindow.login_screen = tk.Toplevel()
        InterfaceWindow.login_screen.title("Login")
        InterfaceWindow.login_screen.geometry("350x250")

        tk.Label(InterfaceWindow.login_screen, text="Please enter your login details").pack()
        tk.Label(InterfaceWindow.login_screen, text="").pack()

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(InterfaceWindow.login_screen, text="Username").pack()
        self.entry_username = tk.Entry(InterfaceWindow.login_screen, textvariable=self.username)
        self.entry_username.pack()

        tk.Label(InterfaceWindow.login_screen, text="Password").pack()
        self.entry_password = tk.Entry(InterfaceWindow.login_screen, textvariable=self.password)
        self.entry_password.pack()

        tk.Label(InterfaceWindow.login_screen, text="").pack()
        self.entry_password.config(show="*")

        tk.Button(InterfaceWindow.login_screen, text="Login", height="1", width="10", command=lambda: self.send_credentials(login_flag=True)).pack()

    def send_credentials(self, login_flag=False):
        """ Sends user information to the account management system """
        self.account_management.receive_credentials(username=self.username.get(), password=self.password.get(), login_flag=login_flag)

    @staticmethod
    def prompt_user(option):
        # FIXME: Clean up this code.
        """ Prompt the user with prompts based on actions """
        if option == 'fail-login':
            login_failed = tk.Label(InterfaceWindow.login_screen, text="Password Error!", fg="#E81500", font=("Arial", 12))
            login_failed.after(1000, login_failed.destroy)
            login_failed.pack()
        elif option == 'user-taken':
            user_taken = tk.Label(InterfaceWindow.register_screen, text="Username already taken!", fg="#E81500", font=("Arial", 12))
            user_taken.after(1000, user_taken.destroy)
            user_taken.pack()
        elif option == 'registered':
            registered = tk.Label(InterfaceWindow.register_screen, text="Registered Successfully!", fg="#36BB00", font=("Arial", 12))
            registered.after(1000, registered.destroy)
            registered.pack()

class AccountManagement():
    def __init__(self):
        super().__init__()
        self.connect_to_database = sqlite3.connect("user.db")
        self.cursor = self.connect_to_database.cursor()
        self.create_database() # Construct the data base.

    def create_database(self):
        """ Creates a SQL database to store the user data. """
        # Check the table has been created.
        self.cursor.execute(f"PRAGMA table_info(accounts)")
        rows = self.cursor.fetchall()
        
        # Create the table if it is an empty database.
        if len(rows) <= 0:
            self.cursor.execute("CREATE TABLE accounts (username, password)")

    def receive_credentials(self, password, username, login_flag):
        """ Retrieve the user data from the text boxes. """
        self.username = username.lower()
        self.password = password

        if login_flag:
            self.login_verify(self.username, self.password)
        else:
            self.register_user()

    def user_exist(self, username):
        """ Check is the username is already taken. """
        search_query = "SELECT * FROM accounts WHERE username = ?"
        self.cursor.execute(search_query, (username.lower(),))
        # Check if user already exist in the database.
        if self.cursor.fetchone() is not None:
            Interface.prompt_user('user-taken')
            return True
        return False

    def register_user(self):
        """ Register the new user into the database. """
        if self.user_exist(self.username): return 
        hashed_password = self.hash_password(self.password)
        insert_query = "INSERT INTO accounts (username, password) VALUES (?, ?)"
        self.cursor.execute(insert_query, (self.username, hashed_password))    
        self.connect_to_database.commit()
        Interface.prompt_user('registered')

    def login_verify(self, username, password):
        """ Verify the user data to proceed with login. """
        hashed_password = self.hash_password(password)
        select_query = "SELECT * FROM accounts WHERE username = ? AND password = ?"
        self.cursor.execute(select_query, (username, hashed_password))
        result = self.cursor.fetchone()

        if result:
            self.dashboard()
        else:
            Interface.prompt_user('fail-login')
                
    def hash_password(self, password):
        """ Hash the users password. """
        # Use the SHA-256 algorithm to generate a cryptographic hash
        hash_object = hashlib.sha256(password.encode())

        # Return the hexadecimal representation of the hash
        return hash_object.hexdigest()

    # FIXME: I am never using this function.
    def close_connection(self):
         self.connect_to_database.close()

    # FIXME: There is no show password button.
    def password_show(self, button_click):
        if button_click == "show_login_password":
            self.entry_password.config(show="")
        elif button_click == "hide_login_password":
            self.entry_password.config(show="*")
        elif button_click == "show_register_password":
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def dashboard(self):
        """ Users dashboard. """
        note_management = NotesManagement()

        # self.dashboard_screen = tk.Toplevel(self.master)
        self.dashboard_screen = tk.Toplevel()
        self.dashboard_screen.title("Dashboard")
        self.dashboard_screen.geometry("350x250")
    
        tk.Label(self.dashboard_screen, text=f"Greetings, {self.username.capitalize()}!").pack()
        tk.Button(self.dashboard_screen, text="Create secret note", command=note_management.create_secret_notes).pack()
        tk.Button(self.dashboard_screen, text="View secret note", command=note_management.view_notes).pack()
        tk.Button(self.dashboard_screen, text="Delete secret note", command=note_management.delete_notes).pack()

class NotesManagement(tk.Frame):
    def __init__(self):
        super().__init__()

    def delete_notes_message(self):
        self.register_screen = tk.Toplevel(self.master)
        self.register_screen.title("Notes")
        self.register_screen.geometry("350x250")

        delete_file = self.delete_file.get()

        try:
            os.remove(delete_file)
        except:
            tk.Label(self.register_screen, text="File not found.").pack()

        tk.Label(self.register_screen, text=f"{delete_file} has been removed.").pack()

    def delete_notes(self):
        # TODO: Make sure the user can not delete the script files.
        self.register_screen = tk.Toplevel(self.master)
        self.register_screen.title("Delete")
        self.register_screen.geometry("350x250")

        list_files = [file for file in os.listdir()]

        tk.Label(self.register_screen, text="Choose a filename to delete: ").pack()
        tk.Label(self.register_screen, text=list_files).pack()

        self.delete_file = tk.StringVar()

        tk.Entry(self.register_screen, textvariable=self.delete_file).pack()
        tk.Button(self.register_screen, command=self.delete_notes_message, text="OK").pack()

    def view_notes(self):
        read_file_screen = tk.Toplevel(self.master)
        read_file_screen.title("Notes")
        read_file_screen.geometry("350x250")

        read_notes = open(self.file_name, "r")        
        data = read_notes.read()

        tk.Label(read_file_screen, text=data).pack()

    def save_text(self):
        # Get the filename from the textbox.
        get_filename = self.file_name.get()

        if get_filename == "" or "." in get_filename:
            empty_filename = tk.Label(self.notes_screen, text="Enter filename!", fg="#E81500", font=("Arial", 12))
            empty_filename.after(750, lambda: empty_filename.destroy())
            empty_filename.pack()
            return

        # Write the notes to the filename provided from the user.
        data = open(get_filename, "w")
        data.write(self.text_box.get("1.0", tk.END))
        data.close()

        # Confirm to the user that the data was saved successfully.
        tk.Label(self.notes_screen, text="Text File Saved", fg="#36BB00", font=("Arial", 12)).pack()

    def create_secret_notes(self):
        self.file_name = tk.StringVar()
        self.text_box = ""

        self.notes_screen = tk.Toplevel(self.master)
        self.notes_screen.title("Make Notes")
        self.notes_screen.geometry("350x250")

        tk.Label(self.notes_screen, text="Enter a filename: ").pack()
        tk.Entry(self.notes_screen, textvariable=self.file_name).pack()
        tk.Label(self.notes_screen, text="Enter secret notes: ").pack()

        self.text_box = tk.Text(self.notes_screen, width=30, height=8)
        self.text_box.insert(tk.END, "Enter your notes here!") #FIXME: Remote this text box on click.
        self.text_box.config(state=tk.NORMAL)
        self.text_box.pack(expand=False)

        tk.Button(self.notes_screen, text="Save", command=self.save_text).pack()

    def choose_files(self):
        open_file_screen = tk.Toplevel(self.master)
        open_file_screen.title("Info")
        open_file_screen.geometry("350x250")

        # Do not include current user in the list of files.
        list_files = os.listdir()

        tk.Label(open_file_screen, text="Choose a filename below: ").pack()
        tk.Label(open_file_screen, text=list_files).pack()

        self.file_name = tk.StringVar()

        tk.Entry(open_file_screen, textvariable=self.file_name).pack()
        tk.Button(open_file_screen, command=self.view_notes, text="OK").pack()

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.interface = Interface()
        self.notes_management = NotesManagement()
        self.account_management = AccountManagement()
        self.interface.main_screen()

if __name__ == '__main__':
    root = tk.Tk()
    application = MainApplication(root)
    application.pack(fill="both", expand=True)
    root.mainloop()
