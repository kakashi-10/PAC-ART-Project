
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox
import mysql.connector


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Downloads\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def link():
    window.destroy()
    import SignIn
    SignIn.create_menu_window()

def signup():
    global name, email, password
    if name.get() == '' or email.get() == '' or password.get() == '': 
        messagebox.showerror('Error', 'Please fill all the fields.')
    else:
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Haimot@10',
                database='pac_art'
            )
            cursor = db.cursor()

            sql = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
            values = (name.get(), email.get(), password.get()) 
            cursor.execute(sql, values)
            db.commit()

            messagebox.showinfo('Success', 'User registered successfully!')
            window.destroy()
            import SignIn
            SignIn.create_menu_window()
        except mysql.connector.Error as err:
            messagebox.showerror('Error', f"Something went wrong: {err}")

def create_menu_window():
    global window, name, email, password
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
        highlightthickness=0
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
        229.0,
        image=entry_image_2
    )
    name = Entry(
        bd=0,
        bg="#F5F5F5",
        fg="#000716",
        highlightthickness=0
    )
    name.place(
        x=428.0,
        y=209.0,
        width=457.0,
        height=38.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        656.5,
        300.0,
        image=entry_image_3
    )
    email = Entry(
        bd=0,
        bg="#F5F5F5",
        fg="#000716",
        highlightthickness=0
    )
    email.place(
        x=428.0,
        y=280.0,
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
        423.0,
        185.0,
        anchor="nw",
        text="Name:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        423.0,
        327.0,
        anchor="nw",
        text="Password:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        423.0,
        256.0,
        anchor="nw",
        text="Email:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    sign_up = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=signup,
        relief="flat"
    )
    sign_up.place(
        x=502.0,
        y=430.0,
        width=310.0,
        height=48.0
    )

    canvas.create_text(
        521.0,
        62.0,
        anchor="nw",
        text="Sign Up",
        fill="#000000",
        font=("Inter Bold", 36 * -1)
    )

    canvas.create_text(
        423.0,
        497.0,
        anchor="nw",
        text="Already have an account?",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    link_sign_in = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=link,
        relief="flat"
    )
    link_sign_in.place(
        x=623.0,
        y=489.0,
        width=75.0,
        height=36.0
    )
    window.resizable(False, False)
    window.mainloop()

# Main application logic wrapped under if __name__ == "__main__"
if __name__ == "__main__":
    create_menu_window()  # Start the application with the menu window

