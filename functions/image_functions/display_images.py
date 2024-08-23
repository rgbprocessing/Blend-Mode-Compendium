# -*- coding: utf-8 -*-
# display_images.py
# This file contains display functions for resulting images
#
# Author: Dani
# Created: 2022-01-22
# Last Modified: 2024-08-21
#
# Part of the Blend Mode Compendium Project
# Requires: matplotlib, numpy, PIL
# 
# Usage: Import this module and call the functions with appropriate parameters.
# Example:
# from display_images import plot_2_images
# plot_2_images(image1, image2, caption_A="Custom Caption 1", caption_B="Custom Caption 2")

import matplotlib.pyplot as plt
import numpy as np
from ..blend_mode_functions import blend_images
#..folder1.functionA import some_function_from_A

def plot_2_images(image_A, image_B, caption_A="Image A", caption_B="Image B"):
    """
    Plots two images side by side with custom captions.

    Parameters:
    - image_A: First image to be displayed.
    - image_B: Second image to be displayed.
    - caption_A: Caption for the first image (default: "Image A").
    - caption_B: Caption for the second image (default: "Image B").
    """
    plt.figure(figsize=(12, 6))

    # Display first image
    plt.subplot(1, 2, 1)
    plt.imshow((np.round(image_A*255)).astype(int))
    plt.axis('off')  # Hide the axes
    plt.title(caption_A)

    # Display second image
    plt.subplot(1, 2, 2)
    plt.imshow((np.round(image_B*255)).astype(int))
    plt.axis('off')  # Hide the axes
    plt.title(caption_B)

    plt.show()
    return
    
def create_alpha_transition_graphic(image1, image2, num_steps=5, blend_mode='normal'):
    """
    Creates a graphic with a sequence of images transitioning between two input images with varying alpha values.
    
    Parameters:
    - image1: The first input PIL image.
    - image2: The second input PIL image.
    - num_steps: Number of transition steps (default is 5).
    
    Returns:
    - A Matplotlib figure displaying the transition steps.
    """
    # Calculate the alpha values
    alphas = np.linspace(0, 1, num_steps)
    
    # Create a figure to display the images
    fig, axes = plt.subplots(1, num_steps, figsize=(num_steps * 4, 5))
    
    # For each alpha value, blend the images and display them in the figure
    for i, alpha in enumerate(alphas):
        blended_image = blend_images(image1, image2, alpha, blend_mode)
        axes[i].imshow((np.round(blended_image*255)).astype(int))
        axes[i].axis('off')
        axes[i].set_title(f"Alpha: {alpha:.2f}", fontsize=12)
    
    plt.tight_layout()
    plt.show()
    return
