import numpy as np
from PIL import Image
import glob
import os
import shutil

# Get the current directory
current_directory = os.getcwd()

# Search for image files in the current directory
image_files = glob.glob(os.path.join(current_directory, '*.png')) + \
              glob.glob(os.path.join(current_directory, '*.jpg')) + \
              glob.glob(os.path.join(current_directory, '*.jpeg')) + \
              glob.glob(os.path.join(current_directory, '*.bmp')) + \
              glob.glob(os.path.join(current_directory, '*.gif'))

def resize_with_aspect_ratio(image, target_size):
    width, height = image.size
    target_width, target_height = target_size

    if width == height:
        resized_image = image.resize((300, 300))
        return resized_image
    
    # Calculate aspect ratios
    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height
    
    if aspect_ratio > target_aspect_ratio:
        # Image is wider than target aspect ratio
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    else:
        # Image is taller than target aspect ratio
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    
    return resized_image

def convert_image_alpha_bg_to_pcx_with_white_background():

    if os.path.exists(current_directory + "\\out"):
        os.removedirs(current_directory + "\\out")
    os.makedirs(current_directory + "\\out")
        
    for image_path in image_files:
        # Open the image
        img = Image.open(image_path)

        img = resize_with_aspect_ratio(img, target_size)

        # debug image mode
        print(img.mode)

        # Check for transparency for different modes. Here in order [P, RGBA, ...]
        transparency_index = img.info.get("transparency", None)
        alpha_channel = img.split()[-1]

        print(alpha_channel)

        # Check if there are any fully transparent pixels if RGBA
        has_zero_alpha = any(alpha == 0 for alpha in alpha_channel.getdata())

        if transparency_index != None or img.mode == "RGBA" and has_zero_alpha:
            # Convert to numpy array
            img_array = np.array(img)
            # Binarize the image using a threshold
            # threshold = 0
            img = np.where(img_array > 0, 255, 0).astype(np.uint8)
            # Invert the colors
            img = 255 - img
            # Convert back to PIL Image
            img = Image.fromarray(img)

        # Convert to black and white (1-bit)
        img = img.convert("1", dither=0)

        # Save the image as PCX
        img.save(image_path+'.pcx', 'PCX')

        # Move each image file to the destination directory
        for image_path in image_files:
            shutil.move(image_path+'.pcx', current_directory+"\\out")


# Example usage:
target_size = (200, 125)
convert_image_alpha_bg_to_pcx_with_white_background()

