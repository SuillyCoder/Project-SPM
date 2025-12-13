#If you wanna run this, first enter this command in your terminal (not in VS Code):
# brew install python-tk@3.12
# or brew install python-tk@3.13

import tkinter as tk
#rom matplotlib import pyplot as plt

root = tk.Tk()
root.geometry("800x500")
root.title("Project SPM - TKinter Setup")


tk.Label(root, text="PROJECT S.P.M.", font=('Times New Roman', '30')).pack(padx = 20, pady = 20)

tk.Text(root, height=5, width=20).pack()

tk.Label(root, text="PROJECT S.P.M.", font=('Put stuff in the line', '10')).pack(padx = 10, pady = 10)
tk.Entry(root).pack(padx = 10, pady = 10)

buttonFrame = tk.Frame(root).columnconfigure(0, weight=1)
surprise = tk.Button(buttonFrame, text="CLICK ME FOR A SURPRISE!", command=root.quit).pack()

tk.Frame(root, width=200, height=100, bg="blue").pack(padx = 10, pady = 10)

root.mainloop()
