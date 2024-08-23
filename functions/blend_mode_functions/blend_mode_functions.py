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
from skimage import color

def screen(image1, image2):
    """
    Applies the Screen blend mode to two images.

    The Screen blend mode lightens the image by blending the lighter areas
    of both images. It is achieved by inverting the colors of both images,
    multiplying them, and then inverting the result.

    Parameters:
    - image1 (numpy.ndarray): First image array with values in [0, 1].
    - image2 (numpy.ndarray): Second image array with values in [0, 1].

    Returns:
    - blended_image (numpy.ndarray): The result of applying the Screen blend mode.
    """
    
    return 1 - (1 - image1) * (1 - image2)

def blend_images(image1, image2, alpha=1, blend_mode='normal'):
    """
    Blends two images using the specified alpha value.

    Parameters:
    - image1: First image as a NumPy array.
    - image2: Second image as a NumPy array.
    - alpha: Blending factor. 0.0 gives the first image, 1.0 gives the second image.

    Returns:
    - Blended image as a NumPy array.
    """
    skipone = False #sets flag for cases where we need to skip without erroring out
    
    # Ensure both images have the same dimensions
    if image1.shape != image2.shape:
        raise ValueError("Images must have the same dimensions for blending.")

    # Perform the blending based on the specified blend mode
    if blend_mode == 'normal':
        blended_image = image2
    
    elif blend_mode == 'multiply':
        blended_image = image1 * image2
    
    elif blend_mode == 'screen':
        blended_image = screen(image1, image2)
        
        
    elif blend_mode == 'overlay':
        image1=image1[:,:,0:3]
        image2=image2[:,:,0:3]
        blended_image = np.where(image1 < 0.5,
                                 2 * image2 * image1,
                                 1 - 2 * (1 - image2) * (1 - image1))
            
    elif blend_mode == 'darken':
        blended_image = np.minimum(image1, image2)

    elif blend_mode == 'linear burn':
        blended_image = np.maximum(0, image1 + image2 - 1)
    
    elif blend_mode == 'difference':
        blended_image = np.abs(image1[:,:,0:3] - image2[:,:,0:3])

    elif blend_mode == 'lighten':
        blended_image = np.maximum(image1, image2)

    elif blend_mode == 'linear dodge':
        blended_image = np.clip(image1 + image2, 0, 1)
        
    else:
        print('not implemented yet: ', blend_mode)
        skipone = True
        #raise ValueError(f"Not implemented yet: {blend_mode}")

    if not skipone:
        # Alpha blending
        blended_image = (1 - alpha) * image1 + alpha * blended_image
        
        # Clip values to be in the valid range [0, 255] for image data
        blended_image = np.clip(blended_image, 0, 1)
        
        return blended_image
    else:
        skipone = False