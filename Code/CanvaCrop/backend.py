import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd

class MockupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mockup Overlay Application")
        self.root.geometry("400x600")
        
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TListbox', font=('Arial', 10))

        # Frame for mockup list
        frame_mockup_list = ttk.Frame(root, padding="10")
        frame_mockup_list.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_mockup_list, text="Select Mockup(s):").pack(anchor=tk.W)
        
        self.mockup_listbox = tk.Listbox(frame_mockup_list, selectmode=tk.MULTIPLE, height=8)
        self.mockup_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Frame for image upload and overlay buttons
        frame_buttons = ttk.Frame(root, padding="10")
        frame_buttons.pack(fill=tk.BOTH, expand=True)
        
        self.upload_button = ttk.Button(frame_buttons, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)
        
        self.overlay_button = ttk.Button(frame_buttons, text="Overlay Image", command=self.overlay_image)
        self.overlay_button.pack(pady=5)
        
        # Frame for image preview
        frame_preview = ttk.Frame(root, padding="10")
        frame_preview.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_preview, text="Image Preview:").pack(anchor=tk.W)
        self.image_label = ttk.Label(frame_preview)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Load mockups from CSV
        self.mockups_df = pd.read_csv("../../data/mockup819new.csv")
        for mockup in self.mockups_df['image_id'].tolist():
            self.mockup_listbox.insert(tk.END, mockup)

        self.selected_image_path = None
        self.save_directory = "/Users/matt/Pictures/Midjourney/Imagine/Downloads"  # Set your save directory here

    def upload_image(self):
        initial_dir = "/Users/matt/Pictures/Midjourney/Imagine/Downloads"  # Set your initial directory here
        self.selected_image_path = filedialog.askopenfilename(initialdir=initial_dir)
        if self.selected_image_path:
            img = Image.open(self.selected_image_path)
            img.thumbnail((200, 200))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def overlay_image(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "No image selected")
            return

        selected_mockups = [self.mockup_listbox.get(i) for i in self.mockup_listbox.curselection()]
        if not selected_mockups:
            messagebox.showerror("Error", "No mockup selected")
            return

        for mockup in selected_mockups:
            self.perform_overlay(mockup, self.selected_image_path)

    def perform_overlay(self, mockup_name, image_path):
        mockup_info = self.mockups_df[self.mockups_df['image_id'] == mockup_name].iloc[0]
        mockup_path = mockup_info['image_path']
        top, left, height, width = mockup_info['top'], mockup_info['left'], mockup_info['height'], mockup_info['width']

        mockup_img = Image.open(mockup_path)
        overlay_img = Image.open(image_path)

        overlay_img = overlay_img.resize((int(width), int(height)))

        mockup_img.paste(overlay_img, (int(left), int(top)))

        # Extract prefix from overlay image filename
        overlay_image_name = os.path.basename(image_path)
        prefix = overlay_image_name.split('_')[0]

        # Generate the new filename
        new_filename = f"{prefix}_{mockup_name}"

        # Save the image automatically to the set directory
        save_path = os.path.join(self.save_directory, new_filename)
        mockup_img.save(save_path)
        messagebox.showinfo("Success", f"Image saved as {new_filename} in {self.save_directory}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MockupApp(root)
    root.mainloop()
