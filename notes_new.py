import tkinter as tk
import os

class Register(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        
    def register_page(self):
        self.register_screen = tk.Toplevel(self.master)
        self.register_screen.title("Register")
        self.register_screen.geometry("350x250")
        self.register_screen.resizable(0,0)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        tk.Label(self.register_screen, text="Please enter your details").pack()
        tk.Label(self.register_screen, text="").pack()
        
        tk.Label(self.register_screen, text="Username").pack()
        self.entry_username = tk.Entry(self.register_screen, textvariable=self.username)
        self.entry_username.pack()
        
        tk.Label(self.register_screen, text="Password").pack()
        self.entry_password = tk.Entry(self.register_screen, textvariable=self.password)
        self.entry_password.pack()
        
        tk.Label(self.register_screen, text="").pack() 
        self.entry_password.config(show="*")
        
        # TODO: Change up the tk.Buttons to have eyes instead of a bar. 
        # tk.Button(self.register_screen, text="Show password!", height="1", width="12", command=lambda: self.password_show("show_register_password")).pack()
        # tk.Button(self.register_screen, text="Hide password!", height="1", width="12", command=lambda: self.password_show("hide_register_password")).pack()
        tk.Button(self.register_screen, text="Register", height="1", width="10", command=self.register_user).pack()
        
    def register_user( self ):
        username_info = self.username.get()
        password_info = self.password.get()
        
        try:
            os.makedirs(username_info)
            os.chdir(username_info)
            
            file = open(username_info, "w")
            file.write("Username:\n")
            file.write(username_info + "\n")
            file.write("Password:\n")
            file.write(password_info)
            file.close()
        except FileExistsError:
            self.register_screen.config(text='User Already Created!')
            
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

class Login(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        
    def login_verify( self ):
        get_username = self.user_verify.get()
        get_password = self.pass_verify.get()

        list_of_files = os.listdir("./test/")
        if get_username in list_of_files:
            self.file_name = str(get_username)
            
            # TODO: Remove after debugging is finished. 
            print("System: Debug file name " + self.file_name)
            
            # TODO: Files not saving in test.
            os.chdir("./test/" + self.file_name)
            
            file_open = open(get_username, "r")
            verify = file_open.read().splitlines()
            if get_password in verify:
                self.login_completed()
            else:
                tk.Label(self.login_screen, text="Password Error!", fg="#E81500", font=("Lato", 12)).pack()
        else:
            tk.Label(self.login_screen, text="User not found!", fg="#E81500", font=("Lato", 12)).pack()
            
    def login_completed( self ):
        self.dashboard_screen = tk.Toplevel(self.master)
        self.dashboard_screen.title("Dashboard")
        self.dashboard_screen.geometry("350x250")
        
        welcome_user = self.user_verify.get()
        
        tk.Label(self.dashboard_screen, text="Welcome to the dashboard " + welcome_user + "!").pack() 
        tk.Button(self.dashboard_screen, text="Create secret note", command=self.create_secret_notes).pack()
        tk.Button(self.dashboard_screen, text="View secret note", command=self.view_notes).pack()
        tk.Button(self.dashboard_screen, text="Delete secret note", command=self.delete_notes).pack()
        
    def login_page( self ):
        self.login_screen = tk.Toplevel(self.master)
        self.login_screen.title("Login")
        self.login_screen.geometry("350x250")
        self.login_screen.resizable(0,0)

        tk.Label(self.login_screen, text="Please enter your login details").pack()
        tk.Label(self.login_screen, text="").pack()
        
        self.user_verify = tk.StringVar()
        self.pass_verify = tk.StringVar()

        tk.Label(self.login_screen, text="Username").pack()
        self.entry_username1 = tk.Entry(self.login_screen, textvariable=self.user_verify)
        self.entry_username1.pack()
        
        tk.Label(self.login_screen, text="Password").pack()
        self.entry_password1 = tk.Entry(self.login_screen, textvariable=self.pass_verify)
        self.entry_password1.pack()
        
        tk.Label(self.login_screen, text="").pack()
        self.entry_password1.config(show="*")
        
        eye_icon_on = tk.PhotoImage(file="./assets/images/view.png")
        eye_icon_off = tk.PhotoImage(file="./assets/images/invisible.png")
        
        # TODO: Change up the tk.Buttons to have eyes instead of a bar. 
        # tk.Button(self.login_screen, image=eye_icon_on, height="25", width="25", command=lambda: self.password_show("show_login_password")).pack()
        # tk.Button(self.login_screen, image=eye_icon_off, height="1", width="10", command=lambda: self.password_show("hide_login_password")).pack()
        
        tk.Button(self.login_screen, text="Login", height="1", width="10", command=self.login_verify).pack()

class Notes(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        
    def save_file( self ):
        create_notes = self.file_name.get()
        get_notes = create_notes.get()
        
        data = open(self.file_name, "w")
        data.write(get_notes)
        data.close()
        
        tk.Label(self.notes_screen, text="Text File Saved", fg="#36BB00", font=("Lato", 12)).pack()
        
    def delete_notes( self ):
        self.register_screen0 = tk.Toplevel(self.master)
        self.register_screen0.title("Delete")
        self.register_screen0.geometry("350x250")
        
        list_files = os.listdir()
        
        tk.Label(self.register_screen0, text="Choose a filename to delete: ").pack()
        tk.Label(self.register_screen0, text=list_files).pack()
        
        self.delete_file = tk.StringVar()
        
        tk.Entry(self.register_screen0, textvariable=self.delete_file).pack()
        tk.Button(self.register_screen0, command=self.delete_notes_message, text="OK").pack()
        
    def delete_notes_message( self ):
        delete = self.delete_file.get()
        os.remove(delete)
        
        self.register_screen1 = tk.Toplevel(self.master)
        self.register_screen1.title("Notes")
        self.register_screen1.geometry("350x250")
        
        tk.Label(self.register_screen1, text=delete+" has been removed").pack()
        
    def create_secret_notes( self ):        
        self.file_name = tk.StringVar()
        create_notes = tk.StringVar()
        
        self.notes_screen = tk.Toplevel(self.master)
        self.notes_screen.title("Make Notes")
        self.notes_screen.geometry("350x250")
        
        tk.Label(self.notes_screen, text="Enter a filename: ").pack()
        tk.Entry(self.notes_screen, textvariable=self.file_name).pack()
        tk.Label(self.notes_screen, text="Enter secret notes: ").pack()
        tk.Entry(self.notes_screen, textvariable=create_notes).pack()
        tk.Button(self.notes_screen, text="Save", command=self.save_file).pack()
        
    def choose_files( self ):
        open_file_screen = tk.Toplevel(self.master)
        open_file_screen.title("Info")
        open_file_screen.geometry("350x250")
        
        list_files = os.listdir()
        
        tk.Label(open_file_screen, text="Choose a filename below: ").pack()
        tk.Label(open_file_screen, text=list_files).pack()
        
        self.file_name = tk.StringVar()
        
        tk.Entry(open_file_screen, textvariable=self.file_name).pack()
        tk.Button(open_file_screen, command=self.view_notes, text="OK").pack()
        
    def view_notes( self ):    
        read_file_screen = tk.Toplevel(self.master)
        read_file_screen.title("Notes")
        read_file_screen.geometry("350x250")    
        
        read_notes = open(self.file_name.get(), "r")
        data = read_notes.read()
        
        tk.Label(read_file_screen, text=data).pack()

class Main(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
    
    def screen( self ):        
        self.master.geometry("350x250")
        self.master.title("Secret Notes")
        self.master.iconphoto(True, tk.PhotoImage(file="./assets/images/favicon.png"))
        self.master.resizable(0,0)    
        
        tk.Label(text="Secret Notes", bg="#4BA400", fg="#FFFFFF", width="300", height="2", font=("Lato", 14)).pack()
        tk.Label(text="").pack()
        tk.Button(text="Login", height="1", width="25", font=("Lato", 12), command=self.login_page).pack()
        tk.Label(text="").pack()
        tk.Button(text="Register", height="1", width="25", font=("Lato", 12), command=self.register_page).pack()
                
# TODO: It should not inherit from TopLevel.
class MainApplication(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()