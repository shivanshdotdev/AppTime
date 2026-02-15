import tkinter as tk
from tkinter import ttk, messagebox as mb


root = tk.Tk()
root.withdraw()  

def ui_for_usage_log():

    window = tk.Toplevel(root)
    window.protocol("WM_DELETE_WINDOW", window.destroy)

    window.title("Log Viewer")
    window.geometry('400x300')

    with open(PERSISTENT_FILE, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(list(data.items()), columns=["App", "Duration"])

    tree = ttk.Treeview(window, columns=list(df.columns), show="headings")

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", minwidth=180)

    tree.heading("App", text="App", anchor="center")
    tree.heading("Duration", text="Duration", anchor="center")

    # tree.insert(parent=, index=, values=)


    # # Insert data
    # for row in df.itertuples(index=False):
    #     tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def clear_usage_log():
        global PERSISTENT_FILE
        PERSISTENT_FILE.write_text("{}")

    ttk.Button(window, text="Close", command=window.destroy).pack()
    ttk.Button(window, text="Clear", command=clear_usage_log).pack()

def program_exits():
    root.destroy()

root.mainloop()