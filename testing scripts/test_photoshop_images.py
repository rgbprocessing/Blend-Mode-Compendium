# -*- coding: utf-8 -*-
# test_photoshop_images.py
# This script processes images stored in the 'photoshop images' folder which were
# created in photoshop using different blend modes. The script compares pairs of 
# images using the Sum of Absolute Error (SAE) to determine cases which are 
# imperceptible for our test images to distinguish.
#
# Author: Dani
# Created: 2022-01-22
# Last Modified: 2024-08-21
#
# Part of the Blend Mode Compendium Project
# Requires: os, matplotlib
# 
# Usage: Current configuration loops over 'photoshop images' directory for images
# beginning with 'test' and ending with '.png'. Run the script from the testing scripts
# directory to execute the test.

import os
import matplotlib.pyplot as plt
from functions.calculations import calculate_absolute_error

def compare_images(image_files, threshold=0.1):
    """
    Compares all images in the list and prints file names and similarity scores for pairs below the threshold.

    Parameters:
    - image_files (list): List of image file paths.
    - threshold (float): Similarity threshold for flagging similar images. Lower MSE indicates higher similarity.
    """
    # Load all images
    images = [plt.imread(file) for file in image_files]
    
    # Compare each image with every other image
    num_images = len(images)
    for i in range(num_images):
        for j in range(i + 1, num_images):
            sae = calculate_absolute_error(images[i], images[j])
            if sae < threshold:
                similarity_score = 1 - sae  # Higher score indicates more similarity
                print(f"Images '{image_files[i]}' and '{image_files[j]}' are {similarity_score:.2f} similar (SAE: {sae:.5f})")

# Test images
image_dir = os.path.join(os.path.dirname(__file__), '..', 'photoshop images')  # Get the test images directory
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.startswith('test') and f.endswith('.png')]

compare_images(image_files)

#Results: Color & Hue | Dissolve & Normal are exactly the same for the 12 stripe test image
