import tkinter as tk
import sqlite3
import hashlib
import uuid
import datetime
import re

class Window:
    def __init__(self):
        self.register_screen = None
        self.login_screen = None
        self.notes_screen = None

class Interface(tk.Frame):
    def __init__(self):
        """ Initialize the interface components of the application. """
        super().__init__()
        self.account_management = AccountManagement()

        # Close the database on close of the application.
        self.master.protocol("WM_DELETE_WINDOW", self.account_management.close_connection)

    def main_screen(self):
        """ Creates the interface for the main screen """
        self.master.title("Secret Notes")
        self.master.geometry("350x250")

        # Provide the login and register button to the user on the main page.
        tk.Label(text="Secret Notes", bg="#4BA400", fg="#FFFFFF", width="300", height="2", font=("Arial", 14)).pack()
        tk.Label(text="").pack()
        tk.Button(text="Login", height="1", width="25", font=("Arial", 12), command=self.login_page).pack()
        tk.Label(text="").pack()
        tk.Button(text="Register", height="1", width="25", font=("Arial", 12), command=self.register_page).pack()

    def register_page(self):
        """ Creates the interface for the registration screen """
        Window.register_screen = tk.Toplevel()
        Window.register_screen.title("Register")
        Window.register_screen.geometry("350x250")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(Window.register_screen, text="Please enter your details").pack()
        tk.Label(Window.register_screen, text="").pack()

        tk.Label(Window.register_screen, text="Username").pack()
        self.entry_username = tk.Entry(Window.register_screen, textvariable=self.username)
        self.entry_username.pack()

        tk.Label(Window.register_screen, text="Password").pack()
        self.entry_password = tk.Entry(Window.register_screen, textvariable=self.password)
        self.entry_password.pack()

        tk.Label(Window.register_screen, text="").pack()
        self.entry_password.config(show="*")

        #TODO: Clear the register password text.

        tk.Button(Window.register_screen, text="Register", height="1", width="10", command=self.send_credentials).pack()

    def login_page(self):
        """ Creates the interface for the login screen """
        # Creates the window for the login screen.
        Window.login_screen = tk.Toplevel()
        Window.login_screen.title("Login")
        Window.login_screen.geometry("350x250")

        tk.Label(Window.login_screen, text="Please enter your login details").pack()
        tk.Label(Window.login_screen, text="").pack()

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(Window.login_screen, text="Username").pack()
        self.entry_username = tk.Entry(Window.login_screen, textvariable=self.username)
        self.entry_username.pack()

        tk.Label(Window.login_screen, text="Password").pack()
        self.entry_password = tk.Entry(Window.login_screen, textvariable=self.password)
        self.entry_password.pack()

        tk.Label(Window.login_screen, text="").pack()
        self.entry_password.config(show="*")

        #TODO: Clear the login text.

        tk.Button(Window.login_screen, text="Login", height="1", width="10", command=lambda: self.send_credentials(login_flag=True)).pack()

    def send_credentials(self, login_flag=False):
        """ Sends user information to the account management system """
        self.account_management.receive_credentials(username=self.username.get(), password=self.password.get(), login_flag=login_flag)

        # # FIXME: There is no show password button.
    # def password_show(self, button_click):
    #     if button_click == "show_login_password":
    #         self.entry_password.config(show="")
    #     elif button_click == "hide_login_password":
    #         self.entry_password.config(show="*")
    #     elif button_click == "show_register_password":
    #         self.entry_password.config(show="")
    #     else:
    #         self.entry_password.config(show="*")

    @staticmethod
    def create_label(text, color, font, window, time=1000):
        """ Helper method to create a label that get's destroyed after a second. """
        label = tk.Label(window, text=text, fg=color, font=font)
        label.after(time, label.destroy)
        label.pack()

    @staticmethod
    def prompt_user(option):
        """ Prompt the user with prompts based on actions """
        if option == 'fail-login':
            Interface.create_label("Please check login details.", "#E81500", ("Arial", 12), Window.login_screen)
        elif option == 'user-taken':
            Interface.create_label("Username taken.", "#E81500", ("Arial", 12), Window.register_screen)
        elif option == 'registered':
            Interface.create_label("Successfully registered.", "#36BB00", ("Arial", 12), Window.register_screen)
        elif option == 'notes-saved':
            Interface.create_label("Text File Saved.", "#36BB00", ("Arial", 12), Window.notes_screen)
        elif option == 'bad-password':
            Interface.create_label("Your password should be at least 8 characters long, \n contain a combination of letters, numbers, and symbols, \n and should not include any personal information or common phrases.", "#E81500", ("Arial", 12), Window.register_screen, time=5000)


class AccountManagement(tk.Frame):
    def __init__(self):
        super().__init__()
        self.connect_to_database = sqlite3.connect("user-data.db")
        self.cursor = self.connect_to_database.cursor()
        self.create_database() # Construct the data base.

    def create_database(self):
        """ Creates a SQL database to store the user data. """
        # Check the table has been created.
        self.cursor.execute(f"PRAGMA table_info(accounts)")
        rows = self.cursor.fetchall()

        # Create the table if it is an empty database.
        if len(rows) <= 0:
            self.cursor.execute("CREATE TABLE accounts (username TEXT, password TEXT, uuid TEXT)")
            self.cursor.execute("CREATE TABLE notes (uuid TEXT, content TEXT, date DATETIME)")

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
            return True
        return False

    def check_password(self, password):
        """
        Check if the users password has a minimum of 8 characters, 
        combination of letters, numbers and symbols, no personal information,
        amd common phrases.
        """
        
        # Read in the common_words file:
        with open('common_words.txt', 'r') as f:
            common_words = f.read().splitlines()
        
        # Check if the password is at least 8 characters long.
        if len(password) < 8:
            return False
        # Check if the username is in the password.
        elif self.username in password:
            return False
        # Check if the password contains at least one number.
        elif not any(char.isdigit() for char in password):
            return False
        # Check if the password contains at least one letter.
        elif not any(char.isalpha() for char in password):
            return False
        # Check if the password contains at least one symbol.
        elif not any(char in '!@#$%^&*()_+-' for char in password):
            return False
        # Check if the password is a common word.
        elif password in common_words:
            return False
        # If all checks pass, return True
        else:
            return True        

    def register_user(self):
        """ Check if the user meets the requirements. """
        # Check if the username does not exist 
        if not self.user_exist(self.username): 
            # Check if the password meets the criteria.
            if self.check_password(self.password):
                # Add the user to the database
                self.add_to_database()    
            else:
                # Respond with a prompt on meeting the criteria.
                Interface.prompt_user("bad-password")  
        else:
            # Respond with a prompt on already being a user.
            Interface.prompt_user('user-taken')      

    def add_to_database(self):
        """ Register the new user into the database. """
        hashed_password = self.hash_password(self.password)
        insert_query = "INSERT INTO accounts (username, password, uuid) VALUES (?, ?, ?)"
        self.cursor.execute(insert_query, (self.username, hashed_password, str(uuid.uuid4())))
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

    def close_connection(self):
        """ Close the application and the database. """
        self.connect_to_database.close()
        self.master.destroy()

    def access_uuid(self, username: str) -> str: #TODO: type hinting?
        """ Access the users UUID. """
        select_query = "SELECT uuid FROM accounts WHERE username = ?"
        self.cursor.execute(select_query, (username,))
        uuid_id = self.cursor.fetchone()
        return uuid_id[0]

    def dashboard(self):
        """ Users dashboard. """
        note_management = NotesManagement()

        dashboard_screen = tk.Toplevel()
        dashboard_screen.title("Dashboard")
        dashboard_screen.geometry("350x250")
        
        # Send the UUID of the logged in user to the notes management.
        note_management.retrieve_uuid_id(self.access_uuid(self.username))

        tk.Label(dashboard_screen, text=f"Greetings, {self.username.capitalize()}!").pack()
        tk.Button(dashboard_screen, text="Create secret note", command=note_management.create_secret_notes).pack()
        tk.Button(dashboard_screen, text="View secret note", command=note_management.view_notes).pack()
        tk.Button(dashboard_screen, text="Delete secret note", command=note_management.delete_notes).pack()

class NotesManagement(tk.Frame):
    def __init__(self):
        super().__init__()
        self.connect_to_database = sqlite3.connect("user-data.db")
        self.cursor = self.connect_to_database.cursor()

    def retrieve_uuid_id(self, uuid):
        """ Get the user UUID. """
        self.uuid_id = uuid

    def delete_notes(self):
        self.note = tk.Toplevel()
        self.note.title("Delete")
        self.note.geometry("350x250")

    def delete_notes_message(self):
        pass

    def view_notes(self):
        """ View all the notes. """
        read_file_screen = tk.Toplevel()
        read_file_screen.title("Notes")
        read_file_screen.geometry("350x250")
        select_query = "SELECT content, date FROM notes WHERE uuid = ?"
        self.cursor.execute(select_query, (self.uuid_id, ))
        results = self.cursor.fetchall() 

        if results:
            count = 1
            for row in results:
                row = f"------Note: {count}------- \n {row[0]}, {row[1]}"
                tk.Label(read_file_screen, text=row, font=("arial", 15)).pack()
                count+=1
        else:
            tk.Label(read_file_screen, text="No data.", font=("arial", 15)).pack()

    def save_text(self, notes): # TODO: Encrypt the user notes with AES.
        """ Save the newly created notes. """
        insert_query = "INSERT INTO notes (uuid, content, date) VALUES (?, ?, ?)"
        date_time = datetime.datetime.now()
        self.cursor.execute(insert_query, (self.uuid_id, notes, date_time.strftime("%x")))
        self.connect_to_database.commit()

        # Confirm to the user that the data was saved successfully.
        Interface.prompt_user('notes-saved')

    def create_secret_notes(self):
        """ Creates a new note. """
        # Create the window for the creation of notes.
        Window.notes_screen = tk.Toplevel()
        Window.notes_screen.title("Make Notes")
        Window.notes_screen.geometry("350x250")

        # Create the text box for the user to write.
        tk.Label(Window.notes_screen, text="Enter secret notes: ").pack()
        text_box = tk.Text(Window.notes_screen, width=30, height=10)
        text_box.insert(tk.END, "Enter your notes here!") #FIXME: Remote this text box on click.
        text_box.config(state=tk.NORMAL)
        text_box.pack(expand=False)
        
        # Save the text.
        tk.Button(Window.notes_screen, text="Save", command=lambda: self.save_text(text_box.get("1.0", "end-1c"))).pack()

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
