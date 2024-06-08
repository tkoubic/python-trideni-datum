import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS

def get_date_taken(path):
    try:
        image = Image.open(path)
        exif_data = image._getexif()
        if not exif_data:
            return None

        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                return value
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def sort_photos_by_month(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg', 'png', 'tiff', 'bmp')):
                file_path = os.path.join(root, file)
                date_taken = get_date_taken(file_path)
                if date_taken:
                    year_month = date_taken[:7].replace(':', '-')  # YYYY-MM formát
                    target_dir = os.path.join(folder_path, year_month)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    shutil.move(file_path, os.path.join(target_dir, file))

def open_folder():
    folder_path = filedialog.askdirectory(title="Vyberte složku s fotografiemi")
    if folder_path:
        sort_photos_by_month(folder_path)
        messagebox.showinfo("Hotovo", "Fotografie byly roztříděny podle měsíce pořízení.")

# Vytvoření hlavního okna
root = tk.Tk()
root.title("Třídění souborů")
root.geometry("300x200")

# Vytvoření tlačítka
btn_open = tk.Button(root, text="Vyberte složku", command=open_folder)
btn_open.pack(pady=20)

# Spuštění aplikace
root.mainloop()
