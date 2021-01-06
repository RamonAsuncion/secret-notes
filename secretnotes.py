from tkinter import *
import os

# Django and Flask are the most popular tools used to write an application server in Python


def register_user():

    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write("Username:\n")
    file.write(username_info + "\n")
    file.write("Password:\n")
    file.write(password_info)
    file.close()

    entry_username.delete(0, END)
    entry_password.delete(0, END)

    Label(screen1, text="Registration successful!",
          fg="green", font=("Lato", 12)).pack()


def destroyed():
    screen4.destroy()


def destroyed1():
    screen5.destroy()


def login_completed():
    session()


def saved():
    Label(screen7, text="Saved", fg="green", font=("Lato", 12)).pack()


def save():
    filename_get = raw_filename.get()
    notes_get = raw_notes.get()

    data = open(filename_get, "w")
    data.write(notes_get)
    data.close()

    saved()


def session():
    screen6 = Toplevel(screen)
    screen6.title("Dashboard")
    screen6.geometry("350x250")
    Label(screen6, text="Welcome to the dashboard").pack()
    Button(screen6, text="Create secret note",
           command=create_secret_notes).pack()
    Button(screen6, text="View secret note", command=view_notes).pack()
    Button(screen6, text="Delete secret note", command=delete_note).pack()


def delete_note():
    screen10 = Toplevel(screen)
    screen10.title("Delete")
    screen10.geometry("250x250")
    all_files = os.listdir()
    Label(screen10, text="Choose a filename to delete: ").pack()
    Label(screen10, text=all_files).pack()
    global raw_delete
    raw_delete = StringVar()
    Entry(screen10, textvariable=raw_delete).pack()
    Button(screen10, command=delete_note1, text="OK").pack()


def delete_note1():
    delete = raw_delete.get()
    os.remove(delete)
    screen11 = Toplevel(screen)
    screen11.title("Notes")
    screen11.geometry("400x400")
    Label(screen11, text=delete + " has been removed").pack()


def create_secret_notes():
    global raw_filename
    global raw_notes
    global screen7

    raw_filename = StringVar()
    raw_notes = StringVar()

    screen7 = Toplevel(screen)
    screen7.title("Make Notes")
    screen7.geometry("250x150")
    Label(screen7, text="Enter a filename: ").pack()
    Entry(screen7, textvariable=raw_filename).pack()
    Label(screen7, text="Enter secret notes: ").pack()
    Entry(screen7, textvariable=raw_notes).pack()
    Button(screen7, text="Save", command=save).pack()


def view_notes1():
    filename1 = raw_filename1.get()
    data = open(filename1, "r")
    data1 = data.read()
    screen9 = Toplevel(screen)
    screen9.title("Notes")
    screen9.geometry("400x400")
    Label(screen9, text=data1).pack()


def view_notes():
    screen8 = Toplevel(screen)
    screen8.title("Info")
    screen8.geometry("250x250")
    all_files = os.listdir()
    Label(screen8, text="Choose a filename below: ").pack()
    Label(screen8, text=all_files).pack()
    global raw_filename1
    raw_filename1 = StringVar()
    Entry(screen8, textvariable=raw_filename1).pack()
    Button(screen8, command=view_notes1, text="OK").pack()


def pass_not_recognized():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Retype pass!")
    screen4.geometry("250x150")
    Label(screen4, text="Password Error!").pack()
    Button(screen4, text="OK", command=destroyed).pack()


def user_not_found():
    global screen5
    screen5 = Toplevel(screen)
    screen5.title("Retype user!")
    screen5.geometry("250x150")
    Label(screen5, text="User not found!").pack()
    Button(screen5, text="OK", command=destroyed1).pack()


def login_verify():
    username1 = user_verify.get()
    password1 = pass_verify.get()

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()

        if password1 in verify:
            login_completed()
        else:
            pass_not_recognized()

    else:
        user_not_found()


def register_page():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("350x250")

    global username
    global password
    global entry_username
    global entry_password

    username = StringVar()
    password = StringVar()

    Label(screen1, text="Please enter your details").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Username * ").pack()
    entry_username = Entry(screen1, textvariable=username)
    entry_username.pack()
    Label(screen1, text="Password * ").pack()
    entry_password = Entry(screen1, textvariable=password)
    entry_password.pack()
    Label(screen1, text="").pack()
    entry_password.config(show="*")
    password_show = Button(screen1, text="Show password!",
                           height="1", width="12", command=buttonshow).pack()
    password_hide = Button(screen1, text="Hide password!",
                           height="1", width="12", command=buttonhide).pack()
    Button(screen1, text="Register", height="1",
           width="10", command=register_user).pack()


def buttonshow():
    entry_password.config(show="")


def buttonhide():
    entry_password.config(show="*")


def login_page():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("350x250")

    Label(screen2, text="Please enter your login details").pack()
    Label(screen2, text="").pack()

    global user_verify
    global pass_verify

    user_verify = StringVar()
    pass_verify = StringVar()

    global entry_username1
    global entry_password1

    Label(screen2, text="Username * ").pack()
    entry_username1 = Entry(screen2, textvariable=user_verify)
    entry_username1.pack()
    Label(screen2, text="Password * ").pack()
    entry_password1 = Entry(screen2, textvariable=pass_verify)
    entry_password1.pack()
    Label(screen2, text="").pack()
    entry_password1.config(show="*")

    password_show1 = Button(screen2, text="Show password!",
                            height="1", width="12", command=buttonshow1).pack()
    password_hide1 = Button(screen2, text="Hide password!",
                            height="1", width="12", command=buttonhide1).pack()

    Button(screen2, text="Login", height="1",
           width="10", command=login_verify).pack()


def buttonshow1():
    entry_password1.config(show="")


def buttonhide1():
    entry_password1.config(show="*")


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("350x250")
    screen.title("Secret Notes")
    Label(text="Secret Notes", bg="grey", width="300",
          height="2", font=("Lato", 12)).pack()
    Label(text="").pack()
    Button(text="Login", height="1", width="25", font=(
        "Lato", 12), command=login_page).pack()
    Label(text="").pack()
    Button(text="Register", height="1", width="25", font=(
        "Lato", 12), command=register_page).pack()

    screen.mainloop()


main_screen()
