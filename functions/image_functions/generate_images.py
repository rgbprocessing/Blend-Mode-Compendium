# -*- coding: utf-8 -*-
# generate_images.py
# This file contains functions to generate test images
#
# Author: Dani
# Created: 2022-01-22
# Last Modified: 2024-08-21
#
# Part of the Blend Mode Compendium Project
# Requires: colorsys, numpy
# 
# Usage: Import this module and call the functions with appropriate parameters.
# Example:
# from generate_images import generate_rainbow_colors
# colors = generate_rainbow_colors(numColors)

import colorsys
import numpy as np
import matplotlib.pyplot as plt

def generate_rainbow_colors(num_colors):
    """
    Generates a list of colors in the rainbow using HSL color space.
    
    Parameters:
    - num_colors: Number of colors to generate.
    
    Returns:
    - A list of RGB tuples representing the rainbow colors.
    """
    colors = []
    for i in range(num_colors):
        hue = i / num_colors  # Vary hue from 0 to 1
        rgb = colorsys.hls_to_rgb(hue, 0.5, 1.0)  # Convert HSL to RGB (lightness = 0.5, saturation = 1.0)
        colors.append(rgb)
    return colors

def generate_striped_images(num_colors=12, image_size=12):
    """
    Generates two images with horizontal and vertical rainbow stripes.
    
    Parameters:
    - num_colors: Number of stripes/colors in the rainbow.
    - image_size: Size of the square image (height and width).
    
    Returns:
    - image_horizontal_stripes: Image with horizontal stripes.
    - image_vertical_stripes: Image with vertical stripes.
    """
    # Generate the rainbow colors
    rainbow_colors = generate_rainbow_colors(num_colors)
    
    # Create empty images for horizontal and vertical stripes
    image_horizontal_stripes = np.zeros((image_size, image_size, 3))
    image_vertical_stripes = np.zeros((image_size, image_size, 3))
    
    # Calculate stripe dimensions
    stripe_height = image_size // num_colors
    stripe_width = image_size // num_colors
    
    # Fill the image with horizontal and vertical stripes
    for i, color in enumerate(rainbow_colors):
        image_horizontal_stripes[i * stripe_height:(i + 1) * stripe_height, :] = color
        image_vertical_stripes[:, i * stripe_width:(i + 1) * stripe_width] = color
       
    return image_horizontal_stripes, image_vertical_stripes

def load_and_crop_to_square(image_path_A, image_path_B):
    """
    Loads two images from file paths and crops them to the largest central square 
    that can be uniformly applied to both images.
    
    Parameters:
    - image_path_A (str): File path to the first image.
    - image_path_B (str): File path to the second image.
    
    Returns:
    - cropped_A (numpy.ndarray): The largest central square cropped from the first image.
    - cropped_B (numpy.ndarray): The largest central square cropped from the second image.
    """
    # Load the images using matplotlib
    image_A = plt.imread(image_path_A)
    image_B = plt.imread(image_path_B)

    # Get the dimensions of the images
    h_A, w_A = image_A.shape[:2]
    h_B, w_B = image_B.shape[:2]

    # Determine the size of the largest central square that can be cropped from each image
    size_A = min(h_A, w_A)
    size_B = min(h_B, w_B)

    # Find the minimum size between the two to ensure both cropped images are the same size
    final_size = min(size_A, size_B)

    # Calculate the coordinates for cropping image_A
    left_A = (w_A - final_size) // 2
    top_A = (h_A - final_size) // 2
    cropped_A = image_A[top_A:top_A + final_size, left_A:left_A + final_size]

    # Calculate the coordinates for cropping image_B
    left_B = (w_B - final_size) // 2
    top_B = (h_B - final_size) // 2
    cropped_B = image_B[top_B:top_B + final_size, left_B:left_B + final_size]

    return cropped_A/255, cropped_B/255
