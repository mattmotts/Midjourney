import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd

class MockupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mockup Overlay Application")

        # Listbox for mockup selection
        self.mockup_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.mockup_listbox.pack()

        # Button to upload an image
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        # Button to overlay the image
        self.overlay_button = tk.Button(root, text="Overlay Image", command=self.overlay_image)
        self.overlay_button.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Load mockups from CSV
        self.mockups_df = pd.read_csv("mockups.csv")
        for mockup in self.mockups_df['image_id'].tolist():
            self.mockup_listbox.insert(tk.END, mockup)

        self.selected_image_path = None

    def upload_image(self):
        self.selected_image_path = filedialog.askopenfilename()
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
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            mockup_img.save(save_path)
            messagebox.showinfo("Success", f"Image saved as {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MockupApp(root)
    root.mainloop()
