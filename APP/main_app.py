import tkinter as tk
from mockup_selection import MockupSelectionApp
from upload_overlay import UploadOverlayApp
from perform_overlay import PerformOverlayApp
import pandas as pd

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mockup Overlay Application")
        
        self.mockup_data_path = '/Users/matt/Documents/Coding/Midjourney/APP/mockup_data.csv'
        self.mockups_df = pd.read_csv(self.mockup_data_path)
        
        self.run_mockup_selection()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run_mockup_selection(self):
        self.clear_window()
        MockupSelectionApp(self.root, self.run_upload_overlay)

    def run_upload_overlay(self, selected_mockups):
        self.clear_window()
        UploadOverlayApp(self.root, selected_mockups, self.run_perform_overlay)

    def run_perform_overlay(self, selected_mockups, image_path):
        self.clear_window()
        PerformOverlayApp(self.root, selected_mockups, image_path, self.run_mockup_selection)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
