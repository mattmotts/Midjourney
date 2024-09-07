import tkinter as tk
from csv_loader import CSVLoadApp
from mockup_selection import MockupSelectionApp
from upload_overlay import UploadOverlayApp
from perform_overlay import PerformOverlayApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mockup Overlay Application")
        self.csv_file_path = None
        self.mockup_directory = None

        self.run_csv_load()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Step 1: CSV Load
    def run_csv_load(self):
        self.clear_window()
        self.root.title("CSV Loader")
        CSVLoadApp(self.root, self.run_mockup_load)

    # Step 2: Mockup Load
    def run_mockup_load(self, csv_file_path):
        self.csv_file_path = csv_file_path  # Store the CSV file path
        self.clear_window()
        self.root.title("Mockup Selection")
        MockupSelectionApp(self.root, self.run_upload_overlay, self.run_csv_load)

    # Step 3: Upload Overlay
    def run_upload_overlay(self, selected_mockups):
        if not selected_mockups:
            tk.messagebox.showerror("Error", "No mockup selected")
            return
        self.clear_window()
        self.root.title("Upload Overlay")
        UploadOverlayApp(self.root, selected_mockups, self.run_perform_overlay, self.run_mockup_load)

    # Step 4: Perform Overlay
    def run_perform_overlay(self, selected_mockups, image_path):
        if not image_path:
            tk.messagebox.showerror("Error", "No image selected")
            return
        self.clear_window()
        self.root.title("Overlay Selection")
        # Pass the CSV file path to ensure the correct data is used
        PerformOverlayApp(self.root, selected_mockups, image_path, self.csv_file_path, self.run_mockup_load)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
