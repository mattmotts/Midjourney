from PIL import Image, ImageTk, ImageOps
import pandas as pd
import os
import tkinter as tk

class PerformOverlayApp:
    def __init__(self, root, selected_mockups, image_path, return_to_home_callback):
        self.root = root
        self.save_directory = "/Users/matt/Pictures/Midjourney/Imagine/Downloads"
        self.mockup_data_path = '/Users/matt/Documents/Coding/Midjourney/APP/mockup_data.csv'
        self.mockups_df = pd.read_csv(self.mockup_data_path)
        self.selected_mockups = selected_mockups
        self.image_path = image_path
        self.return_to_home_callback = return_to_home_callback

        self.preview_overlay()

    def preview_overlay(self):
        self.clear_window()

        # Add canvas for scrolling
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        max_width = 300
        max_height = 300

        for mockup in self.selected_mockups:
            mockup_info = self.mockups_df[self.mockups_df['image_id'] == mockup].iloc[0]
            mockup_path = mockup_info['image_path']
            top, left, height, width = mockup_info['top'], mockup_info['left'], mockup_info['height'], mockup_info['width']

            try:
                mockup_img = Image.open(mockup_path)
            except Exception as e:
                print(f"Failed to load image: {mockup_path} with error: {e}")
                continue

            overlay_img = Image.open(self.image_path)
            overlay_img = overlay_img.resize((int(width), int(height)))

            mockup_img.paste(overlay_img, (int(left), int(top)))

            # Resize the image to fit within the specified max_width and max_height
            mockup_img.thumbnail((max_width, max_height))

            try:
                img_preview = ImageTk.PhotoImage(mockup_img)
            except Exception as e:
                print(f"Failed to create ImageTk.PhotoImage: {e}")
                continue

            preview_label = tk.Label(self.frame, image=img_preview)
            preview_label.image = img_preview
            preview_label.pack(pady=10, padx=10)

        tk.Button(self.root, text="Save", command=self.save_overlay).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.root, text="Cancel", command=self.return_to_home_callback).pack(side=tk.RIGHT, padx=10, pady=10)

    def save_overlay(self):
        for mockup in self.selected_mockups:
            mockup_info = self.mockups_df[self.mockups_df['image_id'] == mockup].iloc[0]
            mockup_path = mockup_info['image_path']
            top, left, height, width = mockup_info['top'], mockup_info['left'], mockup_info['height'], mockup_info['width']

            mockup_img = Image.open(mockup_path)
            overlay_img = Image.open(self.image_path)
            overlay_img = overlay_img.resize((int(width), int(height)))

            mockup_img.paste(overlay_img, (int(left), int(top)))

            overlay_image_name = os.path.basename(self.image_path)
            prefix = overlay_image_name.split('_')[0]
            new_filename = f"{prefix}_{mockup}.png"
            save_path = os.path.join(self.save_directory, new_filename)
            mockup_img.save(save_path)
            print(f"Image saved as {new_filename} in {self.save_directory}")

        tk.messagebox.showinfo("Done", "Overlay process completed!")
        self.return_to_home_callback()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PerformOverlayApp(root, ["mockup1", "mockup2"], "path/to/image.png", lambda: print("Return to home"))
    root.mainloop()
