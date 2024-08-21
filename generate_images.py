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

def generate_striped_images(num_colors, image_size):
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