from PIL import Image
import pandas as pd
import os

class PerformOverlayApp:
    def __init__(self, selected_mockups, image_path):
        self.save_directory = "/Users/matt/Pictures/Midjourney/Imagine/Downloads"
        
        # Use the absolute path for the mockup_data.csv
        self.mockup_data_path = '/Users/matt/Documents/Coding/Midjourney/APP/mockup_data.csv'
        
        # Load the mockup data
        self.mockups_df = pd.read_csv(self.mockup_data_path)
        
        self.selected_mockups = selected_mockups
        self.image_path = image_path
        self.perform_overlay()

    def perform_overlay(self):
        for mockup in self.selected_mockups:
            # Get the relevant mockup information
            mockup_info = self.mockups_df[self.mockups_df['image_id'] == mockup].iloc[0]
            mockup_path = mockup_info['image_path']
            top, left, height, width = mockup_info['top'], mockup_info['left'], mockup_info['height'], mockup_info['width']

            # Open the mockup image and the overlay image
            mockup_img = Image.open(mockup_path)
            overlay_img = Image.open(self.image_path)

            # Resize the overlay image to fit the mockup
            overlay_img = overlay_img.resize((int(width), int(height)))

            # Paste the overlay image onto the mockup image at the specified position
            mockup_img.paste(overlay_img, (int(left), int(top)))

            # Prepare the new filename and save the overlaid image
            overlay_image_name = os.path.basename(self.image_path)
            prefix = overlay_image_name.split('_')[0]
            new_filename = f"{prefix}_{mockup}.png"
            save_path = os.path.join(self.save_directory, new_filename)
            mockup_img.save(save_path)

            print(f"Image saved as {new_filename} in {self.save_directory}")

if __name__ == "__main__":
    PerformOverlayApp(["mockup1", "mockup2"], "path/to/image.png")
