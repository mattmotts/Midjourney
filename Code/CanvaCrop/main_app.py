# main_app.py
import tkinter as tk
from mockup_selection import MockupSelectionApp
from upload_overlay import UploadOverlayApp
from perform_overlay import PerformOverlayApp

class MainApp:
    def __init__(self, root):
        self.root = root  # This is the only Tk instance
        self.root.title("Mockup Overlay Application")
        self.run_mockup_selection()

    def run_mockup_selection(self):
        self.new_window = tk.Toplevel(self.root)  # Use Toplevel instead of Tk
        MockupSelectionApp(self.new_window, self.run_upload_overlay)

    def run_upload_overlay(self, selected_mockups):
        self.new_window = tk.Toplevel(self.root)  # Use Toplevel instead of Tk
        UploadOverlayApp(self.new_window, selected_mockups, self.run_perform_overlay)

    def run_perform_overlay(self, selected_mockups, image_path):
        PerformOverlayApp(selected_mockups, image_path)
        tk.messagebox.showinfo("Done", "Overlay process completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
