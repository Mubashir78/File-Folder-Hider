import time
import os
from sys import exit
from os.path import isfile, getsize as file_size
import tkinter
from tkinter import Tk, filedialog ,Label, Button, StringVar, Entry, simpledialog
from datetime import date
from tkinter import font
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning

today = date.today()
d = today.strftime("%d-%b-%Y")

t = time.localtime()
cur_t = time.strftime("%H:%M:%S", t)

WIDTH, HEIGHT = 500, 300

log_file, pass_file = "log.txt", "passw.pass"
fi_fo_path = txt_input = None

counter = counter_2 = 0


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


def dialog_box_menu():
    global win, label, label_2, counter, button_h, button_uh, button_sh_log, button_del_log, button_exit
    win = Tk()
    win.attributes("-topmost", True)
    win.resizable(width=False, height=False)
    win.eval('tk::PlaceWindow . center')
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win, WIDTH, HEIGHT)
    win.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win.title("File/Folder Hider")
    win.configure(bg="gray")


    label = Label(text="============== Main Menu ==============", font=("Calibri", 19, "bold"), bg="gray")
    intro_txt = StringVar(win, "Welcome To File/Folder Hider!\nHere you can hide and unhide your files and/or folders.\n\nPlease press one of the buttons below\nto use the File/Folder Hider:")
    label_2 = Label(textvariable=intro_txt, font=("Calibri", 14), width=50, bg="darkgray")
    
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

    button_exit = Button(text="Exit", font=("Calibri",14), bg="darkgray", command=lambda:[m_box(win)])
    button_exit.config(width = 6, height = 1, relief="groove")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_exit.grid(row = 0, column = 3, pady = 5, sticky='NE')
    label.grid(row = 1, column = 0, columnspan = 4, pady = (8,5))
    label_2.grid(row = 2, column = 0, columnspan = 4, pady = (8,13))
    button_h.grid(row = 3, column = 0, ipadx = 6, ipady = 5, pady = (5,5), sticky='S')
    button_uh.grid(row = 3, column = 1, ipadx = 6, ipady = 5, padx = (0,10), pady = (5,5), sticky='S')
    button_sh_log.grid(row = 3, column = 2, ipadx = 6, ipady = 7, padx = (10,0), pady = (5,5), sticky='S')
    button_del_log.grid(row = 3, column = 3, ipadx = 6, ipady = 7, pady = (5,5), sticky='S')

    win.grid_rowconfigure(0, weight=0)
    win.grid_rowconfigure(1, weight=2)
    win.grid_rowconfigure(2, weight=2)
    win.grid_rowconfigure(3, weight=1)

    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)
    win.grid_columnconfigure(2, weight=1)
    win.grid_columnconfigure(3, weight=1)

    counter += 1
    if counter >= 2:
        counter = 1
        label_2.destroy()

    win.mainloop()


def dialog_box_hide():
    global win_h, button_fi, button_fo, button_exit, button_exit_menu
    win_h = Tk()
    win_h.attributes("-topmost", True)
    win_h.resizable(width=False, height=False)
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_h, WIDTH, HEIGHT)
    win_h.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_h.title("Dialog Box: Hide")
    win_h.configure(bg="gray")

    label = Label(text="================= Hide =================", font=("Calibri", 19, "bold"), bg="gray")

    hide_txt = StringVar(win_h, "Click one of the buttons below to select\nwhat you want to hide:")
    label_2 = Label(textvariable=hide_txt, font=("Calibri",16), width=50, bg="darkgray")
    
    button_fi = Button(text="Hide a File", font=("Calibri",15), bg="darkgray", command=lambda:[open_file(win_h, "hide", dialog_box_hide)])
    button_fi.config(width = 11, height = 1, relief="groove")
    button_fi.bind("<Enter>", lambda x: [button_fi.config(relief="raised")])
    button_fi.bind("<Leave>", lambda x: [button_fi.config(relief="groove")])

    button_fo = Button(text="Hide a Folder",font=("Calibri",15), bg="darkgray", command=lambda:[open_folder(win_h, "hide", dialog_box_hide)])
    button_fo.config(width = 11, height = 1, relief="groove")
    button_fo.bind("<Enter>", lambda x: [button_fo.config(relief="raised")])
    button_fo.bind("<Leave>", lambda x: [button_fo.config(relief="groove")])

    button_exit = Button(text="Exit", font=("Calibri", 14), bg="darkgray", command=lambda:[m_box(win_h)])
    button_exit.config(width = 6, height = 1, relief="groove")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    button_exit_menu = Button(text="Exit To Main Menu", font=("Calibri",13), bg="darkgray", command=lambda: [win_h.destroy(), dialog_box_menu()])
    button_exit_menu.config(width = 15, height = 1, relief="groove")
    button_exit_menu.bind("<Enter>", lambda x: [button_exit_menu.config(relief="sunken")])
    button_exit_menu.bind("<Leave>", lambda x: [button_exit_menu.config(relief="groove")])

    button_exit.grid(row = 0, column = 2, pady = 5, sticky='NE')
    button_exit_menu.grid(row = 1, column = 2, sticky='E')
    label.grid(row = 2, column = 0, columnspan = 3)
    label_2.grid(row = 3, column = 0, columnspan = 3)
    button_fi.grid(row = 4, column = 0, ipadx = 8,ipady = 5, padx = (5,5), pady = (0,5), sticky='SE')
    button_fo.grid(row = 4, column = 2, ipadx = 8,ipady = 5, pady = (0,5), sticky='SW')

    win_h.grid_rowconfigure(0, weight=0)
    win_h.grid_rowconfigure(1, weight=1)
    win_h.grid_rowconfigure(2, weight=2)
    win_h.grid_rowconfigure(3, weight=2)
    win_h.grid_rowconfigure(4, weight=1)

    win_h.grid_columnconfigure(0, weight=1)
    win_h.grid_columnconfigure(1, weight=2)
    win_h.grid_columnconfigure(2, weight=1)

    win_h.focus_force()
    win_h.mainloop()


def dialog_box_unhide():
    try:
        global win_uh, button_op_log, button_uh, txt_box, fi_fo_path, button_exit, button_exit_menu, txt_input, text
        win_uh = Tk()
        win_uh.attributes("-topmost", True)
        WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_uh, WIDTH, HEIGHT)    
        win_uh.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
        win_uh.resizable(width=False, height=False)
        win_uh.title("Dialog Box: Unhide")
        win_uh.configure(bg="gray")
        
        label = Label(text="================ Unhide ================", font=("Calibri", 19, "bold"), bg="gray")

        label_2 = Label(text="Open the log file to check the full path to the file/folder\nyou want to unhide and copy/paste it below:", font=("Calibri", 14), width=50, bg="darkgray")
        
        text = StringVar(win_uh)
        txt_box = Entry(win_uh, textvariable=text, width = 70, justify="center")
        text.trace_add("write", txt_box_change)
        txt_box.bind("<Return>", get_txt_input)
        
        button_op_log = Button(text="Open Log File", font=("Calibri", 16), bg="darkgray", command=lambda :[os.startfile(log_file, show_cmd=1)])
        button_op_log.config(width = 12, height = 1, relief="groove")
        button_op_log.bind("<Enter>", lambda x: [button_op_log.config(relief="raised")])
        button_op_log.bind("<Leave>", lambda x: [button_op_log.config(relief="groove")])

        button_uh = Button(text="Unhide", font=("Calibri", 16), bg="darkgray", command = get_txt_input)
        button_uh.config(width = 11, height = 1, relief="groove", state="disabled")

        button_exit = Button(text="Exit", font=("Calibri", 17), bg="darkgray", command=lambda :[m_box(win_uh)])
        button_exit.config(width = 6, height = 1, relief="groove")
        button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
        button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

        button_exit_menu = Button(text="Exit To Main Menu", font=("Calibri",12), bg="darkgray", command=lambda: [win_uh.destroy(), dialog_box_menu()])
        button_exit_menu.config(width = 16, height = 1, relief="groove")
        button_exit_menu.bind("<Enter>", lambda x: [button_exit_menu.config(relief="sunken")])
        button_exit_menu.bind("<Leave>", lambda x: [button_exit_menu.config(relief="groove")])

        button_exit.grid(row = 0, column = 2, pady = 5, sticky='NE')
        button_exit_menu.grid(row = 1, column = 2, sticky='E')
        label.grid(row = 2, column = 0, columnspan = 3, pady=(2,2))
        label_2.grid(row = 3, column = 0, columnspan = 3, pady = (2,3))
        txt_box.grid(row = 4, column = 0, columnspan = 3, pady = (7,7))
        button_op_log.grid(row = 5, column = 0, padx=(0,5), pady = (0,5), sticky='S')
        button_uh.grid(row = 5, column = 2, pady = (0,5), sticky='S')

        win_uh.grid_rowconfigure(0, weight=1)
        win_uh.grid_rowconfigure(1, weight=1)
        win_uh.grid_rowconfigure(2, weight=2)
        win_uh.grid_rowconfigure(3, weight=2)
        win_uh.grid_rowconfigure(4, weight=2)
        win_uh.grid_rowconfigure(5, weight=1)

        win_uh.grid_columnconfigure(0, weight=1)
        win_uh.grid_columnconfigure(1, weight=2)
        win_uh.grid_columnconfigure(2, weight=1)

        txt_box.focus_force()
        win_uh.mainloop()

    except TypeError:
        win_uh.destroy()
        showerror(title="Invalid Path",
                  message=Error.file_path_er)
        dialog_box_unhide()


def create_pass_dialog_box():
    global win_pass, password, entry_box_pass
    win_pass = Tk()
    win_pass.attributes("-topmost", True)
    win_pass.resizable(width=False, height=False)
    win_pass.eval('tk::PlaceWindow . center')
    WIN_WIDTH, WIN_HEIGHT, X, Y = center(win_pass, WIDTH, HEIGHT)
    win_pass.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(X)}+{int(Y)}")
    win_pass.title("Create Password")
    win_pass.configure(bg="gray")

    label = Label(text="Enter a strong password:", font=("Calibri", 16, "bold"), bg="darkgray", fg="black")
    label_pass = Label(text="Password:", font=("Calibri", 14, "bold"), bg="darkgray")
    label_conf_pass = Label(text="Confirm Password:", font=("Calibri", 12, "bold"), bg="darkgray")

    password = StringVar(win_pass)
    conf_password = StringVar(win_pass)

    entry_box_pass = Entry(win_pass, textvariable=password, width=55, justify="center")
    entry_box_pass.bind("<Return>", lambda x: entry_box_conf_pass.focus_force())

    entry_box_conf_pass = Entry(win_pass, textvariable=conf_password, width=55, justify="center")
    entry_box_conf_pass.bind("<Return>", lambda x: [store_pass(password, conf_password)])

    disabled = ("<Control-x>", "<Control-c>", "<Control-v>", "<Button-3>")
    for i in disabled:
        entry_box_conf_pass.bind(i, lambda x: "break")
    
    button = Button(text="Create", font=("Calibri", 16), command= lambda: [store_pass(password, conf_password)])
    button.config(width = 10, height = 1, relief="groove", bg="darkgray")
    button.bind("<Enter>", lambda x: [button.config(relief="raised")])
    button.bind("<Leave>", lambda x: [button.config(relief="groove")])

    button_exit = Button(text="Exit", font=("Calibri", 17), command=lambda :[m_box(win_pass)])
    button_exit.config(width = 6, height = 1, relief="groove", bg="darkgray")
    button_exit.bind("<Enter>", lambda x: [button_exit.config(relief="sunken")])
    button_exit.bind("<Leave>", lambda x: [button_exit.config(relief="groove")])

    label.grid(row = 0, column = 0, columnspan=2)
    label_pass.grid(row = 1, column = 0, ipadx=30, ipady=5, padx=(5,5))
    label_conf_pass.grid(row = 2, column = 0, ipadx=10, ipady=5, padx=(5,5))
    entry_box_pass.grid(row = 1, column = 1, padx=(5,5))
    entry_box_conf_pass.grid(row = 2, column = 1, padx=(5,5))
    button.grid(row = 3, column = 0, columnspan=2)
    button_exit.grid(row = 0, column = 1, padx = 5,  pady = 5, sticky="NE")

    win_pass.grid_rowconfigure(0, weight=2)
    win_pass.grid_rowconfigure(1, weight=1)
    win_pass.grid_rowconfigure(2, weight=1)
    win_pass.grid_rowconfigure(3, weight=1)
    
    win_pass.grid_columnconfigure(0, weight=1)
    win_pass.grid_columnconfigure(0, weight=4)
    
    entry_box_pass.focus_force()
    win_pass.mainloop()


def get_txt_input(*_):
    global txt_input
    txt_input = text.get()
    unhide_fi_fo(txt_input)


def txt_box_change(*_):
    if text.get():
        button_uh.config(state="normal")
        button_uh.bind("<Enter>", lambda x: [button_uh.config(relief="raised")])
        button_uh.bind("<Leave>", lambda x: [button_uh.config(relief="groove")])
    else:
        button_uh.unbind("<Enter>")
        button_uh.unbind("<Leave>")
        button_uh.config(state="disabled")


def open_file(win, opr, command):
    win.destroy()
    global fi_fo_path
    fi_fo_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                title="Open File",
                filetypes=(("All","*.*"),
                (".exe","*.exe"),(".txt","*.txt"),(".png","*.png"),(".jpg","*.jpg"),(".doc","*.doc")))
    
    if fi_fo_path == None or fi_fo_path == "":
        showerror(title="Dialog Box Exited",
                  message=Error.dialog_box_hide_exit_er)
        dialog_box_hide()

    else:
        if os.path.isfile(fi_fo_path):
            if opr == "hide":
                hide("File", fi_fo_path)
            elif opr == "unhide":
                unhide("File", fi_fo_path)
        
        else:
            showerror(title="Invalid Path",
                      message=Error.file_path_er)
            command()


def open_folder(win, opr, command):
    win.destroy()
    global fi_fo_path
    fi_fo_path = filedialog.askdirectory()

    if fi_fo_path == None or fi_fo_path == "":
        showerror(title="Dialog Box Exited",
                  message=Error.dialog_box_hide_exit_er)
        dialog_box_hide()

    else:
        if os.path.isdir(fi_fo_path):
            if opr == "hide":
                hide("Folder", fi_fo_path)
            elif opr == "unhide":
                unhide("Folder", fi_fo_path)
        
        else:
            showerror(title="Invalid Path",
                      message=Error.file_path_er)
            command()


def create_pass():
    showwarning("First Time Run", "Looks like you are running File/Folder Hider for the first time.\n\nIn order to ensure that it is only you that has access to this script, please create a master password in the next dialog box.")
    return create_pass_dialog_box()


def store_pass(password, conf_pass):
    global counter_2
    password = password.get()
    conf_pass = conf_pass.get()
    if password == conf_pass:
        if password != "" and conf_pass != "":
            with open(pass_file, "w") as file:
                file.write(password)
            pass_path = os.path.abspath(pass_file)
            os.system(f'attrib +h +s "{pass_path}"')
            counter_2 += 1
            showinfo("Success", "Master Password has been created successfully.\n\nClick OK to run File/Folder Hider.")
            win_pass.destroy()
            return dialog_box_menu()

        else:
            showerror("Invalid Password Format", "Master password cannot be empty.\nPlease try again.")
            return entry_box_pass.focus_force()
            
    
    else:
        return showerror("Unmatching Passwords", "The passwords you have entered do not match.\nPlease try again.")


def logging(file_folder,fi_fo_path,opr):
    if file_size(log_file) == 0:
        with open(log_file,"a") as f:
            f.write(f"[Action: {opr};  Date & Time of Action: {d} {cur_t};  {file_folder} Path: {fi_fo_path}]\n")
            
    else:
        with open(log_file,"a") as f:
            f.write(f"\n[Action: {opr};  Date & Time of Action: {d} {cur_t};  {file_folder} Path: {fi_fo_path}]\n")


def create_log():
    with open(log_file, "w") as _:
        pass
    log_path = os.path.abspath(log_file)
    os.system(f'attrib +h +s "{log_path}"')


def show_log():
    if isfile(log_file):
        os.startfile(log_file, show_cmd=1)
    else:
        return create_log(), show_log()


def clear_log():
    if isfile(log_file):
        if file_size(log_file) != 0:
            with open(log_file, "r") as file:
                data = file.read()
                no_of_hide_str, no_of_unhide_str = data.count("Hide"), data.count("Unhide")
            if no_of_hide_str <= no_of_unhide_str:
                conf = askquestion(title="Confirmation",
                                    message="This will clear all log in 'log.txt'. This action can not be undone.\n\nDo you wish to proceed?")

                if conf == "yes":
                    os.remove(log_file)
                    showinfo(title="Cleared All Log",
                            message="All log has been cleared successfully.")
                    return win.focus_force()

                else:
                    return

            else:
                showerror("Error", "Cannot clear log as there still are\nhidden files/folders present in your computer.\n\nPlease unhide them all before clearing log.")
    
        else:
            showerror(title="Log is Empty",
                    message="The log is already cleared.")
    
    else:
        return create_log(), clear_log()


def hide(file_folder, fi_fo_path):
    os.system(f'attrib +h +s +r "{fi_fo_path}"')
    logging(f"{file_folder}", fi_fo_path,"Hide")
    del fi_fo_path
    showinfo(title=f"{file_folder} Hiding Complete",
             message=f"{file_folder} has been hidden successfully.")
    retry_code("hide", dialog_box_hide)


def hide_fi_fo(path):
    if os.path.isfile(path):
        hide("File", path)
       
    elif os.path.isdir(path):
        hide("Folder", path)


def unhide(file_type, path):
    os.system(f'attrib -h -s -r "{path}"')
    logging(f"{file_type}", path,"Unhide")
    del path
    win_uh.destroy()
    showinfo(title=f"{file_type} Unhiding Complete",
             message=f"{file_type} has been made visible successfully.")
    retry_code("unhide", dialog_box_unhide)


def unhide_fi_fo(path):
    if os.path.isfile(path):
        unhide("File", path)
       
    elif os.path.isdir(path):
        unhide("Folder", path)

    else:
        showerror(title="Invalid Path",
                  message=Error.file_path_er)
        txt_box.focus_force()


def retry_code(opr, command):
    retry = askquestion(title="Confirmation",
                        message=f"Do you wish to {opr} another file/folder?")
    if retry == "yes":
        return command()

    else:
        return dialog_box_menu()


def m_box(win):
    conf = askquestion(title="Confirmation",
                       message="Are you sure you want to exit?")
    if conf == "yes":
        global counter_2
        counter_2 += 1
        win.destroy()
        exit()


if __name__ == "__main__":
    if isfile(log_file) == False:
        create_log()
    if isfile(pass_file) == False:
        create_pass()
        while counter_2 < 1:
            showerror("No Master Password Created", "No master password has been created.\nYou must create one before running File/Folder Hider.")
            create_pass_dialog_box()
    else:
        while True:
            inp_pass = simpledialog.askstring("Password Required", "Please enter the Master Password in order to access File/Folder Hider:")
            with open(pass_file, "r") as file:
                password = file.read()
                if inp_pass == password:
                    showinfo("Password Matched", "Access Granted. Click OK to run File/Folder Hider.")
                    dialog_box_menu()
                    break
                else:
                    showerror("Incorrect Password", "The password is incorrect. Please try again.")
exit()