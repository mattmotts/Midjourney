# upload_overlay.py
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class UploadOverlayApp:
    def __init__(self, root, selected_mockups, next_step_callback):
        self.root = root
        self.root.title("Upload Image")
        self.root.geometry("400x600")
        self.selected_mockups = selected_mockups
        self.next_step_callback = next_step_callback

        frame_buttons = ttk.Frame(root, padding="10")
        frame_buttons.pack(fill=tk.BOTH, expand=True)

        self.upload_button = ttk.Button(frame_buttons, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        frame_preview = ttk.Frame(root, padding="10")
        frame_preview.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_preview, text="Image Preview:").pack(anchor=tk.W)
        self.image_label = ttk.Label(frame_preview)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        ttk.Button(root, text="Next", command=self.save_image_path_and_proceed).pack(pady=10)

        self.selected_image_path = None

    def upload_image(self):
        initial_dir = '/Users/matt/Pictures/Midjourney/Imagine/Downloads'  # Set your initial directory here
        self.selected_image_path = filedialog.askopenfilename(initialdir=initial_dir)
        if self.selected_image_path:
            img = Image.open(self.selected_image_path)
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def save_image_path_and_proceed(self):
        if not self.selected_image_path:
            tk.messagebox.showerror("Error", "No image selected")
            return
        self.next_step_callback(self.selected_mockups, self.selected_image_path)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UploadOverlayApp(root, ["mockup1", "mockup2"], lambda x, y: print(f"Selected mockups: {x}, Image: {y}"))
    root.mainloop()
