#If you wanna run this, first enter this command in your terminal (not in VS Code):
# brew install python-tk@3.12
# or brew install python-tk@3.13

import tkinter as tk

root = tk.Tk()
root.title("Hello Tkinter")
tk.Label(root, text="Welcome to Tkinter!").pack()
tk.Button(root, text="Click me", command=root.quit).pack()
root.mainloop()
