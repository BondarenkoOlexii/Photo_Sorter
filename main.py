from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk
import os
import shutil

image_paths = []  # Список шляхів до зображень
current_index = 0  # Поточний індекс зображення
folder_path_1 = None   #Шлях до нової папки
folder_path_2 = None   #Шлях до другої нової папки

def selection_folder():
    global image_paths, current_index

    folder_path = filedialog.askdirectory()
    if folder_path:
        image_paths.clear()
        image_paths.extend(
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        )

        if image_paths:
            current_index = 0
            show_image()
        else:
            label.config(text="There is no photo in the selected file", image="")
    else:
        label.config(text="File doesn't choose", image="")
    print(image_paths)


def show_image():
    global current_index

    if image_paths:
        image_path = image_paths[current_index]
        try:
            image = Image.open(image_path)
            image = image.resize((400, 300))
            photo = ImageTk.PhotoImage(image)


            label.config(image=photo, text=f"Photo: {os.path.basename(image_path)}")
            label.image = photo
        except FileNotFoundError:
            if current_index != len(image_paths) - 1:
                 current_index += 1
            else:
                current_index = 0
            show_image()
        except Exception as e:
            label.config(text=f"Error when open photo: {e}", image="")
    else:
        label.config(text="There is no photo in the selected file", image="")



def delete_message():
    global current_index, image_paths
    if image_paths:
        os.remove(image_paths[current_index])
        current_index += 1
    show_image()


def choose_folder_1():
    global folder_path_1
    if label.cget('text') == "" or label.cget("Can't display the photo") == "There is no photo in the selected file":
        folder_path_1 = None

    if folder_path_1 is None:
        folder_path_1 = filedialog.askdirectory()
    else:
        return folder_path_1

    if folder_path_1:
        folder_name = os.path.basename(folder_path_1)  # Отримати лише ім'я папки
        move_to_first_file.config(text=f"{folder_name}")  # Змінити текст кнопки
    else:
        move_to_first_file.config(text="File doesn't choose")

def Add_to_first_folder():
    global current_index, image_paths, folder_path_1
    choose_folder_1()

    if folder_path_1:
        if len(image_paths) != 0:
            image_path = image_paths[current_index]
            file_name = os.path.basename(image_path)
            destination_path = os.path.join(folder_path_1, file_name)
        else:
            label.config(text="Photo in file was ended :(")
        try:
            shutil.move(image_path, destination_path)
            image_paths.pop(current_index)
        except Exception as e:
            move_to_first_file.config(text=f"Error: {str(e)}")
    else:
        move_to_first_file.config(text="File doesn't choose")
    show_image()

def choose_folder_2():
    global folder_path_2
    if label.cget('text') == "Can't display the photo " or label.cget('text') == "There is no photo in the selected file":
        folder_path_2 = None

    if folder_path_2 is None:
        folder_path_2 = filedialog.askdirectory()
    else:
        return folder_path_2

    if folder_path_2:
        folder_name = os.path.basename(folder_path_2)  # Отримати лише ім'я папки
        move_to_second_file.config(text=f"{folder_name}")  # Змінити текст кнопки
    else:
        move_to_second_file.config(text="File doesn't choose")



def Add_to_second_folder():
    global current_index, image_paths, folder_path_2
    choose_folder_2()

    if folder_path_2:
        if len(image_paths) != 0:
            image_path = image_paths[current_index]
            file_name = os.path.basename(image_path)
            destination_path = os.path.join(folder_path_2, file_name)
        else:
            label.config(text="Photo in file was ended :(")
        try:
            shutil.move(image_path, destination_path)
            image_paths.pop(current_index)
        except Exception as e:
            move_to_second_file.config(text=f"Error: {str(e)}")
    else:
        move_to_second_file.config(text="File doesn't choose")
    show_image()



# Інтерфейс
window = Tk()
window.title("Photo Sorter")

window.geometry('1080x720')
window.title('PhotoSorter')

# Мітка для зображення
label = Label(window, text="Choose file, with photos", font=("Arial", 14))
label.pack(pady=20)

# Кнопки
select_folder_button = Button(window, text="Choose file", command=selection_folder, activebackground='grey')
select_folder_button.pack(pady=5)

delete_button = Button(window, text="Delete file", command=delete_message, activebackground='grey')
delete_button.place(x=500, y=500)

move_to_first_file = Button(window, text="Choose file", command=Add_to_first_folder, activebackground='grey')
move_to_first_file.place(x=150, y=500)

move_to_second_file = Button(window, text="Choose file", command=Add_to_second_folder, activebackground='grey')
move_to_second_file.place(x=850, y=500)


# Запуск програми
window.mainloop()
