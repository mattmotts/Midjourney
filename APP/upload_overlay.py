import tkinter as tk
from tkinter import filedialog

class UploadOverlayApp:
    def __init__(self, root, selected_mockups, next_step_callback):
        self.root = root
        self.root.title("Upload Overlay Image")
        self.selected_mockups = selected_mockups
        self.next_step_callback = next_step_callback

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.next_button = tk.Button(root, text="Next", state=tk.DISABLED, command=self.proceed)
        self.next_button.pack(pady=20)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(initialdir="/Users/matt/Pictures/Midjourney/Imagine/Downloads")
        if self.image_path:
            self.next_button.config(state=tk.NORMAL)

    def proceed(self):
        if self.image_path:
            self.next_step_callback(self.selected_mockups, self.image_path)
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UploadOverlayApp(root, [], lambda x, y: print(f"Selected mockups: {x}, Image path: {y}"))
    root.mainloop()
