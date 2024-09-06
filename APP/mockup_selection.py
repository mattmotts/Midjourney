import tkinter as tk
from tkinter import filedialog, messagebox

class MockupSelectionApp:
    def __init__(self, root, next_step_callback, go_back_callback):
        self.root = root
        self.next_step_callback = next_step_callback
        self.go_back_callback = go_back_callback
        self.selected_mockups = []

        self.setup_ui()

    def setup_ui(self):
        self.clear_window()

        # Button to upload mockups (multiple selections)
        upload_button = tk.Button(self.root, text="Select Mockups", command=self.upload_mockups)
        upload_button.pack(pady=20)

        # Next and Go Back buttons
        next_button = tk.Button(self.root, text="Next", command=self.on_next)
        next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        back_button = tk.Button(self.root, text="Go Back", command=self.on_back)
        back_button.pack(side=tk.LEFT, padx=10, pady=10)

    def upload_mockups(self):
        self.selected_mockups = filedialog.askopenfilenames(
            initialdir="/users/matt/pictures/midjourney/imagine/mockups", 
            title="Select Mockup Images",
            filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"), ("All files", "*.*"))
        )
        if self.selected_mockups:
            print(f"Selected mockups: {self.selected_mockups}")
        else:
            messagebox.showerror("Error", "No mockups selected")

    def on_next(self):
        if not self.selected_mockups:
            messagebox.showerror("Error", "No mockups selected")
            return
        self.next_step_callback(self.selected_mockups)

    def on_back(self):
        self.go_back_callback()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MockupSelectionApp(root, lambda x: print(f"Next with: {x}"), lambda: print("Going back"))
    root.mainloop()
