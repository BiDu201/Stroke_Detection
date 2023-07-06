import tkinter as tk
from tkinter import messagebox
import pyodbc
import sys
import Main


def path_connect():
    server = server_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE=STROKE;UID={user};PWD={password}"
    return connection_string


def connect_to_database():
    try:
        conn = pyodbc.connect(path_connect())
        messagebox.showinfo("Thành công", "Đã kết nối đến database!")
        sys.argv.append(path_connect())
        window.destroy()
        Main.main()
        conn.close()
    except pyodbc.Error as e:
        messagebox.showerror("Không thể kết nối", str(e))


# Tạo cửa sổ
window = tk.Tk()
window.title("Kết nối SQL Server")
window.geometry("300x150")

# Tạo các widgets
server_label = tk.Label(window, text="Server:")
server_label.pack()
server_entry = tk.Entry(window)
server_entry.pack()

user_label = tk.Label(window, text="User:")
user_label.pack()
user_entry = tk.Entry(window)
user_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

connect_button = tk.Button(window, text="Kết nối", command=connect_to_database)
connect_button.pack(padx=5, pady=5)

server_entry.focus()

# Chạy giao diện chính
window.mainloop()
