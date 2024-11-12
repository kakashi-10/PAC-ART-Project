
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox
import mysql.connector
import re


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Downloads\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def link():
    window.destroy()
    import SignUp
    SignUp.create_menu_window()

def is_valid_email(email):
    # Biểu thức chính quy để kiểm tra định dạng email
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def signin():
    global email, password
    if email.get() == '' or password.get() == '': 
        messagebox.showerror('Error', 'Please fill in all fields')
    elif not is_valid_email(email.get()):
        messagebox.showerror('Error', 'Invalid email format. Please enter a valid email.')
    else:
        try:
            # Connect to MySQL database
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Haimot@10',  # Replace with your MySQL password
                database='pac_art'  # Replace with your database name
            )
            cursor = db.cursor()

            # Check email and password
            sql = "SELECT * FROM user WHERE email = %s AND password = %s"
            values = (email.get(), password.get())
            cursor.execute(sql, values)
            result = cursor.fetchone()

            if result:
                messagebox.showinfo('Success', 'Login successful!')
                window.destroy()
                import Menu  # Ensure Menu.py is in the project directory
                Menu.create_menu_window()
            else:
                messagebox.showerror('Error', 'Invalid email or password')
        except mysql.connector.Error as err:
            messagebox.showerror('Error', f"Something went wrong: {err}")
        finally:
            cursor.close()
            db.close()  # Ensure the database connection is closed


def create_menu_window():
    global window, email, password
    window = Tk()

    window.geometry("1000x600")
    window.configure(bg = "#D9D9D9")


    canvas = Canvas(
        window,
        bg = "#D9D9D9",
        height = 600,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        197.0,
        600.0,
        fill="#1F92E5",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        656.5,
        375.0,
        image=entry_image_1
    )
    password = Entry(
        bd=0,
        bg="#F5F5F5",
        fg="#000716",
        highlightthickness=0,
        show='*'
    )
    password.place(
        x=428.0,
        y=355.0,
        width=457.0,
        height=38.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        656.5,
        279.0,
        image=entry_image_2
    )
    email = Entry(
        bd=0,
        bg="#F5F5F5",
        fg="#000716",
        highlightthickness=0
    )
    email.place(
        x=428.0,
        y=259.0,
        width=457.0,
        height=38.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        217.0,
        295.0,
        image=image_image_1
    )

    canvas.create_text(
        422.0,
        318.0,
        anchor="nw",
        text="Password:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        423.0,
        215.0,
        anchor="nw",
        text="Email:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    sign_in = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=signin,
        relief="flat"
    )
    sign_in.place(
        x=502.0,
        y=430.0,
        width=310.0,
        height=48.0
    )

    canvas.create_text(
        521.0,
        62.0,
        anchor="nw",
        text="Sign In",
        fill="#000000",
        font=("Inter Bold", 36 * -1)
    )

    canvas.create_text(
        422.0,
        505.0,
        anchor="nw",
        text="Don’t have an account ?",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    link_sign_up = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=link,
        relief="flat"
    )
    link_sign_up.place(
        x=607.0,
        y=502.0,
        width=74.0,
        height=27.0
    )
    window.resizable(False, False)
    window.mainloop()

# Main application logic wrapped under if __name__ == "__main__"
if __name__ == "__main__":
    create_menu_window()  # Start the application with the menu window
