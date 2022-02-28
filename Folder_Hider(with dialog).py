from stat import UF_HIDDEN
import time
import os
from tkinter import Tk, Label, Button, CENTER, NE, RAISED, SUNKEN, GROOVE, SW, SE, LEFT, RIGHT, dialog
from tkinter import filedialog
from time import sleep
from datetime import date


today = date.today()
d = today.strftime("%d-%b-%Y")

t = time.localtime()
cur_t = time.strftime("%H:%M:%S", t)

global fi_fo_path
fi_fo_path = None

class Error:
    file_path_er = "File/Folder not found. Please make sure to type the path correctly."
    dialog_box_exit_er = "You exited the dialog box. Please try again."


def intro():
    print("======================\n   File/Folder Hider  \n======================")
    sleep(1.6)
    print("Welcome!")
    sleep(0.8)
    print("\nThis script hides and unhides files and/or folders!")
    sleep(1.2)
    main()

def return_to_menu():
    print("Going back to main menu...")
    sleep(1.2)
    print(" ")
    main()

def exit_code():
    print("The script will now exit.")
    sleep(1)
    exit()

def exit_code_1():
    win.destroy()
    exit_code()

def exit_code_2():
    win.destroy()
    return_to_menu()


def hover(e):
    button["relief"] = RAISED

def hover_2(e):
    button_2["relief"] = RAISED

def hover_exit(e):
    button_exit["relief"] = SUNKEN

def hover_exit_2(e):
    button_exit_menu["relief"] = SUNKEN

def leave(e):
    button["relief"] = GROOVE

def leave_2(e):
    button_2["relief"] = GROOVE

def leave_exit(e):
    button_exit["relief"] = GROOVE

def leave_exit_2(e):
    button_exit_menu["relief"] = GROOVE

def dialog_box():
    global win, button, button_2, button_exit, button_exit_menu
    win = Tk()
    win.attributes("-topmost", True)
    win.geometry("450x250")
    win.eval('tk::PlaceWindow . center')
    win.title("Dialog Box")

    label = Label(text="Click one of the buttons below\nto select what you want to hide:", font=("Calibiri",14))
    
    button = Button(text="Open a file",font=("Calibri",18), command=open_file)
    button.config(width = 15, height = 2, relief=GROOVE)
    button.bind("<Enter>", hover)
    button.bind("<Leave>", leave)

    button_2 = Button(text="Open a folder",font=("Calibri",18), command=open_folder)
    button_2.config(width = 15, height = 2, relief=GROOVE)
    button_2.bind("<Enter>", hover_2)
    button_2.bind("<Leave>", leave_2)

    button_exit = Button(text="Exit", font=("Calibri", 17), command=exit_code_1)
    button_exit.config(width = 5, height = 1, relief=GROOVE)
    button_exit.bind("<Enter>", hover_exit)
    button_exit.bind("<Leave>", leave_exit)

    button_exit_menu = Button(text="Exit To Main Menu", font=("Calibri",12), command=exit_code_2)
    button_exit_menu.config(width = 16, height = 1, relief=GROOVE)
    button_exit_menu.bind("<Enter>", hover_exit_2)
    button_exit_menu.bind("<Leave>", leave_exit_2)

    button_exit.pack(padx = (15,0),pady = (0, 5), anchor=NE)
    button_exit_menu.pack(padx = (15,0),pady = (0,15), anchor=NE)
    label.pack(pady = (5,20), anchor=CENTER, expand=True)
    button.pack(padx = 4, pady = (5,2), anchor=SW, side=LEFT, expand=True)
    button_2.pack(padx = 4, pady = (5,2), anchor=SE, side=RIGHT, expand=True)
    win.mainloop()


def open_file():
    win.destroy()
    global fi_fo_path
    fi_fo_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                title="Open File",
                filetypes=(("All","*.*"),
                (".exe","*.exe"),(".txt","*.txt"),(".png","*.png"),(".jpg","*.jpg"),(".doc","*.doc")))
    return


def open_folder():
    win.destroy()
    global fi_fo_path
    fi_fo_path = filedialog.askdirectory()
    return

def logging(file_folder,fi_fo_path,opr):
    with open("log.txt","a") as f:
            f.write(f"[Action: {opr};  Date & Time of Action: {d} {cur_t};  {file_folder} Path: {fi_fo_path}]\n")


def retry_code(opr, command):
    while True:
        retry = input(f"\nDo you wish to {opr} another file/folder?(y/n): ").lower().strip()
        if retry == "y":
            print("Restarting...")
            sleep(0.8)
            return command()

        elif retry == "n":
            print("\nGoing back...")
            sleep(1)
            return main()

        else:
            print("Invalid input. Please try again.")


def hide(file_folder, fi_fo_path):
    print("Working on it...")
    os.system(f'attrib +h +s +r "{fi_fo_path}"')
    logging(f"{file_folder}", fi_fo_path,"Hide")
    del fi_fo_path
    sleep(1)
    print(f"{file_folder} has been hidden successfully!")
    sleep(0.8)
    retry_code("hide", dialog_box)


def hide_file_folder(fi_fo_path):
    if os.path.isfile(fi_fo_path):
        return hide("File", fi_fo_path)
       
    elif os.path.isdir(fi_fo_path):
        return hide("Folder", fi_fo_path)


def unhide(file_type, path):
    print("Working on it...")
    os.system(f'attrib -h -s -r "{path}"')
    logging(f"{file_type}", path,"Unhide")
    del path
    sleep(1)
    print(f"{file_type} has been made visible successfully!")
    sleep(0.8)
    retry_code("unhide", unhide_file_or_folder)


def unhide_file_or_folder():
    print("\nA text file will be opened for you.")
    sleep(1.2)
    print("To unhide a file/folder, copy the full path to the hidden file/folder from the text file and paste it below.")
    sleep(2)
    while True:
        os.startfile("log.txt", show_cmd=1)
        f_p = input("\nFile/Folder path: ")
        if f_p == "exit":
            exit_code()

        elif f_p == "menu":
            print("Going back to main menu...")
            sleep(1)
            main()

        if os.path.isfile(f_p):
            unhide("File", f_p)

        elif os.path.isdir(f_p):
            unhide("Folder", f_p)
    
        else:
            print("%s" % Error.file_path_er)
            sleep(1.3)

def main():
    print("\nTo lock a file/folder, type 'h'; To unlock a file/folder, type 'uh'; To exit the script, type 'exit'.")
    sleep(1)
    while True:
        usr_choice = input("\nYour input: ").lower()
        if usr_choice == "h":
            while True:
                dialog_box()
                if fi_fo_path != None or fi_fo_path != "":
                    hide_file_folder(fi_fo_path)

                else:
                    print("%s" % Error.dialog_box_exit_er)
                    sleep(1)
                    continue

        elif usr_choice == "uh":
            unhide_file_or_folder()

        elif usr_choice == "exit":
            exit_code()

        else:
            print("Invalid input. Please try again.")
            sleep(1)
            continue

intro()