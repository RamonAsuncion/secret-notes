#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import ttk
import sqlite3
import hashlib
import uuid
import datetime
from PIL import Image, ImageTk
from typing import Literal


class Setting:
    """A class for managing the settings of the application."""

    def __init__(self) -> None:
        pass

    def change_color(self, gui) -> None:
        """Change the color of the main screen window."""
        print("change color")


class Window:
    """A class for managing windows that are used throughout the program."""

    # Store the instance of the class once instantiated.
    __instance: Window | None = None

    @classmethod
    def get_instance(cls: Window) -> Window:
        """ Class method that returns the singleton instance of Window class.

        :param cls: a reference to the class.
        :return: None
        """
        if not cls.__instance:
            Window()
        return cls.__instance

    def __init__(self) -> None:
        """Creates a new instance of Window class and assigns it to Window.__instance
        and creates attributes for register_screen, login_screen, and notes_screen.

        :return: None
        """
        if Window.__instance is None:
            Window.__instance = self
            self.register_screen: tk.Toplevel | None = None
            self.login_screen: tk.Toplevel | None = None
            self.notes_screen: tk.Toplevel | None = None
        else:
            raise Exception("ERROR: This class is a singleton!")


class PromptUserInputs:
    """Provide response to the user"""

    def __init__(self) -> None:
        # A instance of the window management class.
        self.window: Window = Window.get_instance()

    @staticmethod
    def create_label(text: str, color: str, window, pack: bool = False) -> None:
        """Helper method to create a label that get's destroyed after a default of 1.5 second.

        :param str text: The text for the label.
        :param str color: The color of the label in hex.
        :param Entry window: The window the label will be created in.
        :param bool pack: Optional, determines if the label should be packed or gridded (defaults to False).
        :return: None
        """
        label: tk.Label = tk.Label(
            window, text=text, fg=color, font=("Arial", 12), width=25)
        label.after(1500, label.destroy)
        label.pack() if pack else label.grid(row=8, column=1)

    def prompt_user(self, option: str) -> None:
        """Prompt the user with prompts based on actions

        :param str option: The option to prompt the user with, should be one of the following:
            - 'fail-login'
            - 'user-taken'
            - 'registered'
            - 'notes-saved'
            - 'bad-password'

        :return: None
        """
        if option == 'fail-login':
            self.create_label("Please check login details.",
                              "#E81500", self.window.login_screen)
        elif option == 'user-taken':
            self.create_label("Username taken.", "#E81500",
                              self.window.register_screen)
        elif option == 'registered':
            self.create_label("Successfully registered.",
                              "#36BB00", self.window.register_screen)
        elif option == 'notes-saved':
            self.create_label("Text File Saved.", "#36BB00",
                              self.window.notes_screen, pack=True)
        elif option == 'bad-password':
            # Create a new top-level window.
            pass_req = tk.Toplevel()
            pass_req.title("Password Requirement")
            pass_req.geometry("300x150")
            pass_req.resizable(False, False)

            # Create a list of requirements for a strong password.
            requirements = [
                "Password is at least 8 characters long.",
                "Username is not in the password",
                "Password contains at least one number.",
                "Password contains at least one letter.",
                "Password contains at least one symbol.",
                "Password is not a common word."
            ]

            # Create a listbox widget to display the requirements.
            len_max = 0
            listbox = tk.Listbox(pass_req)
            for i in range(1, len(requirements)):
                current_requirement = requirements[i]
                if len(current_requirement) > len_max:
                    len_max = len(current_requirement)
                listbox.insert(i, f"{i}. {current_requirement}")

            # Configure the list-box's width and background.
            listbox.configure(width=len_max, background="#333333")
            listbox.pack()

            # Destroy the window after 7.5 seconds.
            pass_req.after(7500, pass_req.destroy)

            # Create an extra label on the window to make user aware password does not meet requirements.
            self.create_label("Password does not meet \n minimum requirement.",
                              "#E81500", self.window.register_screen)


class Interface(tk.Frame):
    """ A class for managing the graphical user interface."""

    def __init__(self, parent, *args, **kwargs) -> None:
        """Initialize the interface components of the application.

        :return: None
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Variables related to the login form.
        self.entry_username: tk.Entry | None = None
        self.entry_password: tk.Entry | None = None
        self.password_viewer: tk.Button | None = None

        # A instance of the window management class.
        self.window: Window = Window.get_instance()

        # A instance of the settings class.
        self.settings: Setting = Setting()

        # A reference to the password viewer image.
        self.photo_image: ImageTk.PhotoImage = self.update_password_image()

        # Setup the main window.
        self.main_screen()

    def main_screen(self) -> None:
        """Creates the interface for the main screen

        :return: None
        """
        self.parent.title("Secret Notes")
        self.parent.geometry("350x250")

        # Default color of the UI.
        ui_color: str = "#4BA400"

        image_name = "settings"
        img = Image.open(f'assets/images/{image_name}.png').resize((20, 20))
        image = ImageTk.PhotoImage(img)
        setting_button = tk.Button(root, image=image, bg=ui_color, 
                command=self.settings.change_color)
        setting_button.image = image
        setting_button.pack(side='top', anchor='ne')

        # Title.
        tk.Label(text="Secret Notes", bg=ui_color, fg="#FFFFFF", width="300",
                 height="2", font=("Arial", 14)).pack()
        tk.Label(text="").pack()

        # Login button.
        tk.Button(text="Login", height="1", width="25", font=("Arial", 12),
                  command=self.login_page).pack()
        tk.Label(text="").pack()

        # Register button.
        tk.Button(text="Register", height="1", width="25", font=("Arial", 12),
                  command=self.register_page).pack()

    def register_page(self) -> None:
        """Creates the interface for the registration screen

        :return: None
        """
        self.window.register_screen = tk.Toplevel()
        self.close_window(self.window.login_screen)
        self.create_page(self.window.register_screen, login_screen=False)

    def login_page(self) -> None:
        """Creates the interface for the login screen

        :return: None
        """
        self.window.login_screen = tk.Toplevel()
        self.close_window(self.window.register_screen)
        self.create_page(self.window.login_screen)

    @staticmethod
    def close_window(window) -> None:
        """ Close a specific window.

        :param Toplevel window: tkinter toplevel window object
        :return: None
        """
        if window is None:
            return
        window.destroy()

    def create_page(self, window, login_screen: bool = True) -> None:
        """Creates a user interface for entry based on the screen type

        :param Toplevel window: tkinter toplevel window object
        :param bool login_screen: determine whether it is a login screen or not (Default value = True)
        :return: None
        """
        # Check if the current window is a login or registration screen.
        if login_screen:
            entry_point = "Login"
        else:
            entry_point = "Registration"

        # Creates the window for the login screen.
        window.title(entry_point)
        window.geometry("350x250")

        # Configure the width of the columns.
        window.columnconfigure(0, weight=2)
        window.columnconfigure(3, weight=1)

        # The header for the current window.
        header = tk.Label(
            window, text=f"Enter your {entry_point.lower()} details:")
        header.grid(row=0, column=1)
        tk.Label(window, text="").grid(row=1, column=1)

        # Instantiate StringVar objects to handle the username and password of the entries.
        username: tk.StringVar = tk.StringVar()
        password: tk.StringVar = tk.StringVar()

        # Create a username entry for the user to interact.
        tk.Label(window, text="Username").grid(row=2, column=1)
        self.entry_username = tk.Entry(window, textvariable=username)
        self.entry_username.grid(row=3, column=1, sticky="news")

        # Create a password entry for the user to interact.
        tk.Label(window, text="Password").grid(row=4, column=1)
        bullet = "\u2022"  # Specifies bullet character.
        self.entry_password = tk.Entry(
            window, show=bullet, textvariable=password)
        self.entry_password.grid(row=5, column=1, sticky="news")

        # Create a password viewer button to show and hide the password on the password entry.
        self.password_viewer = tk.Button(window, bg="#333333", image=self.photo_image,
                                                    command=lambda: self.password_show(self.entry_password))
        self.password_viewer.grid(row=5, column=2, sticky="we")

        # Submit button to send the credentials the account management class.
        tk.Label(window, text="").grid(row=6, column=1)

        submit_button: tk.Button = tk.Button(window, text="Submit", height="1", width="10",
                                             command=lambda: self.send_credentials(username.get(), password.get(), login_screen))

        # Allow the user to press enter on the password entry to submit.
        self.entry_password.bind("<Return>", lambda _:
                                 self.send_credentials(username.get(), password.get(), login_screen))

        submit_button.grid(row=7, column=1)

    def send_credentials(self, username: str, password: str, login_flag: bool) -> None:
        """Sends user information to the account management system

        :param str password: the user submitted password.
        :param str username: the user submitted username.
        :param bool login_flag: whether the window is the login or registration page.
        :return: None
        """
        # Send the credentials.
        AccountManagement(self.parent).receive_credentials(
            username, password, login_flag)
        self.clear_user_forum(self.entry_username, self.entry_password)

    def clear_user_forum(self, entry_user: tk.Entry | None, entry_pass: tk.Entry | None) -> None:
        """Delete the username and password on the entry box once submitted. 

        :param Entry entry_user: the entry box for the username.
        :param Entry entry_pass: the entry box for the password.
        :return: None
        """
        if entry_user:
            entry_user.delete(0, tk.END)
        if entry_pass:
            entry_pass.delete(0, tk.END)

    def password_show(self, entry_password: tk.Entry | None) -> None:
        """Show to users password

        :param Entry entry_password: an entry box specifically for a password that has
            been configured with the bullet character (\u2022).
        :return: None
        """
        if entry_password is None:
            return

        bullet: str = "\u2022"
        if entry_password.cget('show') == bullet:
            entry_password.config(show='')
            view = "hide"
        else:
            entry_password.config(show=bullet)
            view = "view"

        # Update the image of the password viewer icon.
        self.photo_image = self.update_password_image(view)
        self.password_viewer.configure(image=self.photo_image)

    @staticmethod
    def update_password_image(option: str = "view") -> ImageTk.PhotoImage:
        """This function loads an image from the assets folder and resizes
        it to a specified width and height before returning it as a tkinter PhotoImage.

        :param str option: is a string that specifies whether the user wishes to view or hide the password
            (Default value = "view")
            - 'view'
            - 'hide'

        :return: PhotoImage: the new image.
        """
        image_name: Literal['invisible',
                            'view'] = "invisible" if option == "hide" else "view"
        img = Image.open(f'assets/images/{image_name}.png').resize((20, 20))
        return ImageTk.PhotoImage(img)


class AccountManagement(tk.Frame):
    """ A class for managing user account data stored in a database. """

    def __init__(self, parent) -> None:
        """Initialize the account management system of the application.

        :param parent: the parent window.

        :return: None
        """
        super().__init__()
        # Variables related to the users login detail.
        self.username: str = ""
        self.password: str = ""

        self.parent = parent

        # The creation of the account database.
        self.connect_to_database: sqlite3.Connection = sqlite3.connect(
            "user-data.db")
        self.cursor: sqlite3.Cursor = self.connect_to_database.cursor()
        self.create_database()  # Construct the database.

        # Provide feedback to the user when certain actions are done.
        self.interface = PromptUserInputs()

        # Close the database on close of the application.
        parent.protocol("WM_DELETE_WINDOW", self.close_connection)

    def create_database(self) -> None:
        """Creates a SQL database to store the user data.

        :return: None
        """
        # Create the table if it is an empty database.
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS accounts (username TEXT, password TEXT, uuid TEXT)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS notes (uuid TEXT, content TEXT, date DATETIME)')

    def receive_credentials(self, username: str, password: str, login_flag: bool) -> None:
        """Retrieve the user data from the text boxes.

        :param str password: the user submitted password.
        :param str username: the user submitted username.
        :param bool login_flag: whether the user is submitting the password through the login
            or registration page.
        :return: None
        """
        self.username: str = username.lower()
        self.password: str = password

        if login_flag:
            self.login_verify(self.username, self.password)
        else:
            self.register_user(self.username, self.password)

    def user_exist(self, username: str) -> bool:
        """Check is the username is already taken.

        :param str username: the user submitted username.
        :return: bool: a boolean indicating if the user already exists.
        """
        search_query = "SELECT * FROM accounts WHERE username = ?"
        self.cursor.execute(search_query, (username.lower(),))
        return True if self.cursor.fetchone() is not None else False

    def check_password(self, password: str) -> bool:
        """Check if the users password has a minimum of 8 characters,
        combination of letters, numbers and symbols, no personal information,
        amd common phrases.

        :param str password: the password to be evaluated.
        :return: bool: a boolean indicating if the password meets the
            minimum requirements.
        """
        if password is None:
            raise ValueError('Password cannot be None.')

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

    def register_user(self, username: str, password: str) -> None:
        """Check if the user meets the requirements.

        :param str username: the user submitted username.
        :param str password: the user submitted password.
        :return: None
        """
        # Check if the username does not exist
        if not self.user_exist(username):
            # Check if the password meets the criteria.
            if self.check_password(password):
                # Add the user to the database
                self.add_to_database()
            else:
                # Respond with a prompt on meeting the criteria.
                self.interface.prompt_user("bad-password")
        else:
            # Respond with a prompt on already being a user.
            self.interface.prompt_user('user-taken')

    def add_to_database(self) -> None:
        """Register the new user into the database.

        :return: None
        """
        hashed_password = self.hash_password(self.password)
        insert_query = "INSERT INTO accounts (username, password, uuid) VALUES (?, ?, ?)"
        self.cursor.execute(insert_query, (self.username,
                            hashed_password, str(uuid.uuid4())))
        self.connect_to_database.commit()
        self.interface.prompt_user('registered')

    def login_verify(self, username: str, password: str) -> None:
        """Verify the user data to proceed with login.

        :param str username: the user submitted username.
        :param str password: the user submitted password.
        :return: None
        """
        # Compare the submitted data to the database.
        hashed_password = self.hash_password(password)
        select_query = "SELECT * FROM accounts WHERE username = ? AND password = ?"
        self.cursor.execute(select_query, (username, hashed_password))
        result = self.cursor.fetchone()

        # Proceed to the dashboard if the login was successful.
        self.dashboard() if result else self.interface.prompt_user('fail-login')

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the users password.

        :param str password: the user submitted password.
        :return: str: the hashed form of the password.
        """
        if password is None:
            return

        # Use the SHA-256 algorithm to generate a cryptographic hash
        hash_object = hashlib.sha256(password.encode())

        # Return the hexadecimal representation of the hash
        return hash_object.hexdigest()

    def close_connection(self):
        """Close the application and the database."""
        self.connect_to_database.close()
        self.parent.destroy()

    def access_uuid(self, username: str) -> str:
        """Access the users UUID.

        :param str username: the user submitted username.
        :return: str: the user's UUID.
        """
        if username is None:
            raise ValueError("Username cannot be None.")

        select_query = "SELECT uuid FROM accounts WHERE username = ?"
        self.cursor.execute(select_query, (username,))
        uuid_id: tuple = self.cursor.fetchone()
        return uuid_id[0]

    def dashboard(self) -> None:
        """Users dashboard.

        :return: None
        """
        note_management = NoteManagement(self.parent)

        dashboard_screen = tk.Toplevel()
        dashboard_screen.title("Dashboard")
        dashboard_screen.geometry("350x250")

        # Send the UUID of the logged-in user to the note management.
        note_management.retrieve_uuid_id(self.access_uuid(self.username))

        # Display different options to the user on how to manage their notes.
        tk.Label(dashboard_screen,
                 text=f"Greetings, {self.username.capitalize()}!").pack()
        tk.Button(dashboard_screen, text="Create secret note",
                  command=note_management.create_secret_notes).pack()
        tk.Button(dashboard_screen, text="View secret note",
                  command=note_management.view_notes).pack()
        tk.Button(dashboard_screen, text="Delete secret note",
                  command=note_management.view_delete_notes).pack()


class NoteManagement(tk.Frame):
    """ A class for managing notes stored in a database. """

    def __init__(self, parent) -> None:
        """Initialize the note management components of the application.

        :return: None
        """
        super().__init__()
        # The creation of the account database.
        self.connect_to_database = sqlite3.connect("user-data.db")
        self.cursor = self.connect_to_database.cursor()
        self.window = Window.get_instance()

        # Provide feedback to the user when certain actions are done.
        self.interface = PromptUserInputs()

    def retrieve_uuid_id(self, uuid: str) -> None:
        """Get the user UUID.

        :param uuid: the user's UUID.
        :return: None
        """
        self.uuid_id = uuid

    def view_delete_notes(self) -> None:
        """View the set of notes scheduled to be deleted in a tree view.

        :return: None
        """
        # Create the window.
        delete_note_screen = tk.Toplevel()
        delete_note_screen.title("Delete")
        delete_note_screen.geometry("350x250")

        # Change the style of the table.
        ttk.Style().configure("Treeview", background="#333333",
                              foreground="white", fieldbackground="333333")

        # Create a treeview with 2 columns
        tree = ttk.Treeview(delete_note_screen, columns=(
            "note", "date"), show="headings")

        # Create the Scrollbar widget
        scrollbar = ttk.Scrollbar(
            delete_note_screen, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Set the yscrollcommand of the Treeview widget to the Scrollbar set.
        tree.configure(yscrollcommand=scrollbar.set)

        # Set the column width
        tree.column("date", width=50)

        # Set column headings
        tree.heading("note", text="Note")
        tree.heading("date", text="Date")

        # Create a query to select all notes from the database
        select_query = "SELECT content, date FROM notes"

        # Execute the query and select the results
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()

        # Insert the results into the treeview
        for row in rows:
            tree.insert('', tk.END, values=row)

        # Set the treeview
        tree.pack(expand=tk.YES, fill=tk.BOTH)

        # Button to delete the selected content.
        delete_button = tk.Button(delete_note_screen, text="Delete",
                                  command=lambda: self.delete_note(tree))
        delete_button.pack(side=tk.BOTTOM)

    def delete_note(self, current_tree: ttk.Treeview) -> None:
        """Delete a note from a database based on a treeview selection.

        :param current_tree: A reference to the treeview widget.
        :return: None
        """
        # Check if a row is selected.
        if not current_tree.selection():
            return

        # Get the selected item
        selected_item = current_tree.selection()[0]

        # Get the item's value
        item_value = current_tree.item(selected_item)['values']

        # Get the note content
        note = item_value[0]

        # Execute to delete query based on the note content
        delete_query = "DELETE FROM notes WHERE content = ?"
        self.cursor.execute(delete_query, (note,))
        self.connect_to_database.commit()

        # Refresh the treeview
        current_tree.delete(selected_item)

    def view_notes(self) -> None:
        """View all the notes.

        :return: None
        """
        read_file_screen = tk.Toplevel()
        read_file_screen.title("Notes")
        read_file_screen.geometry("350x250")
        select_query = "SELECT content, date FROM notes WHERE uuid = ?"
        self.cursor.execute(select_query, (self.uuid_id,))
        results = self.cursor.fetchall()

        # TODO: Make this into a tree view.
        if results:
            count = 1
            for row in results:
                message = f"{row[0]}, {row[1]} \n"
                tk.Label(read_file_screen, text=message,
                         font=("arial", 15)).pack()
                count += 1
        else:
            tk.Label(read_file_screen, text="No data.",
                     font=("arial", 15)).pack()

    def save_text(self, notes: str) -> None:
        """Save the newly created notes.

        :param str notes:
        :return: None
        """
        insert_query = "INSERT INTO notes (uuid, content, date) VALUES (?, ?, ?)"
        date_time = datetime.datetime.now()
        self.cursor.execute(insert_query, (self.uuid_id,
                            notes, date_time.strftime("%x")))
        self.connect_to_database.commit()

        # Confirm to the user that the data was saved successfully.
        self.interface.prompt_user('notes-saved')

    def create_secret_notes(self) -> None:
        """Creates a new note.

        :return: None
        """
        # Create the window for the creation of notes.
        self.window.notes_screen = tk.Toplevel()
        self.window.notes_screen.title("Make Notes")
        self.window.notes_screen.geometry("350x250")

        # Create the text box for the user to write.
        tk.Label(self.window.notes_screen, text="Enter secret notes: ").pack()
        text_box = tk.Text(self.window.notes_screen, width=30, height=10)
        text_box.insert(tk.END, "Enter your notes here!")
        text_box.config(state=tk.NORMAL)
        text_box.pack(expand=False)

        # Clear the text box once clicked.
        text_box.bind("<Button-1>", lambda _: self.clear_text(text_box))
        text_box.focus_set()

        # Save the text.
        tk.Button(self.window.notes_screen, text="Save", command=lambda: self.save_text(
            text_box.get("1.0", "end-1c"))).pack()

    @staticmethod
    def clear_text(entry: tk.Text) -> None:
        """ Clears the text off an entry.

        :param Text entry: the text in a text box to be deleted.
        :return: None
        """
        if entry is None:
            return

        entry.delete('1.0', tk.END)


class MainApplication(tk.Frame):
    """ Initialize all the components to the secret note app. """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.interface = Interface(parent)
        self.account_management = AccountManagement(parent)
        self.note_management = NoteManagement(parent)


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
