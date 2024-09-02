import tkinter as tk
from mockup_selection import MockupSelectionApp
from upload_overlay import UploadOverlayApp
from perform_overlay import PerformOverlayApp
import pandas as pd

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mockup Overlay Application")
        
        # Use the absolute path to the mockup_data.csv file
        self.mockup_data_path = '/Users/matt/Documents/Coding/Midjourney/APP/mockup_data.csv'
        
        # Load the mockup data
        self.mockups_df = pd.read_csv(self.mockup_data_path)
        
        # Start with the first step
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
        PerformOverlayApp(selected_mockups, image_path)
        tk.messagebox.showinfo("Done", "Overlay process completed!")
        # Optionally, you can close the application after this step:
        # self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
