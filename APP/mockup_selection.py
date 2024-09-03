import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

class MockupSelectionApp:
    def __init__(self, root, next_step_callback):
        self.root = root
        self.root.title("Mockup Selection")
        self.root.geometry("500x700")
        self.next_step_callback = next_step_callback

        frame_mockup_list = ttk.Frame(root, padding="10")
        frame_mockup_list.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_mockup_list, text="Select Mockup(s):").pack(anchor=tk.W)

        self.mockup_listbox = tk.Listbox(frame_mockup_list, selectmode=tk.MULTIPLE, height=10)
        self.mockup_listbox.pack(fill=tk.BOTH, expand=True)
        self.mockup_listbox.bind("<<ListboxSelect>>", self.show_selected_mockup)

        frame_preview = ttk.Frame(root, padding="10")
        frame_preview.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_preview, text="Image Preview:").pack(anchor=tk.W)
        self.image_label = ttk.Label(frame_preview)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.mockup_data_path = '/Users/matt/Documents/Coding/Midjourney/APP/mockup_data.csv'
        self.mockups_df = pd.read_csv(self.mockup_data_path)
        self.mockup_paths = {}

        for mockup in self.mockups_df['image_id'].tolist():
            self.mockup_listbox.insert(tk.END, mockup)
            mockup_info = self.mockups_df[self.mockups_df['image_id'] == mockup].iloc[0]
            self.mockup_paths[mockup] = mockup_info['image_path']

        ttk.Button(root, text="Next", command=self.save_selection_and_proceed).pack(pady=10)

    def show_selected_mockup(self, event):
        selected_mockup = self.mockup_listbox.get(tk.ACTIVE)
        if selected_mockup in self.mockup_paths:
            img = Image.open(self.mockup_paths[selected_mockup])
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def get_selected_mockups(self):
        return [self.mockup_listbox.get(i) for i in self.mockup_listbox.curselection()]

    def save_selection_and_proceed(self):
        selected_mockups = self.get_selected_mockups()
        if not selected_mockups:
            tk.messagebox.showerror("Error", "No mockup selected")
            return
        self.next_step_callback(selected_mockups)

if __name__ == "__main__":
    root = tk.Tk()
    app = MockupSelectionApp(root, lambda x: print(f"Selected mockups: {x}"))
    root.mainloop()
