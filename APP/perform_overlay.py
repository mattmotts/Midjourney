from PIL import Image, ImageTk, ImageOps
import pandas as pd
import os
import tkinter as tk

class PerformOverlayApp:
    def __init__(self, root, selected_mockups, image_path, csv_file_path, return_to_overlay_callback, return_to_mockup_callback):
        self.root = root
        self.save_directory = "/Users/matt/Pictures/Midjourney/Imagine/Downloads"
        self.csv_file_path = csv_file_path
        self.mockups_df = pd.read_csv(self.csv_file_path)  # Load the uploaded CSV file
        self.selected_mockups = selected_mockups
        self.image_path = image_path
        self.return_to_overlay_callback = return_to_overlay_callback
        self.return_to_mockup_callback = return_to_mockup_callback

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
            # Normalize the mockup path and match based on the filename (case-insensitive)
            mockup_basename = os.path.basename(mockup).lower()

            try:
                # Match based on the lowercase basename
                mockup_info = self.mockups_df[self.mockups_df['image_id'].str.lower() == mockup_basename].iloc[0]
            except IndexError:
                print(f"Error: {mockup} not found in the CSV file.")
                continue

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

        # Save button to save the overlay image
        tk.Button(self.root, text="Save", command=self.save_overlay).pack(side=tk.LEFT, padx=10, pady=10)

        # Go Back button to return to the upload overlay stage
        tk.Button(self.root, text="Go Back", command=lambda: self.return_to_home_callback(self.selected_mockups)).pack(side=tk.RIGHT, padx=10, pady=10)

    def save_overlay(self):
        for mockup in self.selected_mockups:
            # Normalize the mockup path and match based on the filename (case-insensitive)
            mockup_basename = os.path.basename(mockup).lower()

            try:
                # Match based on the lowercase basename
                mockup_info = self.mockups_df[self.mockups_df['image_id'].str.lower() == mockup_basename].iloc[0]
            except IndexError:
                print(f"Error: {mockup_basename} not found in the CSV file.")
                continue

            mockup_path = mockup_info['image_path']
            top, left, height, width = mockup_info['top'], mockup_info['left'], mockup_info['height'], mockup_info['width']

            mockup_img = Image.open(mockup_path)
            overlay_img = Image.open(self.image_path)
            overlay_img = overlay_img.resize((int(width), int(height)))

            mockup_img.paste(overlay_img, (int(left), int(top)))

            overlay_image_name = os.path.basename(self.image_path)
            prefix = overlay_image_name.split('_')[0]
            new_filename = f"{prefix}_{mockup_basename}"
            save_path = os.path.join(self.save_directory, new_filename)
            mockup_img.save(save_path)
            print(f"Image saved as {new_filename} in {self.save_directory}")

        tk.messagebox.showinfo("Done", "Overlay process completed!")

        # After saving, go back to the mockup selection stage
        self.return_to_mockup_callback(self.csv_file_path)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PerformOverlayApp(root, ["mockup1", "mockup2"], "path/to/image.png", "path/to/csv.csv", lambda: print("Return to overlay"), lambda: print("Return to mockup selection"))
    root.mainloop()
