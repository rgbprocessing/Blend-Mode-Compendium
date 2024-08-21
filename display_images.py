# -*- coding: utf-8 -*-
# display_images.py
# This file contains display functions for resulting images
#
# Author: Dani
# Created: 2022-01-22
# Last Modified: 2024-08-21
#
# Part of the Blend Mode Compendium Project
# Requires: matplotlib
# 
# Usage: Import this module and call the functions with appropriate parameters.
# Example:
# from display_images import plot_2_images
# plot_2_images(image1, image2, caption_A="Custom Caption 1", caption_B="Custom Caption 2")

import matplotlib.pyplot as plt

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
    plt.imshow(image_A)
    plt.axis('off')  # Hide the axes
    plt.title(caption_A)

    # Display second image
    plt.subplot(1, 2, 2)
    plt.imshow(image_B)
    plt.axis('off')  # Hide the axes
    plt.title(caption_B)

    plt.show()
