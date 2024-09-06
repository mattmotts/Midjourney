import tkinter as tk
from tkinter import filedialog, messagebox

class CSVLoadApp:
    def __init__(self, root, next_step_callback):
        self.root = root
        self.root.title("CSV Loader")
        self.next_step_callback = next_step_callback
        self.csv_file_path = None

        self.setup_ui()

    def setup_ui(self):
        self.clear_window()

        tk.Label(self.root, text="Upload your CSV file").pack(pady=10)
        tk.Button(self.root, text="Select Data", command=self.upload_csv).pack(pady=10)

        # Button to move to the next step
        self.next_button = tk.Button(self.root, text="Next", command=self.on_next, state=tk.DISABLED)
        self.next_button.pack(pady=10)

    def upload_csv(self):
        # Set initial directory to open
        self.csv_file_path = filedialog.askopenfilename(
            initialdir="/users/matt/documents/data",
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if self.csv_file_path:
            messagebox.showinfo("CSV Loaded", f"CSV file loaded: {self.csv_file_path}")
            self.next_button.config(state=tk.NORMAL)  # Enable next button

    def on_next(self):
        if not self.csv_file_path:
            messagebox.showerror("Error", "No CSV file uploaded.")
            return

        # Proceed to the next step
        self.next_step_callback(self.csv_file_path)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVLoadApp(root, lambda x: print(f"CSV Loaded: {x}"))
    root.mainloop()
