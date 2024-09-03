import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import pandas as pd

class MockupSelectionApp:
    def __init__(self, root, next_step_callback):
        self.root = root
        self.root.title("Mockup Selection")
        self.root.geometry("700x800")
        self.next_step_callback = next_step_callback

        self.selected_mockups = set()  # Store selected mockups

        frame_mockup_list = ttk.Frame(root, padding="10")
        frame_mockup_list.pack(fill=tk.BOTH, expand=True)

        self.mockup_buttons = {}  # To keep track of buttons and their state
        self.original_images = {}  # To store original images

        self.mockup_data_path = '/Users/matt/Documents/Coding/Midjourney/APP/mockup_data.csv'
        self.mockups_df = pd.read_csv(self.mockup_data_path)
        self.display_mockups(frame_mockup_list)

        ttk.Button(root, text="Next", command=self.save_selection_and_proceed).pack(pady=10)

    def display_mockups(self, frame):
        row, col = 0, 0
        for mockup in self.mockups_df['image_id'].tolist():
            mockup_info = self.mockups_df[self.mockups_df['image_id'] == mockup].iloc[0]
            mockup_path = mockup_info['image_path']
            
            img = Image.open(mockup_path)
            img.thumbnail((150, 150))  # Adjust thumbnail size as needed
            img = ImageTk.PhotoImage(img)

            button = tk.Button(frame, image=img, command=lambda m=mockup: self.toggle_selection(m))
            button.image = img  # Keep a reference to avoid garbage collection
            button.grid(row=row, column=col, padx=10, pady=10)

            label = tk.Label(frame, text=mockup)
            label.grid(row=row + 1, column=col)

            self.mockup_buttons[mockup] = button
            self.original_images[mockup] = img  # Store original image

            col += 1
            if col >= 3:  # Adjust this value to determine the number of columns
                col = 0
                row += 2

    def toggle_selection(self, mockup):
        if mockup in self.selected_mockups:
            self.selected_mockups.remove(mockup)
            self.update_button_state(mockup, selected=False)
        else:
            self.selected_mockups.add(mockup)
            self.update_button_state(mockup, selected=True)

    def update_button_state(self, mockup, selected):
        button = self.mockup_buttons.get(mockup)
        if button:
            if selected:
                # Load the original image
                original_img = Image.open(self.mockups_df[self.mockups_df['image_id'] == mockup]['image_path'].iloc[0])
                
                # Create a shadow effect by expanding the image with a black border
                shadow = ImageOps.expand(original_img, border=25, fill='#000000')  # Black shadow
                
                # Add a light blue border on top of the shadow
                bordered_img = ImageOps.expand(shadow, border=15, fill='#ADD8E6')  # Light blue border over shadow
                
                # Resize and convert to PhotoImage for Tkinter
                bordered_img.thumbnail((150, 150))  # Adjust thumbnail size as needed
                bordered_img = ImageTk.PhotoImage(bordered_img)
                
                # Update the button image
                button.config(image=bordered_img)
                button.image = bordered_img
            else:
                # Revert to the original image
                button.config(image=self.original_images[mockup])
                button.image = self.original_images[mockup]



    def save_selection_and_proceed(self):
        if not self.selected_mockups:
            tk.messagebox.showerror("Error", "No mockup selected")
            return
        print(f"Proceeding with: {self.selected_mockups}")
        self.next_step_callback(self.selected_mockups)

if __name__ == "__main__":
    root = tk.Tk()
    app = MockupSelectionApp(root, lambda x: print(f"Selected mockups: {x}"))
    root.mainloop()
