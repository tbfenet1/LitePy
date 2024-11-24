# Import the required libraries
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os
import subprocess
import webbrowser


# Function to update line numbers
def update_line_numbers(event=None):
    text_content = text.get("1.0", "end-1c")
    lines = text_content.count("\n") + 1
    line_numbers = "\n".join(str(i) for i in range(1, lines + 1))
    line_number_text.config(state='normal')
    line_number_text.delete("1.0", "end")
    line_number_text.insert("1.0", line_numbers)
    line_number_text.config(state='disabled')


# Create an instance of tkinter frame or window
root = Tk()
root.title("LitePy 2.0")
# Set the size of the window
root.geometry("900x550")

# Frame for line numbers and text widget
frame = Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Line number widget
line_number_text = Text(frame, width=4, padx=3, takefocus=0, border=0, background='#eaeaea', state='disabled')
line_number_text.pack(side=tk.LEFT, fill=tk.Y)

# Main Text widget with undo is set
text = Text(frame, undo=True, wrap=tk.NONE)
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add vertical scrollbar
scrollbar = Scrollbar(frame, command=text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scrollbar.set)

# Sync line numbers to the main text widget
text.bind("<KeyRelease>", update_line_numbers)
text.bind("<MouseWheel>", update_line_numbers)

font = tkfont.Font(font=text['font'])
tab = font.measure('    ')
text.config(tabs=tab)
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

# Add bindings and other functions (no changes needed)
root.bind("<Control-s>", lambda x: save_file(root, text))
root.bind("<Control-o>", lambda x: open_file(root, text))
root.bind("<Control-n>", lambda x: new_file())
root.bind("<F5>", lambda x: run_file())
root.bind("<Control-t>", lambda x: temp_tk_ex())


def new_file():
    global current_filepath  # Added global declaration
    text.delete(1.0, tk.END)
    current_filepath = None
    root.title("LitePy 2.0")
    update_line_numbers()


def open_file(root, text):
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
    root.title(f"LitePy 2.0: {filepath}")
    update_line_numbers()


def save_file(root, text):
    global current_filepath
    if current_filepath:  # Check if a file is already opened
        try:
            with open(current_filepath, "w") as f:
                content = text.get(1.0, tk.END)
                f.write(content.rstrip('\n'))  # Avoid adding an extra newline
            root.title(f"LitePy 2.0: {current_filepath}")
        except IOError as e:
            messagebox.showerror("Error", f"Error saving file: {e}")
    else:
        # If no current file, prompt to save as
        filepath = asksaveasfilename(filetypes=[("Python Script", "*.py"), ("Text File", "*.txt")])
        if filepath:
            current_filepath = filepath  # Update current filepath
            save_file(root, text)  # Try saving again with the new path


def run_file():
    save_file(root, text)
    global current_filepath
    if current_filepath and os.path.isfile(current_filepath):
        subprocess.run(['python', "-i", current_filepath])  # Fixed variable name
    else:
        print(f"File {current_filepath} does not exist.")


def py_doc():
    webbrowser.open('https://docs.python.org/3/')


def new_about():
    about = Toplevel()
    about.title("About LitePy")
    tk.Label(about, text='LitePy 2.0\nA simple Python Script Editor.\nBy: Sebastian Taylor\n\nBuild: 0002').pack(padx=30, pady=30)


def new_temp():
    window = tk.Toplevel(root)
    tk.Label(window, text="Select a template:").grid()
    tk.Button(window, text="Tkinter", command=temp_tk).grid()
    tk.Button(window, text="Tkinter Extended", command=temp_tk_ex).grid()
    window.geometry("100x100")


def temp_tk():
    text.delete(1.0, tk.END)
    text.insert(tk.END, '# Import required modules\nfrom tkinter import *\n# Create the window and add a title\nroot = Tk()\nroot.title("Tk")')
    update_line_numbers()


def temp_tk_ex():
    text.delete(1.0, tk.END)
    text.insert(tk.END, '# Import required modules\nfrom tkinter import *\n# Create the window and add a title\nroot = Tk()\nroot.title("Tk")\n\n# Create a menubar\nmenu_bar = Menu(root)\nfile_menu = Menu(menu_bar, tearoff=0)\nfile_menu.add_command(label="Blank Command", command=None, accelerator="<insert>")\nmenu_bar.add_cascade(label="File", menu=file_menu)\n\nroot.config(menu_bar)')
    update_line_numbers()


# Menu bar setup (unchanged)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New Script", command=new_file, accelerator="Ctrl+N")  # Fixed command binding
file_menu.add_command(label="Open", command=lambda: open_file(root, text), accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=lambda: save_file(root, text), accelerator="Ctrl+S")
menu_bar.add_cascade(label="File", menu=file_menu)

run_menu = tk.Menu(menu_bar, tearoff=0)
run_menu.add_command(label="Run Script", command=run_file, accelerator="F5")
menu_bar.add_cascade(label="Run", menu=run_menu)

ins_menu = tk.Menu(menu_bar, tearoff=0)
ins_menu.add_command(label="Templates", command=new_temp)
menu_bar.add_cascade(label="Insert", menu=ins_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Python Docs", command=py_doc)
help_menu.add_command(label="About LitePy", command=new_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Trigger initial line number update
update_line_numbers()

# Run the application
root.mainloop()
