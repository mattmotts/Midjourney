import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class UploadOverlayApp:
    def __init__(self, root, selected_mockups, next_step_callback, go_back_callback, selected_image_path=None):
        self.root = root
        self.selected_mockups = selected_mockups
        self.next_step_callback = next_step_callback
        self.go_back_callback = go_back_callback
        self.selected_image_path = selected_image_path

        self.setup_ui()

    def setup_ui(self):
        self.clear_window()  # Clear the window before displaying new content
        self.root.title("Overlay Selection")

        tk.Button(self.root, text="Upload Image", command=self.upload_image).pack(pady=20)

        # Show preview of selected image if available
        if self.selected_image_path:
            try:
                img = Image.open(self.selected_image_path)
                img.thumbnail((200, 200))  # Resizing the preview image
                img = ImageTk.PhotoImage(img)

                # Display the selected image preview
                self.preview_label = tk.Label(self.root, image=img)
                self.preview_label.image = img  # Keep a reference to avoid garbage collection
                self.preview_label.pack(pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open image: {e}")

        tk.Button(self.root, text="Next", command=self.on_next).pack(pady=10)
        tk.Button(self.root, text="Go Back", command=self.go_back_callback).pack(pady=10)

    def upload_image(self):
        self.selected_image_path = filedialog.askopenfilename(
            initialdir="/Users/matt/Pictures/Midjourney/Imagine/Downloads", 
            title="Select an Image",
            filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"), ("All files", "*.*"))
        )

        if self.selected_image_path:
            try:
                img = Image.open(self.selected_image_path)
                img.thumbnail((200, 200))  # Resizing the preview image
                img = ImageTk.PhotoImage(img)

                # Display the selected image preview
                self.preview_label = tk.Label(self.root, image=img)
                self.preview_label.image = img  # Keep a reference to avoid garbage collection
                self.preview_label.pack(pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open image: {e}")

    def on_next(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "No image selected")
            return
        # Proceed to the next step (perform_overlay)
        self.next_step_callback(self.selected_mockups, self.selected_image_path)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UploadOverlayApp(root, ["mockup1", "mockup2"], lambda x, y: print(f"Selected mockups: {x}, Image: {y}"), lambda: print("Go back"))
    root.mainloop()
