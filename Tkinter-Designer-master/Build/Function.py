
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import OptionMenu, StringVar, Text, Tk, Canvas, Button, PhotoImage, messagebox, filedialog, Listbox, Scrollbar, Scale, Label,  END
from PIL import Image, ImageTk
import os
from io import BytesIO
import cv2
import mysql.connector
import numpy as np
import requests
import threading
from globals import user_session


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\FPTSHOP\Downloads\PAC-ART-Project-main\PAC-ART-Project-main\Tkinter-Designer-master\Build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Global variable to hold the edited image
edited_image = None
sharpness_slider = None
color_correction_sliders = None

# Global variables for sliders
brightness_slider = None
contrast_slider = None

loaded_image = None
current_image = None


IMAGE_WIDTH = 750  # Set the desired width for resizingz

# Biến để theo dõi trạng thái hiển thị của các slider
brightness_visible = False
sharpness_visible = False
color_correction_visible = False

image_size_label = None
scale_value = 0.7  # Tỷ lệ mặc định

is_visible = False
textbox = None
dropdown = None

# Biến toàn cục để lưu cửa sổ loading
loading_window = None

# Thêm biến toàn cục để lưu lịch sử ảnh
image_history = []

window = None


# Function to go back to the Menu page
def back():
    global window
    if window:
        response = messagebox.askyesno("Confirmation", "Are you sure you want to go back to Menu?")
        if response:
            window.destroy()
            window = None  # Đặt lại window
            import Menu
            Menu.create_menu_window(image_path=None, folder_images=None)


# Function to load and display the selected image
def load_selected_image(image_path):
    global current_image, edited_image
    try:
        img = Image.open(image_path).convert('RGB')
        img_resized = img.resize((IMAGE_WIDTH, int(IMAGE_WIDTH * img.height / img.width)))  # Correct resizing
        current_image = img
        edited_image = img
        display_image(img_resized)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading image: {e}")


def display_image(image):
    img_resized = image.resize((int(IMAGE_WIDTH * scale_value), int((IMAGE_WIDTH * scale_value) * image.height / image.width)))  # Đảm bảo tỷ lệ
    img_tk = ImageTk.PhotoImage(img_resized)

    # Tính toán tọa độ để căn giữa
    x = 375  # Giữa canvas có chiều rộng 700
    y = 350  # Giữa canvas có chiều cao 700

    canvas.create_image(x, y, image=img_tk, anchor="center")
    canvas.image = img_tk  # Giữ tham chiếu để tránh thu gom rác


def load_folder_images(folder_images):
    global listbox
    listbox.delete(0, 'end')
    for img in folder_images:
        listbox.insert("end", os.path.basename(img))
    listbox.bind('<<ListboxSelect>>', lambda event: display_selected_image(folder_images))


def display_selected_image(folder_images):
    # Lấy ảnh đã chọn
    selected_image = listbox.get(listbox.curselection())
    img_path = next(img for img in folder_images if os.path.basename(img) == selected_image)
    load_selected_image(img_path)
    


# # Function to export the displayed image

def exportimage():
    global edited_image
    if edited_image:
        # Hộp thoại lưu tệp
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
            filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"), ("All files", ".*")])
        
        if file_path:
            try:
                # Lấy tên ảnh từ đường dẫn
                name_image = os.path.basename(file_path)

                # Kết nối tới cơ sở dữ liệu
                db = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database=''
                )
                cursor = db.cursor()

                # Kiểm tra xem ảnh đã tồn tại trong cơ sở dữ liệu chưa
                check_sql = "SELECT COUNT(*) FROM edited_image WHERE name_image = %s"
                cursor.execute(check_sql, (name_image,))
                exists = cursor.fetchone()[0]

                if exists > 0:
                    # Nếu ảnh đã tồn tại, không lưu vào database và không lưu file
                    messagebox.showwarning("File Exists", f"An image with the name '{name_image}' already exists in the database.")
                else:
                    # Lưu ảnh đã chỉnh sửa ra file
                    edited_image.save(file_path)
                    messagebox.showinfo("Export Successful", f"Image has been saved to: {file_path}")

                    # Đọc dữ liệu ảnh dưới dạng nhị phân
                    with open(file_path, 'rb') as file:
                        image_data = file.read()

                    # Lệnh INSERT vào bảng edited_image
                    sql = "INSERT INTO edited_image (name_image, image_data, user_id) VALUES (%s, %s, %s)"
                    values = (name_image, image_data, user_session.user_id)
                    cursor.execute(sql, values)
                    db.commit()

                    # Thông báo thành công chỉ khi ảnh được thêm vào cơ sở dữ liệu
                    print("Edited image added to database successfully.")

            except mysql.connector.Error as db_error:
                messagebox.showerror("Database Error", f"Error occurred while saving to the database: {db_error}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Error occurred while saving the image: {e}")
            finally:
                if cursor:
                    cursor.close()
                if db:
                    db.close()
        else:
            messagebox.showwarning("No File Selected", "Please select a file to save the image.")
    else:
        messagebox.showwarning("No Image", "No image to export.")

# Hàm nâng cao ảnh sử dụng DeepAI API với văn bản đầu vào
def other(image, text_input=None):
    img_array = np.array(image)
    _, img_encoded = cv2.imencode('.png', img_array)
    img_bytes = img_encoded.tobytes()

    api_url = ""
    headers = {
        'api-key': ""
    }
    
    files = {'image': img_bytes}
    if text_input:
        files['text'] = text_input.encode('utf-8')
    
    response = requests.post(api_url, headers=headers, files=files)
    
    if response.status_code == 200:
        output_url = response.json().get('output_url')
        enhanced_img_data = requests.get(output_url).content
        enhanced_img_array = np.frombuffer(enhanced_img_data, np.uint8)
        enhanced_img = cv2.imdecode(enhanced_img_array, cv2.IMREAD_COLOR)
        return Image.fromarray(enhanced_img)
    else:
        messagebox.showerror("Apply Failed", "Could not using DeepAI.")
        return image



def remove_background(image):
    img_array = np.array(image)
    _, img_encoded = cv2.imencode('.png', img_array)
    img_bytes = img_encoded.tobytes()

    api_url = ""
    headers = {
        'api-key': ""
    }
    files = {'image': img_bytes}

    response = requests.post(api_url, headers=headers, files=files)

    if response.status_code == 200:
        output_url = response.json().get('output_url')
        removed_bg_img_data = requests.get(output_url).content
        removed_bg_img_array = np.frombuffer(removed_bg_img_data, np.uint8)
        
        # Giải mã và tạo kênh alpha để có nền trong suốt
        removed_bg_img = cv2.imdecode(removed_bg_img_array, cv2.IMREAD_UNCHANGED)

        # Kiểm tra nếu hình ảnh có 4 kênh (BGRA)
        if removed_bg_img.shape[2] == 4:
            return Image.fromarray(removed_bg_img)
        else:
            # Nếu không có kênh alpha, thêm kênh alpha để tạo nền trong suốt
            b, g, r = cv2.split(removed_bg_img)
            alpha_channel = np.ones(b.shape, dtype=b.dtype) * 255  # Kênh alpha đầy
            removed_bg_img = cv2.merge((b, g, r, alpha_channel))
            return Image.fromarray(removed_bg_img)
    else:
        messagebox.showerror("Background Removal Failed", "Could not remove the background using DeepAI.")
        return image



def super_sesolution(image):
    img_array = np.array(image)
    _, img_encoded = cv2.imencode('.png', img_array)
    img_bytes = img_encoded.tobytes()

    api_url = ""
    headers = {
        'api-key': ""
    }
    files = {'image': img_bytes}

    response = requests.post(api_url, headers=headers, files=files)

    if response.status_code == 200:
        output_url = response.json().get('output_url')
        colorized_img_data = requests.get(output_url).content
        colorized_img_array = np.frombuffer(colorized_img_data, np.uint8)
        colorized_img = cv2.imdecode(colorized_img_array, cv2.IMREAD_COLOR)
        return Image.fromarray(colorized_img)
    else:
        messagebox.showerror("Super Resolution Failed", "Could not Super Resolution the image using DeepAI.")
        return image


def colorizer(image):
    try:
        # Chuyển ảnh sang mảng byte
        img_array = np.array(image)
        _, img_encoded = cv2.imencode('.png', img_array)
        img_bytes = img_encoded.tobytes()

        # Gửi yêu cầu tới API
        api_url = ""
        headers = {'"}
        files = {'image': img_bytes}

        response = requests.post(api_url, headers=headers, files=files)

        if response.status_code == 200:
            output_url = response.json().get('output_url')
            if not output_url:
                messagebox.showerror("Error", "Invalid output URL.")
                return image

            # Tải ảnh từ output_url
            colorized_img_data = requests.get(output_url).content
            if not colorized_img_data:
                messagebox.showerror("Error", "Failed to fetch colorized image.")
                return image

            # Giải mã mảng byte thành ảnh
            colorized_img_array = np.frombuffer(colorized_img_data, np.uint8)
            if len(colorized_img_array) == 0:
                messagebox.showerror("Error", "Image data is invalid.")
                return image

            colorized_img = cv2.imdecode(colorized_img_array, cv2.IMREAD_COLOR)
            if colorized_img is None:
                messagebox.showerror("Error", "Failed to decode image.")
                return image

            # Chuyển đổi sang định dạng PIL
            return Image.fromarray(cv2.cvtColor(colorized_img, cv2.COLOR_BGR2RGB))
        else:
            messagebox.showerror("Image Colorizer Failed", f"Error {response.status_code}: {response.text}")
            return image
    except Exception as e:
        messagebox.showerror("Exception", str(e))
        return image


def ai_selfie(image, text_input=None):
    # Chuyển đổi hình ảnh thành mảng numpy
    img_array = np.array(image)
    _, img_encoded = cv2.imencode('.png', img_array)
    img_bytes = img_encoded.tobytes()

    api_url = ""
    headers = {
        'api-key': ""
    }
    
    files = {'image': img_bytes}
    if text_input:
        files['text'] = text_input.encode('utf-8')
    
    response = requests.post(api_url, headers=headers, files=files)
    
    if response.status_code == 200:
        output_url = response.json().get('output_url')
        generated_img_data = requests.get(output_url).content
        generated_img_array = np.frombuffer(generated_img_data, np.uint8)
        generated_img = cv2.imdecode(generated_img_array, cv2.IMREAD_COLOR)
        generated_img = cv2.cvtColor(generated_img, cv2.COLOR_BGR2RGB)  # Chuyển đổi màu sắc
        return Image.fromarray(generated_img)
    else:
        messagebox.showerror("Generate Failed", "Could not use DeepAI.")
        return image


def adjust_brightness_and_contrast(image, brightness=0, contrast=0):
    img = np.array(image)
    brightness = np.clip(brightness, -100, 100)  # Giới hạn độ sáng
    contrast = np.clip(contrast, -100, 100)  # Giới hạn độ tương phản

    # Áp dụng độ tương phản
    img = cv2.convertScaleAbs(img, alpha=(contrast / 100 + 1), beta=brightness)

    # Đảm bảo không có giá trị âm
    img[img < 0] = 0
    img[img > 255] = 255

    return Image.fromarray(img)


def adjust_sharpness(image, sharpness=1.0):
    if sharpness < 0:
        sharpness = 0  # Ngăn độ sắc nét âm
    img = np.array(image)
    kernel = np.array([[0, -1, 0],
                       [-1, 5 + sharpness, -1],
                       [0, -1, 0]])
    img = cv2.filter2D(img, -1, kernel)

    return Image.fromarray(img)


def adjust_color_correction(image, r=1.0, g=1.0, b=1.0):
    img = np.array(image)
    img[:, :, 0] = cv2.multiply(img[:, :, 0], r)
    img[:, :, 1] = cv2.multiply(img[:, :, 1], g)
    img[:, :, 2] = cv2.multiply(img[:, :, 2], b)

    return Image.fromarray(img)


def apply_hdr_effect(image):
    # Convert the PIL image to a NumPy array
    img = np.array(image)

    # Check the number of channels and convert if necessary
    if img.ndim == 2:  # Grayscale image
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:  # If the image has an alpha channel
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

    # Ensure the image is in the correct format
    if img.dtype != np.uint8:
        img = img.astype(np.uint8)

    # Apply the bilateral filter
    hdr_img = cv2.bilateralFilter(img, d=15, sigmaColor=75, sigmaSpace=75)
    
    return Image.fromarray(hdr_img)


def save_image_state(image):
    global image_history
    # Lưu ảnh hiện tại vào lịch sử
    if len(image_history) >= 20:  # Giới hạn số lượng phiên bản lưu
        image_history.pop(0)  # Xóa phiên bản cũ nhất
    image_history.append(image.copy())  # Lưu ảnh hiện tại

def undo():
    global edited_image, image_history
    if len(image_history) > 1:
        # Lấy phiên bản trước đó
        image_history.pop()  # Xóa phiên bản hiện tại
        edited_image = image_history[-1]  # Lấy phiên bản trước
        display_image(edited_image)  # Hiển thị ảnh đã quay lại
    else:
        messagebox.showwarning("Warning", "No more actions to undo.")


def apply_all_adjustments():
    global current_image, edited_image
    if current_image:
        try:
            # Lưu trạng thái ảnh trước khi chỉnh sửa
            save_image_state(edited_image)  # Lưu phiên bản hiện tại

            brightness = brightness_slider.get() if brightness_slider and brightness_slider.winfo_exists() else 0
            contrast = contrast_slider.get() if contrast_slider and contrast_slider.winfo_exists() else 0
            sharpness = sharpness_slider.get() if sharpness_slider and sharpness_slider.winfo_exists() else 1.0
            
            r = color_correction_sliders[0].get() if color_correction_sliders and color_correction_sliders[0].winfo_exists() else 1.0
            g = color_correction_sliders[1].get() if color_correction_sliders and color_correction_sliders[1].winfo_exists() else 1.0
            b = color_correction_sliders[2].get() if color_correction_sliders and color_correction_sliders[2].winfo_exists() else 1.0

            img = adjust_brightness_and_contrast(current_image, brightness, contrast)
            img = adjust_sharpness(img, sharpness)
            img = adjust_color_correction(img, r, g, b)

            edited_image = img  
            display_image(img.resize((IMAGE_WIDTH, int(IMAGE_WIDTH * img.height / img.width))))
        except Exception as e:
            messagebox.showerror("Error", f"Error applying adjustments: {e}")



def adjust_image(image, brightness, contrast, sharpness):
    img = np.array(image)
    img = cv2.convertScaleAbs(img, alpha=(contrast / 100 + 1), beta=brightness)
    img = cv2.filter2D(img, -1, np.array([[0, -1, 0], [-1, 5 + sharpness, -1], [0, -1, 0]]))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def toggle_brightness_contrast_sliders():
    global brightness_slider, contrast_slider, brightness_visible
    if window and window.winfo_exists():
        if not brightness_visible:
            brightness_slider = Scale(window, from_=-100, to=100, label='Brightness', orient='horizontal',
                                       command=lambda _: apply_all_adjustments())
            brightness_slider.place(x=750, y=50)
            contrast_slider = Scale(window, from_=-100, to=100, label='Contrast', orient='horizontal',
                                    command=lambda _: apply_all_adjustments())
            contrast_slider.place(x=750, y=100)
            brightness_visible = True
        else:
            # Kiểm tra nếu các slider đã được tạo ra và tồn tại trước khi ẩn
            if brightness_slider and brightness_slider.winfo_exists():
                brightness_slider.place_forget()
            if contrast_slider and contrast_slider.winfo_exists():
                contrast_slider.place_forget()
            brightness_visible = False


def toggle_sharpness_slider():
    global sharpness_slider, sharpness_visible
    if window and window.winfo_exists():
        if not sharpness_visible:
            sharpness_slider = Scale(window, from_=0, to=100, label='Sharpness', orient='horizontal',
                                     command=lambda _: apply_all_adjustments())
            sharpness_slider.place(x=750, y=160)
            sharpness_visible = True
        else:
            # Kiểm tra nếu sharpness_slider đã được tạo ra và tồn tại trước khi ẩn
            if sharpness_slider and sharpness_slider.winfo_exists():
                sharpness_slider.place_forget()
            sharpness_visible = False
            sharpness_slider = None  # Đặt lại biến sau khi ẩn


def toggle_color_correction_sliders():
    global color_correction_sliders, color_correction_visible
    if window and window.winfo_exists():
        if not color_correction_visible:
            r_slider = Scale(window, from_=0, to=3, resolution=0.1, label='Red', orient='horizontal',
                             command=lambda _: apply_all_adjustments())
            r_slider.place(x=750, y=220)

            g_slider = Scale(window, from_=0, to=3, resolution=0.1, label='Green', orient='horizontal',
                             command=lambda _: apply_all_adjustments())
            g_slider.place(x=750, y=270)

            b_slider = Scale(window, from_=0, to=3, resolution=0.1, label='Blue', orient='horizontal',
                             command=lambda _: apply_all_adjustments())
            b_slider.place(x=750, y=320)

            color_correction_sliders = (r_slider, g_slider, b_slider)
            color_correction_visible = True
        else:
            # Kiểm tra từng slider trước khi ẩn
            if color_correction_sliders:
                for slider in color_correction_sliders:
                    if slider and slider.winfo_exists():
                        slider.place_forget()
            color_correction_visible = False
            color_correction_sliders = None  # Đặt lại biến sau khi ẩn


def toggle_hdr_button():
    global current_image, edited_image
    if current_image:
        try:
            img = apply_hdr_effect(current_image)  
            img_resized = img.resize((IMAGE_WIDTH, int(IMAGE_WIDTH * img.height / img.width)))  
            img_tk = ImageTk.PhotoImage(img_resized)  
            edited_image = img
            
            canvas.create_image(375, 350, image=img_tk, anchor="center")  
            canvas.image = img_tk  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply HDR effect: {e}")
    else:
        messagebox.showwarning("Warning", "No image loaded to apply HDR effect.")


# Hàm hiển thị và ẩn textbox cùng dropdown
def toggle_ai_textbox_and_dropdown():
    global is_visible, textbox, dropdown, dropdown_value, action_button

    if window and window.winfo_exists():
        if not is_visible:
            textbox = Text(window, height=3, width=35)
            textbox.place(x=800, y=390)

             # Thiết lập hint text
            hint_text = "Anime changed, Gray, Pixelation, Sky Replacement, Frame and Border Addition, Light and Shadow Enhancement"
            textbox.insert(1.0, hint_text)
            textbox.tag_add("hint", 1.0, "end")  # Thêm tag cho hint text
            textbox.tag_config("hint", foreground="lightgray")  # Màu mờ cho hint text
            textbox.bind("<FocusIn>", lambda e: clear_hint(textbox, hint_text))
            textbox.bind("<FocusOut>", lambda e: set_hint(textbox, hint_text))

            options = ["Background Remover", "Super Resolution", "Colorizer", "AI Selfie", "Other"]
            dropdown_value = StringVar(window)
            dropdown_value.set("Options")
            dropdown = OptionMenu(window, dropdown_value, *options)
            dropdown.place(x=840, y=445)

            action_button = Button(
                window,
                text="Run",
                command=ai_action
            )
            action_button.place(x=1000, y=445)

            is_visible = True
        else:
            if textbox and textbox.winfo_exists():
                textbox.place_forget()
            if dropdown and dropdown.winfo_exists():
                dropdown.place_forget()
            if action_button and action_button.winfo_exists():
                action_button.place_forget()

            is_visible = False
            textbox = None
            dropdown = None
            action_button = None

def clear_hint(textbox, hint_text):
    if textbox.get(1.0, "end-1c") == hint_text:
        textbox.delete(1.0, "end")
        textbox.config(fg="black")  # Đổi màu chữ về màu chính khi xóa hint

def set_hint(textbox, hint_text):
    if textbox.get(1.0, "end-1c") == "":
        textbox.insert(1.0, hint_text)
        textbox.tag_add("hint", 1.0, "end")  # Thêm tag cho hint text
        textbox.config(fg="lightgray")  # Đổi màu chữ về màu mờ

def show_loading():
    global loading_window  # Sử dụng biến toàn cục
    loading_window = Tk()
    loading_window.title("Loading")
    loading_window.geometry("200x100")

    # Lấy kích thước màn hình
    screen_width = loading_window.winfo_screenwidth()
    screen_height = loading_window.winfo_screenheight()

    # Tính toán vị trí để đặt hộp thoại ở giữa
    x = (screen_width // 2) - (200 // 2)
    y = (screen_height // 2) - (100 // 2)

    # Đặt vị trí cho hộp thoại
    loading_window.geometry(f"200x100+{x}+{y}")
    
    loading_label = Label(loading_window, text="Applying effect, please wait...")
    loading_label.pack(pady=20)

    loading_window.update()  # Cập nhật giao diện


def hide_loading(success_message):
    global loading_window
    if loading_window:
        loading_window.destroy()  # Đóng cửa sổ loading
        loading_window = None  # Đặt lại biến
    messagebox.showinfo("Success", success_message)


def ai_action():
    global textbox, edited_image, current_image  # Thêm current_image vào biến toàn cục
    selected_option = dropdown_value.get()

    if textbox is None or not textbox.winfo_exists():
        messagebox.showwarning("Warning", "Textbox is not available.")
        return

    input_text = textbox.get("1.0", "end-1c").strip()

    def process_action():
        global edited_image, current_image
        if selected_option == "Background Remover":
            if current_image:
                show_loading()  # Hiển thị loading
                img = remove_background(current_image)
                edited_image = img  
                current_image = img  # Cập nhật current_image
                display_image(img)
                hide_loading("Background removed successfully!")
            else:
                messagebox.showwarning("Warning", "No image loaded to process.")

        elif selected_option == "Super Resolution":
            if current_image:
                show_loading()  # Hiển thị loading
                img = super_sesolution(current_image)
                edited_image = img  
                current_image = img  # Cập nhật current_image
                display_image(img)
                hide_loading("Super Resolution successfully!")
            else:
                messagebox.showwarning("Warning", "No image loaded to process.")

        elif selected_option == "Colorizer":
            if current_image:
                show_loading()  # Hiển thị loading
                img = colorizer(current_image)
                edited_image = img  
                current_image = img  # Cập nhật current_image
                display_image(img)
                hide_loading("Image Colorizer successfully!")
            else:
                messagebox.showwarning("Warning", "No image loaded to process.")

        elif selected_option == "AI Selfie":
            if current_image:
                show_loading()  # Hiển thị loading
                img = ai_selfie(current_image, input_text)
                edited_image = img  
                current_image = img  # Cập nhật current_image
                display_image(img)
                hide_loading("AI Selfie successfully!")
            else:
                messagebox.showwarning("Warning", "No image loaded to process.")        

        elif selected_option == "Other":
            if current_image:
                show_loading()  # Hiển thị loading
                img = other(current_image, input_text)
                edited_image = img  
                current_image = img  # Cập nhật current_image
                display_image(img)
                hide_loading("Image update successfully!")
            else:
                messagebox.showwarning("Warning", "No image loaded to process.")

    # Sử dụng threading để không làm treo giao diện
    threading.Thread(target=process_action).start()


def zoom_image(event):
    global scale_value
    if event.delta > 0:  # Zoom in
        scale_value = min(scale_value + 0.1, 1.0)  # Limit max zoom
    else:  # Zoom out
        scale_value = max(scale_value - 0.1, 0.1)  # Limit min zoom
    
    if edited_image:
        display_image(edited_image)
    elif current_image:
        display_image(current_image)


def create_menu_window(image_path=None, folder_images=None):
    global window, canvas, listbox, dropdown_value
    window = Tk()

    window.geometry("1100x700")
    window.configure(bg = "#F5F5F5")

    # Biến để lưu giá trị dropdown
    dropdown_value = StringVar(window)
    dropdown_value.set("Lựa chọn")  # Giá trị mặc định

    canvas = Canvas(
        window,
        bg = "#EDEDED",
        height = 700,
        width = 1100,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        750.0,
        700.0,
        fill="#D9D9D9",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    brightness_and_contrast = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=toggle_brightness_contrast_sliders,
        relief="flat"
    )
    brightness_and_contrast.place(
        x=870.0,
        y=63.0,
        width=150.0,
        height=40.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    hdr = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=toggle_hdr_button,
        relief="flat"
    )
    hdr.place(
        x=870.0,
        y=273.0,
        width=150.0,
        height=40.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    ai = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=toggle_ai_textbox_and_dropdown,
        relief="flat"
    )
    ai.place(
        x=870.0,
        y=343.0,
        width=150.0,
        height=40.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    sharpness = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=toggle_sharpness_slider,
        relief="flat"
    )
    sharpness.place(
        x=870.0,
        y=133.0,
        width=150.0,
        height=40.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    color_correction = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=toggle_color_correction_sliders,
        relief="flat"
    )
    color_correction.place(
        x=870.0,
        y=203.0,
        width=150.0,
        height=40.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    back_button = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=back,
        relief="flat"
    )
    back_button.place(
        x=1047.0,
        y=9.0,
        width=40.0,
        height=40.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    export_image = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=exportimage,
        relief="flat"
    )
    export_image.place(
        x=760.0,
        y=9.0,
        width=40.0,
        height=40.0
    )

    canvas.create_rectangle(
        700.0,
        580.0,
        1100.0,
        700.0,
        fill="#D9D9D9",
        outline="")

    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    Undo = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=undo,
        relief="flat"
    )
    Undo.place(
        x=760.0,
        y=526.0,
        width=30.0,
        height=30.0
    )

    window.bind("<MouseWheel>", zoom_image)

    if image_path:
        load_selected_image(image_path)

    if folder_images:
        scrollbar = Scrollbar(window)
        scrollbar.place(x=1080, y=565, height=130)
        listbox = Listbox(window, yscrollcommand=scrollbar.set)
        listbox.place(x=750, y=580, width=330, height=130)
        scrollbar.config(command=listbox.yview)
        load_folder_images(folder_images)

    window.resizable(False, False)
    window.mainloop()

# # Main application logic wrapped under if __name__ == "__main__"
# if __name__ == "__main__":
#     create_menu_window()  # Start the application with the menu window
