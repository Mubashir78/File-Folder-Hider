# Programmed by: Mubashir Ahmed OR known as Mubashir78 on Github

from pathlib import Path
import os, sys
from datetime import date, datetime
from os import lstat
from os.path import getsize as file_size
from os.path import join, isdir, isfile
from stat import FILE_ATTRIBUTE_HIDDEN as H
from sys import exit
from tkinter import Button, Entry, Label, StringVar, TclError, Tk, filedialog
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning
from win32api import GetFileAttributes

# Current date
today = date.today().strftime("%d-%b-%Y")

# Current time
cur_t = datetime.today().strftime("%I:%M %p")

WIDTH, HEIGHT = 500, 300

# Makes sure that the files below are created in the same directory as the script
log_file, pass_file = Path(__file__).with_name('log.txt'), Path(__file__).with_name('passw.pass')

fi_fo_path = txt_input = conf_exit = None

counter_2 = 0  # Used to indicate whether the user has created master-password or simply skipped it. Upon skipping, error is shown

class Error:
    file_path_er = "File/Folder not found. Please make sure to type the path correctly."
    dialog_box_hide_exit_er = "You exited the dialog box. Please try again."


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
    win.grid_rowconfigure(0, weight=0)
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
    button_h = Button(text="Hide", font=("Calibri",12), bg="darkgray", command= lambda x: get_txt_input(text=text_h, opr='hide'))
    button_h.config(width = 8, height = 1, relief="groove", state="disabled")
    button_h.bind("<Enter>", lambda x: [button_h.config(relief="raised")])
    button_h.bind("<Leave>", lambda x: [button_h.config(relief="groove")])

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
    win_h.grid_rowconfigure(0, weight=0)
    win_h.grid_rowconfigure(1, weight=0)
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

    button_exit = Button(text="Exit", font=("Calibri", 17), bg="darkgray", command=lambda :[exit_dialog_box(win_uh, dialog_box_unhide)])
    button_exit.config(width = 6, height = 1, relief="groove")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_exit_menu = Button(text="Exit To Main Menu", font=("Calibri",12), bg="darkgray", command=lambda: [win_uh.destroy(), dialog_box_menu()])
    button_exit_menu.config(width = 16, height = 1, relief="groove")
    button_exit_menu.bind("<Enter>", lambda x: [button_exit_menu.config(relief="sunken")])
    button_exit_menu.bind("<Leave>", lambda x: [button_exit_menu.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    button_exit.grid(row = 0, column = 2, pady = 5, sticky='NE')
    button_exit_menu.grid(row = 1, column = 2, sticky='E')
    label.grid(row = 2, column = 0, columnspan = 3, pady=(2,2))
    label_2.grid(row = 3, column = 0, columnspan = 3, pady = (2,3))
    txt_box_uh.grid(row = 4, column = 0, columnspan = 3, pady = (7,7))
    button_op_log.grid(row = 5, column = 0, padx=(0,5), pady = (0,5), sticky='S')
    button_uh.grid(row = 5, column = 2, pady = (0,5), sticky='S')

    #--GRID CONFIGURE SECTION--
    win_uh.grid_rowconfigure(0, weight=1)
    win_uh.grid_rowconfigure(1, weight=1)
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
    global win_pass, mas_pass, entry_box_pass, entry_box_conf_pass

    #--WIN_PASS SECTION--
    win_pass = Tk()
    win_pass.attributes("-topmost", True)
    win_pass.resizable(width=False, height=False)
    win_pass.eval('tk::PlaceWindow . center')
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_pass, WIDTH, HEIGHT)
    win_pass.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_pass.title("Create Password")
    win_pass.configure(bg="gray")

    #--LABELS SECTION--
    label = Label(text="Enter a strong password:", font=("Calibri", 16, "bold"), bg="darkgray", fg="black")
    label_pass = Label(text="Password:", font=("Calibri", 14, "bold"), bg="darkgray")
    label_conf_pass = Label(text="Confirm Password:", font=("Calibri", 12, "bold"), bg="darkgray")

    mas_pass = StringVar(win_pass)
    conf_mas_pass = StringVar(win_pass)

    #--ENTRY BOXES SECTION--
    entry_box_pass = Entry(win_pass, textvariable=mas_pass, width=55, justify="center")
    entry_box_pass.bind("<Return>", lambda x: entry_box_conf_pass.focus_force())

    entry_box_conf_pass = Entry(win_pass, textvariable=conf_mas_pass, width=55, justify="center")
    entry_box_conf_pass.bind("<Return>", lambda x: [store_pass(mas_pass, conf_mas_pass)])

    disabled = ("<Control-x>", "<Control-c>", "<Control-v>", "<Button-3>")
    for i in disabled:
        entry_box_conf_pass.bind(i, lambda x: "break") # Binds multiple key presses to function 'break', so that copy-pasting is disabled while password confirmation entry box is active
    
    #--BUTTONS SECTION--
    button = Button(text="Create", font=("Calibri", 16), command= lambda: [store_pass(mas_pass, conf_mas_pass)])
    button.config(width = 10, height = 1, relief="groove", bg="darkgray")
    button.bind("<Enter>", lambda x: [button.config(relief="raised")])
    button.bind("<Leave>", lambda x: [button.config(relief="groove")])

    button_exit = Button(text="Exit", font=("Calibri", 17), command=lambda :[exit_dialog_box(win_pass, create_pass_dialog_box)])
    button_exit.config(width = 6, height = 1, relief="groove", bg="darkgray")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    label.grid(row = 0, column = 0, columnspan=2)
    label_pass.grid(row = 1, column = 0, ipadx=30, ipady=5, padx=(5,5))
    label_conf_pass.grid(row = 2, column = 0, ipadx=10, ipady=5, padx=(5,5))
    entry_box_pass.grid(row = 1, column = 1, padx=(5,5))
    entry_box_conf_pass.grid(row = 2, column = 1, padx=(5,5))
    button.grid(row = 3, column = 0, columnspan=2)
    button_exit.grid(row = 0, column = 1, padx = 5,  pady = 5, sticky="NE")

    #--GRID CONFIGURE SECTION--
    win_pass.grid_rowconfigure(0, weight=2)
    win_pass.grid_rowconfigure(1, weight=1)
    win_pass.grid_rowconfigure(2, weight=1)
    win_pass.grid_rowconfigure(3, weight=1)
    
    win_pass.grid_columnconfigure(0, weight=1)
    win_pass.grid_columnconfigure(0, weight=4)
    
    entry_box_pass.focus_force()
    win_pass.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win_pass, create_pass_dialog_box))
    win_pass.mainloop()


def dialog_box_mas_pass():
    global win_pass_2, txt_box_2, button_ok

    #--WIN_PASS_2 SECTION--
    win_pass_2 = Tk()
    win_pass_2.attributes("-topmost", True)
    win_pass_2.resizable(width=False, height=False)
    win_pass_2.eval('tk::PlaceWindow . center')
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_pass_2, 400, 150)
    win_pass_2.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_pass_2.title("Change Password")
    win_pass_2.configure(bg="gray")

    #--LABELS SECTION--
    label = Label(win_pass_2, text="Please enter the Master Password in order\nto access File/Folder Hider:", font=("Calibri", 14), width = 40, bg="darkgray")

    #--ENTRY BOX SECTION--
    password_2 = StringVar(win_pass_2)
    txt_box_2 = Entry(win_pass_2, textvariable=password_2, width = 60, justify="center", show='*')
    password_2.trace_add("write", lambda x,y,z: txt_box_change(button=button_ok, text=password_2))
    txt_box_2.bind("<Return>", lambda x: get_txt_input(text=password_2, opr='pass'))

    #--BUTTONS SECTION--
    button_ok = Button(text="OK", font=("Calibri", 11), command=lambda x: get_txt_input(text=password_2, opr='pass'))
    button_ok.config(width = 9, height = 1, relief = "groove", bg="darkgray", state="disabled")
    button_ok.bind("<Enter>", lambda x: [button_ok.config(relief="raised")])
    button_ok.bind("<Leave>", lambda x: [button_ok.config(relief="groove")])

    button_cancel = Button(text="Cancel", font=("Calibri", 11), command=lambda : exit_dialog_box(win_pass_2, dialog_box_mas_pass))
    button_cancel.config(width = 9, height = 1, relief = "groove", bg="darkgray")
    button_cancel.bind("<Enter>", lambda x: [button_cancel.config(relief="raised")])
    button_cancel.bind("<Leave>", lambda x: [button_cancel.config(relief="groove")])

    #--WIDGETS' PLACEMENT SECTION--
    label.grid(row = 0, column = 0, columnspan=2)
    txt_box_2.grid(row = 1, column = 0, columnspan=2)
    button_ok.grid(row = 2, column = 0, padx = 40, pady = (2,5), sticky="SE")
    button_cancel.grid(row = 2, column = 1, padx = 40, pady = (2,5), sticky="SW")

    #--GRID CONFIGURE SECTION--
    win_pass_2.grid_rowconfigure(0, weight=1)
    win_pass_2.grid_rowconfigure(1, weight=2)

    win_pass_2.grid_columnconfigure(0, weight=1)
    win_pass_2.grid_columnconfigure(1, weight=1)

    txt_box_2.focus_force()
    win_pass_2.protocol("WM_DELETE_WINDOW", lambda : exit_dialog_box(win_pass_2, dialog_box_mas_pass))
    win_pass_2.mainloop()


def get_txt_input(text, opr, *args): # Takes a StringVar and operation to get the data stored in it and return the function according to the operation, else show error
    global fi_fo_path
    if opr == 'hide':
        fi_fo_path = text.get()
        hide_fi_fo(fi_fo_path)

    elif opr == 'unhide':
        fi_fo_path = text.get()
        unhide_fi_fo(fi_fo_path)

    elif opr == 'pass':
        password = text.get()
        with open(pass_file, "r") as file:
            mas_pass = file.read()

        if password == mas_pass:
            showinfo(title="Password Matched",
                    message="Access Granted. Click OK to run File/Folder Hider.")
            return win_pass_2.destroy(), dialog_box_menu()

        else:
            txt_box_2.delete(0, "end")
            showerror(title="Incorrect Password",
                    message="The password is incorrect. Please try again.")
            txt_box_2.focus_force()


def txt_box_change(button, text): # Changes a button's state from disabled to enabled and vice-versa upon entry of data in a given StringVar
    if text.get():
        button.config(state="normal")
        button.bind("<Enter>", lambda x: [button.config(relief="raised")])
        button.bind("<Leave>", lambda x: [button.config(relief="groove")])

    else:
        button.unbind("<Enter>")
        button.unbind("<Leave>")
        button.config(state="disabled")


def open_file():
    global fi_fo_path
    fi_fo_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                title="Open File",
                filetypes=(("All","*.*"),
                (".exe","*.exe"),(".txt","*.txt"),(".png","*.png"),(".jpeg","*.jpg"),(".doc","*.doc"),(".pdf", "*.pdf")))
    
    if fi_fo_path == None or fi_fo_path == "":
        showerror(title="Dialog Box Exited",
                  message=Error.dialog_box_hide_exit_er)

    else: 
        hide_fi_fo(fi_fo_path)


def open_folder():
    global fi_fo_path
    fi_fo_path = filedialog.askdirectory()

    if fi_fo_path == None or fi_fo_path == "":
        showerror(title="Dialog Box Exited",
                  message=Error.dialog_box_hide_exit_er)

    else:
        hide_fi_fo(fi_fo_path)


def create_pass():
    showwarning("First Time Run", "Looks like you are running File/Folder Hider for the first time.\n\nIn order to ensure that it is only you that has access to this script, please create a master password in the next dialog box.")
    create_pass_dialog_box()


def store_pass(password, conf_pass):
    global counter_2
    password = password.get()
    conf_pass = conf_pass.get()

    if password == conf_pass:
        if password != "" and conf_pass != "":
            with open(pass_file, "w") as file:
                file.write(password)
            counter_2 += 1
            showinfo("Success", "Master Password has been created successfully.\n\nClick OK to run File/Folder Hider.")
            win_pass.destroy()
            return dialog_box_menu()

        else:
            showerror("Invalid Password Format", "Master password cannot be empty.\nPlease try again.")
            return entry_box_pass.focus_force()
            
    
    else:
        entry_box_pass.delete(0, "end")
        entry_box_conf_pass.delete(0, "end")
        showerror("Unmatching Passwords", "The passwords you have entered do not match.\nPlease try again.")
        return entry_box_pass.focus_force()


def change_mas_pass():
    conf = askquestion("Confirmation", "You are about to change the current master password\nwhich is required to access File/Folder Hider.\n\nDo you wish to continue?")
    
    if conf == "yes":
        win.destroy()
        create_pass_dialog_box()

    else: return


def sys_hide(path):
    os.system(f'attrib +h +s "{path}"')

def sys_hide_r_o(path):
    os.system(f'attrib +h +s +r "{join(sys.path[0], path)}"')

def sys_show(path):
    os.system(f'attrib -h -s "{path}"')

def sys_show_r_o(path):
    os.system(f'attrib -h -s -r "{join(sys.path[0], path)}"')


def logging(file_folder,fi_fo_path,opr):
    if file_size(log_file) == 0:
        with open(log_file, "a") as f:
            f.write(f"----Action: {opr};  Date & Time of Action: {today} {cur_t};  {file_folder} Path: {fi_fo_path}----\n")
            
    else:
        with open(log_file, "a") as f:
            f.write(f"\n----Action: {opr};  Date & Time of Action: {today} {cur_t};  {file_folder} Path: {fi_fo_path}----\n")


def create_log():
    with open(log_file, "w") as _:
        pass
    sys_hide(log_file)


def show_log():
    if isfile(log_file):
        os.startfile(log_file)
    else: return create_log(), show_log()


def clear_log():
    if isfile(log_file):
        if file_size(log_file) != 0:
            with open(log_file, "r") as file:
                data = file.read()
                no_of_hide_str, no_of_unhide_str = data.count("Hide"), data.count("Unhide")
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

            else: showerror("Error", "Cannot clear log as there still are\nhidden files/folders present in your computer.\n\nPlease unhide them all before clearing log.")
    
        else: showerror(title="Log is Empty",
                        message="The log is already cleared.")
    
    else: return create_log(), clear_log()


def has_hidden_attribute(filename):
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
        
        else: hide("File", path)

    elif isdir(path):
        txt_box_h.delete(0, "end")
        if has_hidden_attribute(path):
            showerror(title="Folder is Hidden",
                      message="The folder you are trying to hide is already hidden.")

        else: hide("Folder", path)
        
    else:
        txt_box_h.delete(0, "end")
        showerror(title="Invalid Path",
                  message=Error.file_path_er)
        txt_box_h.focus_force()


def hide(file_folder, fi_fo_path):
    sys_hide_r_o(fi_fo_path)
    logging(f"{file_folder}", fi_fo_path, "Hide")
    del fi_fo_path
    showinfo(title=f"{file_folder} Hiding Complete",
             message=f"{file_folder} has been hidden successfully.")


def unhide_fi_fo(path):
    if os.path.isfile(path):
        txt_box_uh.delete(0, "end")
        if has_hidden_attribute(path):
            unhide("File", path)
        else:
            showerror(title="File is Not Hidden",
                      message="The file you are trying to unhide is already visible.")
       
    elif os.path.isdir(path):
        txt_box_uh.delete(0, "end")
        if has_hidden_attribute(path):
            unhide("Folder", path)
        else:
            showerror(title="Folder is Not Hidden",
                      message="The folder you are trying to unhide is already visible.")

    else:
        txt_box_uh.delete(0, "end")
        showerror(title="Invalid Path",
                  message=Error.file_path_er)
        txt_box_uh.focus_force()


def unhide(file_type, path):
    sys_show_r_o(path)
    logging(f"{file_type}", path, "Unhide")
    del path
    showinfo(title=f"{file_type} Unhiding Complete",
             message=f"{file_type} has been made visible successfully.")


def exit_dialog_box(win, dialog_box):
    conf_exit = askquestion(title="Confirmation",
                       message="Are you sure you want to exit?")

    if conf_exit == "yes":
        global counter_2
        counter_2 += 1
        try: win.destroy(), exit()

        except TclError:
            exit()

    if conf_exit == "no":
        try:  
            win.deiconify()
        except TclError:  
            dialog_box()


if __name__ == "__main__":
    if not isfile(log_file):
        create_log()
    if not isfile(pass_file):
        create_pass()
        while counter_2 < 1:
            showerror(title="No Master Password Created",
                      message="No master password has been created.\nYou must create one before running File/Folder Hider.")
            create_pass_dialog_box()
    else: dialog_box_mas_pass()

dialog_box_menu()

# Programmed by: Mubashir Ahmed OR known as Mubashir78 on Github