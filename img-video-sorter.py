import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

# ---------------- CONFIG ----------------

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"}

import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

BACKGROUND_IMAGE = resource_path("mediasorterdragon.png")

# ---------------- FUNCTIONS ----------------

def choose_folder(var):
    folder = filedialog.askdirectory()
    if folder:
        var.set(folder)

def get_date_folder(file_path):
    timestamp = os.path.getmtime(file_path)
    date = time.localtime(timestamp)
    year = str(date.tm_year)
    month = f"{date.tm_mon:02d}"
    return year, month

def sort_media():
    source = source_var.get()
    pictures_root = pictures_var.get()
    videos_root = videos_var.get()

    if not source or not pictures_root or not videos_root:
        messagebox.showerror("Error", "Please select all folders.")
        return

    files = [
        f for f in os.listdir(source)
        if os.path.isfile(os.path.join(source, f))
    ]

    if not files:
        messagebox.showinfo("Info", "No files to sort.")
        return

    progress["maximum"] = len(files)
    progress["value"] = 0

    moved_images = 0
    moved_videos = 0

    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(source, filename)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        try:
            year, month = get_date_folder(file_path)

            if ext in IMAGE_EXTENSIONS:
                dest_folder = os.path.join(pictures_root, year, month)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_folder, filename))
                moved_images += 1

            elif ext in VIDEO_EXTENSIONS:
                dest_folder = os.path.join(videos_root, year, month)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_folder, filename))
                moved_videos += 1

        except Exception as e:
            print(f"Error moving {filename}: {e}")

        progress["value"] = index
        root.update_idletasks()

    messagebox.showinfo(
        "Done",
        f"Sorting complete!\n\nImages moved: {moved_images}\nVideos moved: {moved_videos}"
    )

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Media Sorter")
root.geometry("450x450")
root.resizable(False, False)

# Background image
bg_image = Image.open(BACKGROUND_IMAGE)
bg_image = bg_image.resize((450, 450))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=450, height=450)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Variables
source_var = tk.StringVar()
pictures_var = tk.StringVar()
videos_var = tk.StringVar()

# UI helper functions
def add_label(text, y):
    canvas.create_text(20, y, anchor="w", text=text, fill="white", font=("Arial", 10, "bold"))

def add_entry(var, y):
    entry = tk.Entry(root, textvariable=var, width=38)
    canvas.create_window(20, y, anchor="w", window=entry)

def add_button(command, y):
    btn = tk.Button(root, text="Browse", command=command)
    canvas.create_window(420, y, anchor="e", window=btn)

# UI layout
add_label("Source Folder (Mixed Media)", 30)
add_entry(source_var, 55)
add_button(lambda: choose_folder(source_var), 55)

add_label("Pictures Destination Folder", 100)
add_entry(pictures_var, 125)
add_button(lambda: choose_folder(pictures_var), 125)

add_label("Videos Destination Folder", 170)
add_entry(videos_var, 195)
add_button(lambda: choose_folder(videos_var), 195)

# Progress Bar
progress = ttk.Progressbar(root, length=380)
canvas.create_window(35, 255, anchor="w", window=progress)

# Sort Button
sort_button = tk.Button(
    root,
    text="Sort Media",
    command=sort_media,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12),
    height=2,
    width=18
)
canvas.create_window(225, 330, anchor="center", window=sort_button)

root.mainloop()