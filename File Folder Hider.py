# Programmed by: Mubashir Ahmed OR known as Mubashir78 on GitHub
# https://www.github.com/Mubashir78

import re, os, sys, base64, yagmail
from datetime import date, datetime
from os import lstat
from os.path import getsize as file_size
from os.path import isdir, isfile, join
from pathlib import Path
from random import randint
from stat import FILE_ATTRIBUTE_HIDDEN as H
from tkinter import Button, Entry, Label, StringVar, TclError, Tk, filedialog
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning
from idlelib.tooltip import Hovertip
from win32api import GetFileAttributes

# Current date
today = date.today().strftime("%d-%b-%Y")

# Current time
cur_t = datetime.today().strftime("%I:%M %p")

WIDTH, HEIGHT = 500, 300

# Makes sure that the files below are created in the same directory as the script
log_file, pass_file = Path(__file__).with_name('log.txt'), Path(__file__).with_name('passw.pass')

fi_fo_path = txt_input = conf_exit = None

class Error:
    file_path_er = "File/Folder not found. Please make sure to type the path correctly."
    dialog_box_hide_exit_er = "You exited the dialog box. Please try again."
    invalid_email_format_er = "The email you have entered is of invalid format. Please try again."

class Email:
    """
    Send a Master Password Recovery Code through Gmail to the user email address
    provided while creating/changing the Master Password.
    """
    def __init__(self):
        self.recovery_code = randint(100000,999999)
        self.sender = "filefolderhider@gmail.com"

        with open(pass_file, "rb") as file:
            text = file.readlines()

        user_email = base64.b64decode(text[2]).decode("utf-8")
        self.receiver = user_email
        self.subject = "Recovery code for changing Master Password"
        self.body = f"""\
        Greetings from File Folder Hider! Following is the recovery code asked for changing your Master Password:

        {self.recovery_code}

        If it wasn't you who requested the recovery code, please open File Folder Hider and change your Master Password ASAP.

        Thank you,
        Mubashir78.
        https://www.github.com/Mubashir78"""

    

    def passw_recovery_email(self):
        conf = askquestion(title="Master Password Recovery",
                           message=f"An email will be sent to {self.receiver} containing the recovery code for changing the Master Password.\n\nDo you wish to continue?")
        
        if conf == "yes":
            sys_show(pass_file)
            with open(pass_file, "rb") as file:
                text = file.readlines()
            sys_hide(pass_file)

            enc_password = text[1]
            gmail_password = base64.b64decode(enc_password).decode("utf-8")

            gmail = yagmail.SMTP({self.sender : "File Folder Hider"}, gmail_password)
            gmail.send(to=self.receiver,
                       subject=self.subject,
                       contents=self.body)

            showinfo(title="Recovery Email Sent",
                     message="Recovery email has been sent successfully.\nPlease check for it in your inbox and enter\nthe recovery code in the next dialog box.")

            return win_pass_2.destroy(), dialog_box_recover_mas_pass(self.recovery_code)

        else: del self


def recov_code():
    email = Email()
    return email.passw_recovery_email()

def no_email_info():
    return showerror(title="No Email Found",
                     message="You have not provided your email address.\nTo access the Master Password Recovery feature, please enter your email address while creating/changing the Master Password."), txt_box_2.focus_force()


def center(win, win_width, win_height):
    WIN_WIDTH, WIN_HEIGHT = win_width, win_height
    WIDTH = win.winfo_screenwidth()
    HEIGHT = win.winfo_screenheight()
    X = (WIDTH / 2) - (WIN_WIDTH / 2)
    Y = (HEIGHT / 2) - (WIN_HEIGHT / 2)
    return WIN_WIDTH, WIN_HEIGHT, X, Y

# There are 5 dialog boxes in total for now

def dialog_box_menu():
    global win, label, label_2, button_h, button_uh, button_sh_log, button_del_log, button_exit

    # --WIN SECTION--
    win = Tk()
    win.attributes("-topmost", True)
    win.resizable(width=False, height=False)
    win.eval('tk::PlaceWindow . center')
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win, WIDTH, HEIGHT)
    win.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win.title("File/Folder Hider")
    win.configure(bg="gray")

    #--LABELS SECTION--
    label = Label(text="============== Main Menu ==============", font=("Calibri", 19, "bold"), bg="gray")
    intro_txt = StringVar(win, "Welcome To File/Folder Hider!\nHere you can hide and unhide your files and/or folders.\n\nPlease press one of the buttons below\nto use the File/Folder Hider:")
    label_2 = Label(textvariable=intro_txt, font=("Calibri", 14), width=50, bg="darkgray")
    
    #--BUTTONS SECTION--
    button_h = Button(text="Hide", font=("Calibri",17), bg="darkgray", command=lambda:[win.destroy(), dialog_box_hide()])
    button_h.config(width = 7, height = 1, relief="groove")
    button_h.bind("<Enter>", lambda x: [button_h.config(relief="raised")])
    button_h.bind("<Leave>",lambda x: [button_h.config(relief="groove")])

    button_uh = Button(text="Unhide", font=("Calibri",17), bg="darkgray", command=lambda:[win.destroy(), dialog_box_unhide()])
    button_uh.config(width = 7, height = 1, relief="groove")
    button_uh.bind("<Enter>", lambda x: [button_uh.config(relief="raised")])
    button_uh.bind("<Leave>", lambda x: [button_uh.config(relief="groove")])

    button_sh_log = Button(text="Show Log", font=("Calibri",16), bg="darkgray", command=show_log)
    button_sh_log.config(width = 8, height = 1, relief="groove")
    button_sh_log.bind("<Enter>", lambda x: [button_sh_log.config(relief="raised")])
    button_sh_log.bind("<Leave>", lambda x: [button_sh_log.config(relief="groove")])

    button_del_log = Button(text="Clear Log", font=("Calibri",16), bg="darkgray", command=clear_log)
    button_del_log.config(width = 8, height = 1, relief="groove")
    button_del_log.bind("<Enter>", lambda x: [button_del_log.config(relief="raised")])
    button_del_log.bind("<Leave>", lambda x: [button_del_log.config(relief="groove")])

    button_exit = Button(text="Exit", font=("Calibri",14), bg="darkgray", command=lambda:[exit_dialog_box(win, dialog_box_menu)])
    button_exit.config(width = 6, height = 1, relief="groove")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_change_mas_pass = Button(text="Change Master Password", font=("Calibri", 9), bg="darkgray", command=change_mas_pass)
    button_change_mas_pass.config(width = 24, height = 1, relief="groove")
    button_change_mas_pass.bind("<Enter>", lambda x: [button_change_mas_pass.config(relief="sunken")])
    button_change_mas_pass.bind("<Leave>", lambda x: [button_change_mas_pass.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    button_change_mas_pass.grid(row = 0, column = 0, columnspan = 2, ipady = 3, padx=(2,0), pady = 5, sticky="NW")
    button_exit.grid(row = 0, column = 3, padx = (0,5), pady = 5, sticky='NE')
    label.grid(row = 1, column = 0, columnspan = 4, pady = (8,5))
    label_2.grid(row = 2, column = 0, columnspan = 4, pady = (8,13))
    button_h.grid(row = 3, column = 0, ipadx = 6, ipady = 5, pady = (5,5), sticky='S')
    button_uh.grid(row = 3, column = 1, ipadx = 6, ipady = 5, padx = (0,10), pady = (5,5), sticky='S')
    button_sh_log.grid(row = 3, column = 2, ipadx = 6, ipady = 7, padx = (10,0), pady = (5,5), sticky='S')
    button_del_log.grid(row = 3, column = 3, ipadx = 6, ipady = 7, pady = (5,5), sticky='S')

    #--GRID CONFIGURE SECTION--
    win.grid_rowconfigure(1, weight=2)
    win.grid_rowconfigure(2, weight=2)
    win.grid_rowconfigure(3, weight=1)

    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)
    win.grid_columnconfigure(2, weight=1)
    win.grid_columnconfigure(3, weight=1)

    win.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win, dialog_box_menu))
    win.mainloop()


def dialog_box_hide():
    global win_h, text_h, txt_box_h, button_fi, button_fo, button_exit, button_exit_menu

    #--WIN_H SECTION--
    win_h = Tk()
    win_h.attributes("-topmost", True)
    win_h.resizable(width=False, height=False)
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_h, WIDTH, HEIGHT)
    win_h.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_h.title("Dialog Box: Hide")
    win_h.configure(bg="gray")

    #--LABELS SECTION--
    label = Label(text="================= Hide =================", font=("Calibri", 19, "bold"), bg="gray")

    hide_txt = StringVar(win_h, "Enter the full path to the file/folder you wish to hide,\nor press one of the two buttons below to select from the File Explorer:")
    label_2 = Label(textvariable=hide_txt, font=("Calibri",11), width=60, bg="darkgray")

    #--ENTRY BOX SECTION--
    text_h = StringVar(win_h)
    txt_box_h = Entry(win_h, textvariable=text_h, width = 60, justify="center")
    text_h.trace_add("write", lambda x,y,z: txt_box_change(button=button_h, text=text_h))
    txt_box_h.bind("<Return>", lambda x: get_txt_input(text=text_h, opr='hide'))

    #--BUTTONS SECTION--
    button_h = Button(text="Hide", font=("Calibri",12), bg="darkgray", command= lambda : get_txt_input(text=text_h, opr='hide'))
    button_h.config(width = 8, height = 1, relief="groove", state="disabled")

    button_fi = Button(text="Hide a File", font=("Calibri",15), bg="darkgray", command=open_file)
    button_fi.config(width = 11, height = 1, relief="groove")
    button_fi.bind("<Enter>", lambda x: [button_fi.config(relief="raised")])
    button_fi.bind("<Leave>", lambda x: [button_fi.config(relief="groove")])

    button_fo = Button(text="Hide a Folder",font=("Calibri",15), bg="darkgray", command=open_folder)
    button_fo.config(width = 11, height = 1, relief="groove")
    button_fo.bind("<Enter>", lambda x: [button_fo.config(relief="raised")])
    button_fo.bind("<Leave>", lambda x: [button_fo.config(relief="groove")])

    button_exit = Button(text="Exit", font=("Calibri", 13), bg="darkgray", command=lambda:[exit_dialog_box(win_h, dialog_box_hide)])
    button_exit.config(width = 6, height = 1, relief="groove")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_exit_menu = Button(text="Exit To Main Menu", font=("Calibri",12), bg="darkgray", command=lambda: [win_h.destroy(), dialog_box_menu()])
    button_exit_menu.config(width = 15, height = 1, relief="groove")
    button_exit_menu.bind("<Enter>", lambda x: [button_exit_menu.config(relief="sunken")])
    button_exit_menu.bind("<Leave>", lambda x: [button_exit_menu.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    button_exit.grid(row = 0, column = 2, padx = 5, pady = 5, sticky='NE')
    button_exit_menu.grid(row = 1, column = 2, padx = 5, sticky='E')
    label.grid(row = 2, column = 0, columnspan = 3)
    label_2.grid(row = 3, column = 0, columnspan = 3)
    txt_box_h.grid(row = 4, column = 0, columnspan = 3, padx = (5,75))
    button_h.grid(row = 4, column = 2, padx = (25,8), sticky='E')
    button_fi.grid(row = 5, column = 0, ipadx = 8,ipady = 3, padx = (5,5), pady = (0,5), sticky='SE')
    button_fo.grid(row = 5, column = 2, ipadx = 8,ipady = 3, pady = (0,5), sticky='SW')

    #--GRID CONFIGURE SECTION--
    win_h.grid_rowconfigure(2, weight=2)
    win_h.grid_rowconfigure(3, weight=2)
    win_h.grid_rowconfigure(4, weight=1)
    win_h.grid_rowconfigure(5, weight=1)

    win_h.grid_columnconfigure(0, weight=1)
    win_h.grid_columnconfigure(1, weight=2)
    win_h.grid_columnconfigure(2, weight=1)

    txt_box_h.focus_force()
    win_h.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win_h, dialog_box_hide))
    win_h.mainloop()


def dialog_box_unhide():

    global win_uh, button_op_log, button_uh, txt_box_uh, fi_fo_path, button_exit, button_exit_menu, txt_input

    #--WIN_UH SECTION--
    win_uh = Tk()
    win_uh.attributes("-topmost", True)
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_uh, WIDTH, HEIGHT)    
    win_uh.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_uh.resizable(width=False, height=False)
    win_uh.title("Dialog Box: Unhide")
    win_uh.configure(bg="gray")
    
    #--LABELS SECTION--
    label = Label(text="================ Unhide ================", font=("Calibri", 19, "bold"), bg="gray")

    label_2 = Label(text="Open the log file to check the full path to the file/folder\nyou want to unhide and copy/paste it below:", font=("Calibri", 14), width=50, bg="darkgray")
    
    #--ENTRY BOX SECTION--
    text_uh = StringVar(win_uh)
    txt_box_uh = Entry(win_uh, textvariable=text_uh, width = 70, justify="center")
    text_uh.trace_add("write", lambda x,y,z: txt_box_change(button=button_uh, text=text_uh))
    txt_box_uh.bind("<Return>", lambda x: get_txt_input(text=text_uh, opr='unhide'))
    
    #--BUTTONS SECTION--
    button_op_log = Button(text="Open Log File", font=("Calibri", 16), bg="darkgray", command=lambda :[os.startfile(log_file)])
    button_op_log.config(width = 12, height = 1, relief="groove")
    button_op_log.bind("<Enter>", lambda x: [button_op_log.config(relief="raised")])
    button_op_log.bind("<Leave>", lambda x: [button_op_log.config(relief="groove")])

    button_uh = Button(text="Unhide", font=("Calibri", 16), bg="darkgray", command = lambda : get_txt_input(text=text_uh, opr='unhide'))
    button_uh.config(width = 11, height = 1, relief="groove", state="disabled")

    button_exit = Button(text="Exit", font=("Calibri", 13), bg="darkgray", command=lambda :[exit_dialog_box(win_uh, dialog_box_unhide)])
    button_exit.config(width = 6, height = 1, relief="groove")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_exit_menu = Button(text="Exit To Main Menu", font=("Calibri",12), bg="darkgray", command=lambda: [win_uh.destroy(), dialog_box_menu()])
    button_exit_menu.config(width = 16, height = 1, relief="groove")
    button_exit_menu.bind("<Enter>", lambda x: [button_exit_menu.config(relief="sunken")])
    button_exit_menu.bind("<Leave>", lambda x: [button_exit_menu.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    button_exit.grid(row = 0, column = 2, padx = 5, pady = 5, sticky='NE')
    button_exit_menu.grid(row = 1, column = 2, padx = 5, sticky='E')
    label.grid(row = 2, column = 0, columnspan = 3, pady=(2,2))
    label_2.grid(row = 3, column = 0, columnspan = 3, pady = (2,3))
    txt_box_uh.grid(row = 4, column = 0, columnspan = 3, pady = (7,7))
    button_op_log.grid(row = 5, column = 0, padx=(0,5), pady = (0,5), sticky='S')
    button_uh.grid(row = 5, column = 2, pady = (0,5), sticky='S')

    #--GRID CONFIGURE SECTION--
    win_uh.grid_rowconfigure(2, weight=2)
    win_uh.grid_rowconfigure(3, weight=2)
    win_uh.grid_rowconfigure(4, weight=2)
    win_uh.grid_rowconfigure(5, weight=1)

    win_uh.grid_columnconfigure(0, weight=1)
    win_uh.grid_columnconfigure(1, weight=2)
    win_uh.grid_columnconfigure(2, weight=1)

    txt_box_uh.focus_force()
    win_uh.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win_uh, dialog_box_unhide))
    win_uh.mainloop()


def create_pass_dialog_box():
    global win_pass, mas_pass, entry_box_pass, entry_box_conf_pass, entry_box_email

    #--WIN_PASS SECTION--
    win_pass = Tk()
    win_pass.attributes("-topmost", True)
    win_pass.resizable(width=False, height=False)
    win_pass.eval('tk::PlaceWindow . center')
    win_pass.title("Create Password")
    win_pass.configure(bg="gray")

    #--LABELS SECTION--
    label = Label(text="Enter a strong password (Email is optional):", font=("Calibri", 16, "bold"), width=50, bg="darkgray", fg="black")
    label_pass = Label(text="Password:", font=("Calibri", 15, "bold"), bg="darkgray")
    label_conf_pass = Label(text="Confirm Password:", font=("Calibri", 12, "bold"), bg="darkgray")
    label_email = Label(text="Email (For Password Recovery):", font=("Calibri", 9, "bold"), bg="darkgray")

    #--STRINGVAR SECTION--
    mas_pass = StringVar(win_pass)
    conf_mas_pass = StringVar(win_pass)
    email = StringVar(win_pass)

    #--ENTRY BOXES SECTION--
    entry_box_pass = Entry(win_pass, textvariable=mas_pass, width=55, justify="center")
    mas_pass.trace_add("write", lambda x,y,z: txt_box_change(button=button, text=mas_pass))
    entry_box_pass.bind("<Return>", lambda x: entry_box_conf_pass.focus_force())

    entry_box_conf_pass = Entry(win_pass, textvariable=conf_mas_pass, width=55, justify="center")
    conf_mas_pass.trace_add("write", lambda x,y,z: txt_box_change(button=button, text=conf_mas_pass))
    entry_box_conf_pass.bind("<Return>", lambda x: entry_box_email.focus_force())

    entry_box_email = Entry(win_pass, textvariable=email, width=55, justify="center")
    email.trace_add("write", lambda x,y,z: txt_box_change(button=button, text=email))
    entry_box_email.bind("<Return>", lambda x: [store_pass_email(mas_pass, conf_mas_pass, email)])

    disabled = ("<Control-x>", "<Control-c>", "<Control-v>", "<Button-3>")
    for i in disabled:
        entry_box_conf_pass.bind(i, lambda x: "break") # Binds multiple key presses to function 'break', so that copy-pasting is disabled while password confirmation entry box is active
    
    #--BUTTONS SECTION--
    button = Button(text="OK", font=("Calibri", 16), command= lambda: [store_pass_email(mas_pass, conf_mas_pass, email)])
    button.config(width = 10, height = 1, relief="groove", bg="darkgray", state="disabled")

    button_exit = Button(text="Exit", font=("Calibri", 14), command=lambda :[exit_dialog_box(win_pass, create_pass_dialog_box)])
    button_exit.config(width = 6, height = 1, relief="groove", bg="darkgray")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_exit_menu = Button(text="Exit To Main Menu", font=("Calibri",12), bg="darkgray", command=lambda: [win_pass.destroy(), dialog_box_menu()])
    button_exit_menu.config(width = 16, height = 1, relief="groove")
    button_exit_menu.bind("<Enter>", lambda x: [button_exit_menu.config(relief="sunken")])
    button_exit_menu.bind("<Leave>", lambda x: [button_exit_menu.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    if isfile(pass_file):
        WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_pass, WIDTH, 350)
        win_pass.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
        button_exit.config(font=("Calibri", 14), width = 5)
        label.grid(row = 2, column = 0, columnspan=2)
        label_pass.grid(row = 3, column = 0, ipadx=30, ipady=5, padx = 5)
        label_conf_pass.grid(row = 4, column = 0, ipadx=10, ipady=5, padx = 5)
        label_email.grid(row = 5, column = 0, ipadx=5, ipady=5, padx = 5)
        entry_box_pass.grid(row = 3, column = 1, padx = 5)
        entry_box_conf_pass.grid(row = 4, column = 1, padx = 5)
        entry_box_email.grid(row = 5, column = 1, padx = 5)
        button.grid(row = 6, column = 0, pady = (2,5), columnspan=2)
        button_exit.grid(row = 0, column = 1, padx = 5, pady = (5,18), sticky="NE")
        button_exit_menu.grid(row = 0, column = 1, padx = 5, pady = 5, sticky="SE")

    else: 
        WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_pass, WIDTH, 300)
        win_pass.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
        label.grid(row = 1, column = 0, ipady=3, columnspan=2, sticky="N")
        label_pass.grid(row = 2, column = 0, ipadx=30, ipady=5, padx = 5)
        label_conf_pass.grid(row = 3, column = 0, ipadx=10, ipady=5, padx = 5)
        label_email.grid(row = 4, column = 0, ipadx=5, ipady=5, padx = 5)
        entry_box_pass.grid(row = 2, column = 1, padx = 5)
        entry_box_conf_pass.grid(row = 3, column = 1, padx = 5)
        entry_box_email.grid(row = 4, column = 1, padx = 5)
        button.grid(row = 5, column = 0, columnspan=2)
        button_exit.grid(row = 0, column = 1, padx = 5, pady = 5, sticky="NE")
        button_exit_menu.grid_forget()


    #--GRID CONFIGURE SECTION--
    win_pass.grid_rowconfigure(0, weight=2)
    win_pass.grid_rowconfigure(1, weight=1)
    win_pass.grid_rowconfigure(2, weight=1)
    win_pass.grid_rowconfigure(3, weight=1)
    win_pass.grid_rowconfigure(4, weight=1)
    win_pass.grid_rowconfigure(5, weight=1)
    win_pass.grid_rowconfigure(6, weight=1)
    
    win_pass.grid_columnconfigure(0, weight=1)
    win_pass.grid_columnconfigure(1, weight=4)
    
    entry_box_pass.focus_force()
    win_pass.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win_pass, create_pass_dialog_box))
    win_pass.mainloop()


def dialog_box_mas_pass():
    global win_pass_2, txt_box_2, button_ok

    #--WIN_PASS_2 SECTION--
    win_pass_2 = Tk()
    win_pass_2.resizable(width=False, height=False)
    win_pass_2.eval('tk::PlaceWindow . center')
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_pass_2, 400, 175)
    win_pass_2.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_pass_2.title("Master Password Required")
    win_pass_2.configure(bg="gray")

    try:
        with open(pass_file, "rb") as file:
            text = file.readlines()

        user_email = base64.b64decode(text[2]).decode("utf-8")

    except (FileNotFoundError, IndexError):
        user_email = None

    #--LABELS SECTION--
    label = Label(win_pass_2, text="Please enter the Master Password in order\nto access File/Folder Hider:", font=("Calibri", 14), width = 40, bg="darkgray")
    label_info = Label(win_pass_2, text="?", font=("Calibri",12), width = 3, height = 1, relief="groove", bg="gray")
    Hovertip(label_info, text="You have not provided your email address.\nTo access the Master Password Recovery feature,\nplease enter your email address while creating/\nchanging the Master Password.", hover_delay=200)

    #--STRINGVAR SECTION--
    password_2 = StringVar(win_pass_2)
    #--ENTRY BOX SECTION--
    txt_box_2 = Entry(win_pass_2, textvariable=password_2, width = 60, justify="center", show='*')
    password_2.trace_add("write", lambda x,y,z: txt_box_change(button=button_ok, text=password_2))
    txt_box_2.bind("<Return>", lambda x: get_txt_input(text=password_2, opr='pass'))

    #--BUTTONS SECTION--
    button_ok = Button(text="OK", font=("Calibri", 11), command=lambda : get_txt_input(text=password_2, opr='pass'))
    button_ok.config(width = 9, height = 1, relief = "groove", bg="darkgray", state="disabled")

    button_cancel = Button(text="Cancel", font=("Calibri", 11), command=lambda : exit_dialog_box(win_pass_2, dialog_box_mas_pass))
    button_cancel.config(width = 9, height = 1, relief = "groove", bg="darkgray")
    button_cancel.bind("<Enter>", lambda x: [button_cancel.config(relief="raised")])
    button_cancel.bind("<Leave>", lambda x: [button_cancel.config(relief="groove")])


    button_recov_passw = Button(text="Forgot Password?", font=("Calibri", 9), command=recov_code)
    button_recov_passw.config(width = 17, height = 1, relief = "groove", bg="darkgray", state="disabled")

    if user_email:
        button_recov_passw.config(state="normal")
        button_recov_passw.bind("<Enter>", lambda x: [button_recov_passw.config(relief="raised")])
        button_recov_passw.bind("<Leave>", lambda x: [button_recov_passw.config(relief="groove")])

    else:
        button_recov_passw.unbind("<Enter>")
        button_recov_passw.unbind("<Leave>")
        button_recov_passw.config(state="disabled")

    #--WIDGETS' PLACEMENT SECTION--
    if not user_email:
        label_info.grid(row = 0, column = 2, padx=(0,5), pady = 5, sticky="NE")
    else: label_info.grid_forget()
    button_recov_passw.grid(row = 0, column = 1, padx = 5, pady = 5, sticky="NE")
    label.grid(row = 1, column = 0, columnspan=3)
    txt_box_2.grid(row = 2, column = 0, columnspan=3)
    button_ok.grid(row = 3, column = 1, pady = (2,5), sticky="SW")
    button_cancel.grid(row = 3, column = 1, columnspan=2, padx = 80, pady = (2,5), sticky='SE')

    #--GRID CONFIGURE SECTION--
    win_pass_2.grid_rowconfigure(0, weight=1)
    win_pass_2.grid_rowconfigure(1, weight=1)
    win_pass_2.grid_rowconfigure(2, weight=2)

    win_pass_2.grid_columnconfigure(0, weight=1)
    win_pass_2.grid_columnconfigure(1, weight=2)

    txt_box_2.focus_force()
    win_pass_2.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win_pass_2, dialog_box_mas_pass))
    win_pass_2.mainloop()


def dialog_box_recover_mas_pass(recovery_code):
    global win_pass_3, password_3, txt_box_3

    #--WIN_PASS_3 SECTION--
    win_pass_3 = Tk()
    win_pass_3.attributes("-topmost", True)
    win_pass_3.resizable(width=False, height=False)
    win_pass_3.eval('tk::PlaceWindow . center')
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_pass_3, 400, 230)
    win_pass_3.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_pass_3.title("Master Password Recovery")
    win_pass_3.configure(bg="gray")

    #--LABELS SECTION--
    label = Label(win_pass_3, text="Enter the Recovery Code:", font=("Calibri", 15, "bold"), width = 40, bg="darkgray", fg="black")

    #--STRINGVAR SECTION--
    password_3 = StringVar(win_pass_3)

    #--ENTRY BOX SECTION--
    txt_box_3 = Entry(win_pass_3, textvariable=password_3, width = 60, justify="center")
    password_3.trace_add("write", lambda x,y,z: txt_box_change(button=button_ok, text=password_3))
    txt_box_3.bind("<Return>", lambda x: get_txt_input(text=password_3, opr='recover_pass', recovery_code=recovery_code))

    #--BUTTONS SECTION--
    button_ok = Button(text="OK", font=("Calibri", 13), bg="darkgray", command=lambda : get_txt_input(text=password_3, opr='recover_pass', recovery_code=recovery_code))
    button_ok.config(width = 9, height = 1, relief="groove", state="disabled")
    button_ok.bind("<Enter>", lambda x: [button_ok.config(relief="raised")])
    button_ok.bind("<Leave>", lambda x: [button_ok.config(relief="groove")])

    button_exit = Button(text="Exit", font=("Calibri", 12), bg="darkgray", command=lambda :[exit_dialog_box(win_pass_3, create_pass_dialog_box)])
    button_exit.config(width = 5, height = 1, relief="groove")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_exit_mas_pass = Button(text="Go Back", font=("Calibri",11), bg="darkgray", command=lambda: [win_pass_3.destroy(), dialog_box_mas_pass()])
    button_exit_mas_pass.config(width = 8, height = 1, relief="groove")
    button_exit_mas_pass.bind("<Enter>", lambda x: [button_exit_mas_pass.config(relief="sunken")])
    button_exit_mas_pass.bind("<Leave>", lambda x: [button_exit_mas_pass.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    button_exit.grid(row = 0, column = 1, padx = 5, pady = 5, sticky='NE')
    button_exit_mas_pass.grid(row = 1, column = 1, padx = 5, pady = (0,6), sticky='E')
    label.grid(row = 2, column = 0, columnspan = 2)
    txt_box_3.grid(row = 3, column = 0, columnspan = 2)
    button_ok.grid(row = 4, column = 0, columnspan = 2)

    win_pass_3.rowconfigure(2, weight=2)
    win_pass_3.rowconfigure(3, weight=1)
    win_pass_3.rowconfigure(4, weight=1)

    win_pass_3.columnconfigure(0, weight=1)
    win_pass_3.columnconfigure(1, weight=1)

    txt_box_3.focus_force()
    win_pass_3.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win_pass_3, dialog_box_recover_mas_pass))
    win_pass_3.mainloop()


def get_txt_input(text, opr, recovery_code=None, *args):
    # Takes a StringVar and operation to get the data stored in it and 
    # return the function according to the operation, else show error
    global fi_fo_path
    if opr == 'hide':
        fi_fo_path = text.get()
        return hide_fi_fo(fi_fo_path)

    elif opr == 'unhide':
        fi_fo_path = text.get()
        return unhide_fi_fo(fi_fo_path)

    elif opr == 'pass':
        password = text.get()
        with open(pass_file, "rb") as file:
            mas_pass = file.readline()
        # Decrypts the encrypted password stored in passw.pass
        dec_password = base64.b64decode(mas_pass).decode("utf-8")

        if password == dec_password:
            showinfo(title="Password Matched",
                    message="Access Granted. Click OK to run File/Folder Hider.")
            return win_pass_2.destroy(), dialog_box_menu()

        else:
            txt_box_2.delete(0, "end")
            showerror(title="Incorrect Password",
                    message="The password is incorrect. Please try again.")
            return txt_box_2.focus_force()
        
    elif opr == "recover_pass":
        input_recover_pass = password_3.get()
        if input_recover_pass == str(recovery_code):
            showinfo(title="Recovery Code Matched",
                     message="Authentication successful.\nYou can now proceed to change your Master Password.")
            return win_pass_3.destroy(), create_pass_dialog_box()
        
        else:
            txt_box_3.delete(0, "end")
            showerror(title="Incorrect Recovery Code",
                      message="The recovery code you have entered is incorrect. Please try again.")
            return txt_box_3.focus_force()


def txt_box_change(button, text):
    # Changes a button's state from disabled to enabled and
    # vice-versa upon entry of data in a given StringVar
    if text.get():
        button.config(state="normal")
        button.bind("<Enter>", lambda x: [button.config(relief="raised")])
        button.bind("<Leave>", lambda x: [button.config(relief="groove")])

    else:
        button.unbind("<Enter>")
        button.unbind("<Leave>")
        button.config(state="disabled")


def open_file():
    # Opens up a File Explorer Dialog Box for selecting a file
    global fi_fo_path
    fi_fo_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                title="Open File",
                filetypes=(("All","*.*"),
                (".exe","*.exe"),(".txt","*.txt"),(".png","*.png"),(".jpeg","*.jpg"),(".doc","*.doc"),(".pdf", "*.pdf")))
    
    if not fi_fo_path:
        return showerror(title="Dialog Box Exited",
                  message=Error.dialog_box_hide_exit_er)

    else: 
        return hide_fi_fo(fi_fo_path)


def open_folder():
    # Opens up a File Explorer Dialog Box for selecting a folder
    global fi_fo_path
    fi_fo_path = filedialog.askdirectory()

    if not fi_fo_path:
        return showerror(title="Dialog Box Exited",
                  message=Error.dialog_box_hide_exit_er)

    else:
        return hide_fi_fo(fi_fo_path)


def check_email_format(regex, email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False


def create_pass():
    showwarning("First Time Run", "Looks like you are running File/Folder Hider for the first time.\n\nIn order to ensure that it is only you that has access to this script, please create a master password in the next dialog box.")
    return create_pass_dialog_box()


def create_passw():
    with open(pass_file, "w") as _:
        pass
    return sys_hide(pass_file)

# Following 3 Functions are for deleting their respective Entry text fields

def delete_entry_pass():
    return entry_box_pass.delete(0, "end")

def delete_entry_conf_pass():
    return entry_box_conf_pass.delete(0, "end")

def delete_entry_email():
    return entry_box_email.delete(0, "end")

# Following 2 Functions are for encoding (NOT encrypting) Master
# Password and User Email respectively

def encode_pass(password):
    enc_pass = base64.b64encode(password.encode("utf-8"))
    return enc_pass

def encode_email(email):
    enc_email = base64.b64encode(email.encode("utf-8"))
    return enc_email

# Following 3 Functions are for writing Master Password,
# User Email, and both at the same time respectively

def write_password(password):
    enc_pass = encode_pass(password)
    sys_show(pass_file)
    with open(pass_file, "wb") as file:
        file.write(enc_pass)
    return sys_hide(pass_file)


def write_email(email):
    enc_email = encode_email(email)
    enc_list = [b'UHl0aG9uU2NyaXB0Nzg=\n', enc_email]
    sys_show(pass_file)
    with open(pass_file, "wb") as file:
        for item in enc_list:
            file.write(item)
    return sys_hide(pass_file)


def write_password_and_email(password, email):
    enc_pass = encode_pass(password)
    enc_email = encode_email(email)
    enc_list = [enc_pass, b'\nUHl0aG9uU2NyaXB0Nzg=\n', enc_email]
    sys_show(pass_file)
    with open(pass_file, "wb") as file:
        for item in enc_list:
            file.write(item)
    return sys_hide(pass_file)

# Following function is for deleting User Email 
# when entered "del" command by the user

def delete_email(lines):
    sys_show(pass_file)
    with open(pass_file, "wb") as file:
        for i, line in enumerate(lines):
            if i not in [1,2]:
                file.write(line)
        file.truncate(file.tell() - 1)
    return sys_hide(pass_file)


# Following 3 Functions are for checking multiple conditions upon input for
# Master Password only, User Email only, and both at the same time respectively
# It reacts accordingly to almost all possibilites of user input at various times
# e.g when starting the script for the first time, or when email was not entered in
# the first place, or when Master Password has already been created


def check_password_only(password, orig_password, orig_email):
    if not (orig_password or orig_email):
            write_password(password)
            logging("Create Master Password")
            showinfo("Success", "Master Password has been created successfully.\n\nPress OK to proceed.")
            return win_pass.destroy(), dialog_box_menu()

    elif (orig_password and orig_email) and orig_password != password:
        write_password_and_email(password, orig_email)
        logging("Change Master Password")
        showinfo("Success", "Master Password has been changed successfully.\n\nPress OK to proceed.")
        return win_pass.destroy(), dialog_box_menu()

    elif orig_password and orig_password != password:
        write_password(password)
        logging("Change Master Password")
        showinfo("Success", "Master Password has been changed successfully.\n\nPress OK to proceed.")
        return win_pass.destroy(), dialog_box_menu()

    else:
        delete_entry_pass(), delete_entry_conf_pass()
        showerror("Master Password Already Exists", "The Master Password you have entered is already in use. Please enter a new Master Password.")
        return entry_box_pass.focus_force()


def check_email_only(orig_password, email, orig_email):
    if orig_password:
        if email == "del":
            if orig_email:
                delete_email(lines)
                logging("Delete Email")
                showinfo("Success", "Email has been deleted successfully.")
                return win_pass.destroy(), dialog_box_menu()

            else:
                delete_entry_email()
                showerror("No Email Found", "No email is found to be deleted.")
                return entry_box_email.focus_force()

        elif not orig_email:
            if check_email_format(regex, email):
                write_password_and_email(orig_password, email)
                logging(f"Add Email '{email}'")
                showinfo("Success", "Email has been added successfully.\n\nPress OK to proceed.")
                return win_pass.destroy(), dialog_box_menu()
            
            else:
                delete_entry_email()
                showerror("Invalid Email Format", Error.invalid_email_format_er)
                return entry_box_email.focus_force()
            
        elif orig_email == email:
            delete_entry_email()
            showerror("Email Already Exists", "The email you have entered already exists. Please enter another email address.")
            return entry_box_email.focus_force()

        else:
            if check_email_format(regex, email):
                write_email(email)
                logging(f"Change Email to '{email}'")
                showinfo("Success", "Email has been changed successfully.\n\nPress OK to proceed.")
                return win_pass.destroy(), dialog_box_menu()
            
            else:
                delete_entry_email()
                showerror("Invalid Email Format", Error.invalid_email_format_er)
                return entry_box_email.focus_force()


    else:
        if check_email_format(regex, email):
            showerror("Master Password Required", "Master Password cannot be empty. Please create a Master Password.")
            return entry_box_pass.focus_force()

        else:
            delete_entry_email()
            showerror("Invalid Email Format", Error.invalid_email_format_er)
            return entry_box_email.focus_force()


def check_both_passw_and_email(password, orig_password, email, orig_email):
    if not orig_password:
        if check_email_format(regex, email):
            write_password_and_email(password, email)
            logging(f"Create Master Password & Add Email '{email}'")
            showinfo("Success", "Master Password has been created and your email has been added successfully.\n\nPress OK to proceed.")
            return win_pass.destroy(), dialog_box_menu()
        
        else:
            delete_entry_email()
            showerror("Invalid Email Format", Error.invalid_email_format_er)
            return entry_box_email.focus_force()

    elif email == "del":
        if orig_email:
            if not password:
                delete_email(lines)
                logging("Delete Email")
                showinfo("Success", "Email has been deleted successfully.")
                return win_pass.destroy(), dialog_box_menu()

            else:
                write_password(password)
                logging("Change Master Password & Delete Email")
                showinfo("Success", "Master Password has been changed and email has been deleted successfully.")
                return win_pass.destroy(), dialog_box_menu()

        else:
            delete_entry_email()
            showerror("No Email Found", "No email is found to be deleted.")
            return entry_box_email.focus_force()

    elif password != orig_password:
        if check_email_format(regex, email):
            if email != orig_email:
                write_password_and_email(password, email)
                logging(f"Change Master Password & Add Email '{email}'")
                showinfo("Success", "Master Password has been changed and your email has been added successfully.\n\nPress OK to proceed.")
                return win_pass.destroy(), dialog_box_menu()

            else:
                delete_entry_email()
                showerror("Email Already Exists", "The email you have entered already exists. Please enter another email address.")
                return entry_box_email.focus_force()

        else:
            delete_entry_email()
            showerror("Invalid Email Format", Error.invalid_email_format_er)
            return entry_box_email.focus_force()

    else:
        delete_entry_pass(), delete_entry_conf_pass()
        showerror("Master Password Already Exists", "The Master Password you have entered is already in use. Please enter a new Master Password.")
        return entry_box_pass.focus_force()


# This function uses the above related functions, basically the main function
# for storing Master Password and User Email


def store_pass_email(password, conf_pass, email):
    global regex, lines
    password = password.get()
    conf_pass = conf_pass.get()
    user_email = email.get()

    checking_password = None

    try:
        with open(pass_file, "rb") as file:
            lines = file.readlines()
        checking_password = base64.b64decode(lines[0]).decode("utf-8")
        checking_email = base64.b64decode(lines[2]).decode("utf-8")
    
    except (FileNotFoundError, IndexError):
        checking_email = None

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if password != conf_pass and not user_email:
        delete_entry_pass(), delete_entry_conf_pass()
        showerror("Non-Matching Passwords", "The passwords you have entered do not match. Please try again.")
        return entry_box_pass.focus_force()

    elif password != conf_pass and not check_email_format(regex, user_email) and user_email != "del":
        delete_entry_pass(), delete_entry_conf_pass(), delete_entry_email()
        showerror("Non-Matching Passwords & Invalid Email Format", "The passwords you have entered do not match & the email entered is of invalid format. Please try again.")
        return entry_box_pass.focus_force()

    elif password != conf_pass:
        delete_entry_pass(), delete_entry_conf_pass()
        showerror("Non-Matching Passwords", "The passwords you have entered do not match. Please try again.")
        return entry_box_pass.focus_force()
    
    elif password and user_email:
        check_both_passw_and_email(password, checking_password, user_email, checking_email)

    elif not password:
        check_email_only(checking_password, user_email, checking_email)

    elif not user_email:
        check_password_only(password, checking_password, checking_email)

    
def change_mas_pass():
    conf = askquestion("Confirmation", "You are about to change the current Master Password which is required to access File/Folder Hider. Email address can also be entered to access Master Password Recovery feature.\n\nDo you wish to continue?")
    
    if conf == "yes": return win.destroy(), create_pass_dialog_box()

    else: return

# The commands used to hide and unhide files and folders
def sys_hide(path):
    return os.system(f'attrib +h +s "{path}"')

def sys_hide_r_o(path):
    return os.system(f'attrib +h +s +r "{join(sys.path[0], path)}"')

def sys_show(path):
    return os.system(f'attrib -h -s "{path}"')

def sys_show_r_o(path):
    return os.system(f'attrib -h -s -r "{join(sys.path[0], path)}"')


def logging(opr, file_folder=None, fi_fo_path=None):
    # Logs hiding and unhiding records to log.txt for later use as history
    # and for copy-pasting file/folder path to unhide since they are not
    # visible in File Explorer
    if fi_fo_path:
        if file_size(log_file) == 0:
            with open(log_file, "a") as f:
                f.write(f"----Action: {opr};  Date & Time of Action: {today} {cur_t};  {file_folder} Path: {fi_fo_path}----\n")
            return

        else:
            with open(log_file, "a") as f:
                f.write(f"\n----Action: {opr};  Date & Time of Action: {today} {cur_t};  {file_folder} Path: {fi_fo_path}----\n")
            return

    else:
        if file_size(log_file) == 0:
            with open(log_file, "a") as f:
                f.write(f"----Action: {opr};  Date & Time of Action: {today} {cur_t}----\n")
            return
                
        else:
            with open(log_file, "a") as f:
                f.write(f"\n----Action: {opr};  Date & Time of Action: {today} {cur_t}----\n")
            return


def create_log():
    with open(log_file, "w") as _:
        pass
    return sys_hide(log_file)


def show_log():
    if isfile(log_file):
        os.startfile(log_file)
    else: return create_log(), show_log()


def clear_log():
    if isfile(log_file):
        if file_size(log_file) != 0:
            with open(log_file, "r") as file:
                data = file.read()
            # Counts the number of "Hide" and "Unhide" strings present in the log
            no_of_hide_str, no_of_unhide_str = data.count("Hide"), data.count("Unhide")
            # Checks if the number of "Hide" word is less than or equal to that
            # of "Unhide" word. If yes, then clearing the log is allowed, otherwise not.
            # That basically shows whether there are still hidden files/folders left on
            # the PC or not, to avoid losing their file-paths forever
            if no_of_hide_str <= no_of_unhide_str:
                conf = askquestion(title="Confirmation",
                                   message="This will clear all log in 'log.txt'. This action can not be undone.\n\nDo you wish to continue?")

                if conf == "yes":
                    sys_show(log_file)
                    create_log()
                    showinfo(title="Cleared All Log",
                             message="All log has been cleared successfully.")
                    return win.focus_force()

                else:
                    return

            else: return showerror("Error", "Cannot clear log as there still are\nhidden files/folders present in your computer.\n\nPlease unhide them all before clearing log.")
    
        else: return showerror(title="Log is Empty",
                        message="The log is already cleared.")
    
    else: return create_log(), clear_log()


def has_hidden_attribute(filename):
    # Gets the attributes of the file/folder and returns True if
    # +h attribute is present, otherwise False
    try:
        st = lstat(filename)
        flag = bool(st.st_file_attributes & H)

    except AttributeError:
        attributes = GetFileAttributes(filename)
        flag = attributes & H

    return flag

def hide_fi_fo(path):
    if isfile(path):
        txt_box_h.delete(0, "end")
        if has_hidden_attribute(path):
            showerror(title="File is Hidden",
                      message="The file you are trying to hide is already hidden.")
        
        else: return hide("File", path)

    elif isdir(path):
        txt_box_h.delete(0, "end")
        if has_hidden_attribute(path):
            showerror(title="Folder is Hidden",
                      message="The folder you are trying to hide is already hidden.")

        else: return hide("Folder", path)
        
    else:
        txt_box_h.delete(0, "end")
        showerror(title="Invalid Path",
                  message=Error.file_path_er)
        return txt_box_h.focus_force()


def hide(file_folder, fi_fo_path):
    sys_hide_r_o(fi_fo_path)
    logging("Hide" ,f"{file_folder}", fi_fo_path)
    del fi_fo_path
    return showinfo(title=f"{file_folder} Hiding Complete",
             message=f"{file_folder} has been hidden successfully.")


def unhide_fi_fo(path):
    if os.path.isfile(path):
        txt_box_uh.delete(0, "end")
        if has_hidden_attribute(path):
            return unhide("File", path)

        else:
            return showerror(title="File is Not Hidden",
                      message="The file you are trying to unhide is already visible.")
       
    elif os.path.isdir(path):
        txt_box_uh.delete(0, "end")
        if has_hidden_attribute(path):
            return unhide("Folder", path)

        else:
            return showerror(title="Folder is Not Hidden",
                      message="The folder you are trying to unhide is already visible.")

    else:
        txt_box_uh.delete(0, "end")
        showerror(title="Invalid Path",
                  message=Error.file_path_er)
        return txt_box_uh.focus_force()


def unhide(file_type, path):
    sys_show_r_o(path)
    logging("Unhide", f"{file_type}", path)
    del path
    return showinfo(title=f"{file_type} Unhiding Complete",
             message=f"{file_type} has been made visible successfully.")


def exit_dialog_box(win, dialog_box):
    conf_exit = askquestion(title="Confirmation",
                       message="Are you sure you want to exit?")

    if conf_exit == "yes":
        try: return win.destroy(), sys.exit()

        except TclError:
            return

    else:
        try:
            # If the Tk window passed in as argument is open, redraw/update it, else call its function
            return win.deiconify()
        except TclError:  
            return dialog_box()


if __name__ == "__main__":
    if not isfile(log_file):
        create_log()
    if not isfile(pass_file) or file_size(pass_file) == 0:
        create_pass()
    
    else: dialog_box_mas_pass()

dialog_box_menu()

# Programmed by: Mubashir Ahmed OR known as Mubashir78 on GitHub
# https://www.github.com/Mubashir78
