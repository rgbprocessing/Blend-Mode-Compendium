# -*- coding: utf-8 -*-
# test_blend_modes.py
# This script processes images stored in the 'photoshop images' folder which were
# created in photoshop using different blend modes. The script compares the photoshop
# generated image with the blend mode function code and finds any discrepancies.
#
# Author: Dani
# Created: 2022-01-22
# Last Modified: 2024-08-23
#
# Part of the Blend Mode Compendium Project
# Requires: numpy, os, matplotlib
# 
# Usage: Current configuration loops over 'photoshop images' directory for images
# in the form test_blend_mode.png. Run the script from the testing scripts
# directory to execute the test.

import os
import numpy as np
import matplotlib.pyplot as plt
from functions.blend_mode_functions import blend_images
from functions.image_functions import generate_striped_images, load_and_crop_to_square
from functions.calculations import calculate_absolute_error
import matplotlib.image as mpimg

def process_images(image_folder, image1, image2):
    image_dir = os.path.join(os.path.dirname(__file__), '..', image_folder)  # Get the test images directory

    for filename in os.listdir(image_dir):
        threshold = 0.0
        if filename.endswith(".png"):
            # Extract the blend mode from the filename
            blend_mode = filename[len("test_"):-len(".png")]
            
            # Replace underscores with spaces in the blend mode
            blend_mode = blend_mode.replace('_', ' ')
            
            # Load the actual image
            actual_image_path = os.path.join(image_dir, filename)
            actual_image = (np.round(255*plt.imread(actual_image_path))).astype(int)
            
            try:
                # Create blended image using same blend_mode
                generated_image = (np.round(blend_images(image1, image2, blend_mode=blend_mode)*255)).astype(int)
                
                np.clip(generated_image, 0, 255)
                
                #calculate SAE
                sae = calculate_absolute_error(actual_image[:,:,0:3], generated_image[:,:,0:3])
                if sae > threshold:
                    print(f"Images '{blend_mode}' have SAE: {sae:.5f}")
            except:
                print('not implemented', blend_mode)
            
image_folder = "photoshop images"  # Folder where your images are stored
test_dir = os.path.join(os.path.dirname(__file__), '..', 'test images')
image1 = mpimg.imread(os.path.join(test_dir,'image_horizontal_stripes.png'))
image2 = mpimg.imread(os.path.join(test_dir,'image_vertical_stripes.png'))
process_images(image_folder, image1, image2)
image_folder = "photoshop images 2"  # Folder where your images are stored
image1 = mpimg.imread(os.path.join(test_dir,'imageAcropped.png'))
image2 = mpimg.imread(os.path.join(test_dir,'imageBcropped.png'))
process_images(image_folder, image1, image2)