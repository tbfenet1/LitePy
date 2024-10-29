#-------------------------------------------------------------------------------
# Name:        litepy.pyw
# Purpose:     A light python scripter with the ability to run in python 
#	       interpreter
#
# Author:      22TaylorS
#
# Created:     09/10/2024
# Copyright:   (c) 22TaylorS 2024
# Licence:     GNU General Public License
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# BUILD COMMITED TO GITHUB REPO
#       
#       Comitted: 29/10/24
#       Comiiter: tbfenet1
#       Commit Message: Version 1. fixed a few bugs before release.
#-------------------------------------------------------------------------------


# tbfenet1 -- 29/10/2024
# 	
#	I made this in school so expect some stack overflow
#	copypaste but its open source code under GPL so who cares  ¯\_(ツ)_/¯.
#       

# Import the required libraries
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os
import subprocess
import webbrowser


# Create an instance of tkinter frame or window
root = Tk()
root.title("LitePy 1.0")
# Set the size of the window
root.geometry("900x550")

# Create a Text widget with undo is set
text = Text(root, undo=True)
text.pack(fill=tk.BOTH, expand=True)

# Setting up colorizer
cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat().pattern, re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)

# Define tags
cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}
cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': '#FFFFFF'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
cdg.tagdefs['STRING'] = {'foreground': '#826B03', 'background': '#FFFFFF'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#FF6A00', 'background': '#FFFFFF'}

ip.Percolator(text).insertfilter(cdg)

# Global variable to store the current file path
current_filepath = None

# Bind keys for opening and saving files
root.bind("<Control-s>", lambda x: save_file(root, text))
root.bind("<Control-o>", lambda x: open_file(root, text))
root.bind("<Control-n>", lambda x: new_file())
root.bind("<F5>", lambda x: run_file())


def new_file():
    print("new_file")
    global current_filepath  # Added global declaration
    text.delete(1.0, tk.END)
    del current_filepath
    root.title("LitePy 1.0")


def open_file(root, text):
    print("open_file")
    global current_filepath
    filepath = askopenfilename(filetypes=[("Python Script", "*.py"), ("Python Script Window", "*.pyw")])  # Fixed file types
    if not filepath:
        return
    text.delete(1.0, tk.END)
    try:
        with open(filepath, "r") as f:
            content = f.read()
            text.insert(tk.END, content)
            current_filepath = filepath  # Update current file path
    except IOError as e:
        messagebox.showerror("Error", f"Error opening file: {e}")
    root.title(f"LitePy 1.0: {filepath}")


def save_file(root, text):
    print("save_file")
    global current_filepath
    if current_filepath:  # Check if a file is already opened
        try:
            with open(current_filepath, "w") as f:
                content = text.get(1.0, tk.END)
                f.write(content.rstrip('\n'))  # Avoid adding an extra newline
            root.title(f"LitePy 1.0: {current_filepath}")
        except IOError as e:
            messagebox.showerror("Error", f"Error saving file: {e}")
    else:
        # If no current file, prompt to save as
        filepath = asksaveasfilename(filetypes=[("Python Script", "*.py"), ("Text File", "*.txt")])
        if filepath:
            current_filepath = filepath  # Update current filepath
            save_file(root, text)  # Try saving again with the new path

# Run file in python interpreter
def run_file():
    print("run_file")
    save_file(root, text)
    global current_filepath
    if current_filepath and os.path.isfile(current_filepath):
        subprocess.run(['python', "-i", current_filepath])  # Fixed variable name
    else:
        print(f"File {current_filepath} does not exist.")


def py_doc():
    print("py_doc")
    webbrowser.open('https://docs.python.org/3/')

def new_about():
    print("new_about")
    about = Toplevel()
    about.title("About LitePy")
    tk.Label(about, text='LitePy 1.0\n\nBy: Sebastian Taylor\nReleased:<date>\nBuild: 0001').pack(padx=30, pady=30)
# TODO: MAKE
#def new_find():
#   


# Menu bar setup
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New Script", command=new_file, accelerator="Ctrl+N")  # Fixed command binding
file_menu.add_command(label="Open", command=lambda: open_file(root, text), accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=lambda: save_file(root, text), accelerator="Ctrl+S")
menu_bar.add_cascade(label="File", menu=file_menu)

run_menu = tk.Menu(menu_bar, tearoff=0)
run_menu.add_command(label="Run Script", command=run_file, accelerator="F5")
menu_bar.add_cascade(label="Run", menu=run_menu)


#srch_menu = tk.Menu(menu_bar, tearoff=0)
#srch_menu.add_command(label="Find in script", command=None)#<< IMPLEMENT
#menu_bar.add_cascade(label="Search", menu=srch_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Python Docs", command=py_doc)
help_menu.add_command(label="About LitePy", command=new_about)
menu_bar.add_cascade(label="Help", menu=help_menu)


root.config(menu=menu_bar)
