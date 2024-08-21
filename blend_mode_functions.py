# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:39:33 2024

@author: dmont
"""

import numpy as np

def blend_images(image1, image2, alpha):
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

    # Perform the blending
    blended_image = (1 - alpha) * image1 + alpha * image2

    # Clip values to be in the valid range [0, 255] for image data
    blended_image = np.clip(blended_image, 0, 255).astype(np.uint8)

    return blended_image