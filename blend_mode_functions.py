# -*- coding: utf-8 -*-
# blend_mode_functions.py
# This file contains functions to calculate different blend modes to combine images
#
# Author: Dani
# Created: 2022-01-22
# Last Modified: 2024-08-21
#
# Part of the Blend Mode Compendium Project
# Requires: numpy
# 
# Usage: Import this module and call the functions with appropriate parameters.
# Example:
# from blend_mode_functions import blend_images
# blended_image = blend_images(image1, image2, alpha, blend_mode)

import numpy as np

def blend_images(image1, image2, alpha, blend_mode='normal'):
    """
    Blends two images using the specified alpha value.

    Parameters:
    - image1: First image as a NumPy array.
    - image2: Second image as a NumPy array.
    - alpha: Blending factor. 0.0 gives the first image, 1.0 gives the second image.

    Returns:
    - Blended image as a NumPy array.
    """
    # Ensure both images have the same dimensions
    if image1.shape != image2.shape:
        raise ValueError("Images must have the same dimensions for blending.")

    # Perform the blending based on the specified blend mode
    if blend_mode == 'normal':
        blended_image = image2
    
    elif blend_mode == 'multiply':
        blended_image = image1 * image2
    
    elif blend_mode == 'screen':
        blended_image = 1 - (1 - image1) * (1 - image2)
    
    elif blend_mode == 'overlay':
        # Overlay blend mode applies different blending depending on the base color
        mask = image1 < 128
        blended_image = np.where(mask, 
                                 2 * image1 * image2, 
                                 1 - 2 * (1 - image1) * (1 - image2))
        
    elif blend_mode == 'darken':
        blended_image = np.minimum(image1, image2)

    elif blend_mode == 'color burn':
        blended_image = 1 - np.minimum(1, (1 - image2) / (image1 + 1e-10))

    elif blend_mode == 'linear burn':
        blended_image = np.maximum(0, image1 + image2 - 1)

    elif blend_mode == 'darker color':
        # Calculate the sum of the RGB channels for each image
        sum1 = np.sum(image1, axis=-1)
        sum2 = np.sum(image2, axis=-1)
        # Find the minimum sum between the two images
        min_sum = np.minimum(sum1, sum2)
        # Use np.where to select colors based on the minimum sum
        mask = (sum1 == min_sum)
        blended_image = np.where(mask[:, :, None], image1, image2)

    
    blended_image = (1 - alpha) * image1 + alpha * blended_image

    # Clip values to be in the valid range [0, 255] for image data
    blended_image = np.clip(blended_image, 0, 1)

    return blended_image