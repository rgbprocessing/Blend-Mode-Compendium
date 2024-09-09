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
epsilon = 1e-10

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

def calculate_color_brightness(image):
    #https://www.w3.org/TR/AERT/#color-contrast
    return 0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]

def rgb_to_hcl(image):
    """
    Convert an RGB image to HCL (Hue, Chroma, Luma)

    Parameters:
    image (numpy.ndarray): The RGB image with values in the range [0, 1].

    Returns:
    numpy.ndarray: The HCL image with values in the range [0, 1].
    """
    # Split the image into R, G, and B channels
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    # Calculate max and min values for each pixel
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    
    # Calculate chroma
    c = maxc - minc
    
    # Calculate hue (h)
    h = np.zeros_like(maxc)
    mask = c != 0
    h[mask & (maxc == r)] = (g[mask & (maxc == r)] - b[mask & (maxc == r)]) / c[mask & (maxc == r)]
    h[mask & (maxc == g)] = 2.0 + (b[mask & (maxc == g)] - r[mask & (maxc == g)]) / c[mask & (maxc == g)]
    h[mask & (maxc == b)] = 4.0 + (r[mask & (maxc == b)] - g[mask & (maxc == b)]) / c[mask & (maxc == b)]

    # Normalize hue to [0, 1]
    h = (h / 6.0) % 1.0
    
    # Calculate luma (l)
    l = calculate_color_brightness(image)
    
    # Stack H, S, and L channels into an HSL image
    hcl_image = np.stack([h, c, l], axis=-1)

    return hcl_image

def hcl_to_rgb(hcl_image):
    """
    Convert an HCL image (Hue, Chroma, Luma) to RGB.
    Hue is scaled to [0, 1].
    
    Parameters:
    hcl_image (numpy.ndarray): The HCL image with values in the range [0, 1].
    
    Returns:
    numpy.ndarray: The RGB image with values in the range [0, 1].
    """
    h, c, l = hcl_image[:, :, 0], hcl_image[:, :, 1], hcl_image[:, :, 2]
    
    # Hue scaled to [0, 6] to handle sectors
    h_prime = h * 6
    
    # Intermediate value X, depending on which sector of H' we're in
    x = c * (1 - np.abs(h_prime % 2 - 1))

    # Initialize RGB values
    r1 = np.zeros_like(h)
    g1 = np.zeros_like(h)
    b1 = np.zeros_like(h)

    # Assign RGB1 based on the sector of the hue
    mask = (0 <= h_prime) & (h_prime < 1)
    r1[mask], g1[mask], b1[mask] = c[mask], x[mask], 0

    mask = (1 <= h_prime) & (h_prime < 2)
    r1[mask], g1[mask], b1[mask] = x[mask], c[mask], 0

    mask = (2 <= h_prime) & (h_prime < 3)
    r1[mask], g1[mask], b1[mask] = 0, c[mask], x[mask]

    mask = (3 <= h_prime) & (h_prime < 4)
    r1[mask], g1[mask], b1[mask] = 0, x[mask], c[mask]

    mask = (4 <= h_prime) & (h_prime < 5)
    r1[mask], g1[mask], b1[mask] = x[mask], 0, c[mask]

    mask = (5 <= h_prime) & (h_prime < 6)
    r1[mask], g1[mask], b1[mask] = c[mask], 0, x[mask]

    # Calculate adjustment value to match luma (Y601)
    m = (l - (0.299 * r1 + 0.587 * g1 + 0.114 * b1))
    
    #calculate scale factor
    ms = np.where(l>0,(0.299 * r1 + 0.587 * g1 + 0.114 * b1)/l,epsilon)

    #calculate add factor
    ma = np.where(m+x>1, 2*m + c + x - 2, (m+c-1)/2)
    
    # Calculate Final RGB Values
    # case 1 (too bright): m + c > 1: add remainder to other channels
    # case 2 (normal): 0 <= m <= 1 - c : add m to all channels
    # case 3 (too dark): m < 0 : divide rgb1 by scale factor brightness/luma
    r = np.clip(np.where(m+c>1, r1 + m + ma, np.where(m<0, r1/(ms+epsilon), r1 + m)),0,1)
    g = np.clip(np.where(m+c>1, g1 + m + ma, np.where(m<0, g1/(ms+epsilon), g1 + m)),0,1)
    b = np.clip(np.where(m+c>1, b1 + m + ma, np.where(m<0, b1/(ms+epsilon), b1 + m)),0,1)
    
    # Stack R, G, B channels into an RGB image
    rgb_image = np.stack([r, g, b], axis=-1)

    return rgb_image

def hue(image1, image2):
    # Convert both images from RGB to HCL
    hcl1 = rgb_to_hcl(image1)
    hcl2 = rgb_to_hcl(image2)
    
    # Create the resulting HSL image by taking the hue from image2 and the saturation and lightness from image1
    result_hcl = np.stack([hcl2[:, :, 0], hcl1[:, :, 1], hcl1[:, :, 2]], axis=-1)
    
    # Convert the result back to RGB
    return hcl_to_rgb(result_hcl)

def saturation(image1, image2):
    # Convert both images from RGB to HCL
    hcl1 = rgb_to_hcl(image1)
    hcl2 = rgb_to_hcl(image2)
    
    # Combine the hue and lightness of the base image (image1) with the saturation of the blend image (image2)
    result_hcl = np.stack([hcl1[:, :, 0], hcl2[:, :, 1], hcl1[:, :, 2]], axis=-1)
    
    # Convert the result back to RGB
    return hcl_to_rgb(result_hcl)

def color(image1, image2):
    # Convert both images from RGB to HCL
    hcl1 = rgb_to_hcl(image1)
    hcl2 = rgb_to_hcl(image2)
    
    # Create the resulting HCL image by taking the hue and saturation from image2 and the lightness from image1
    result_hcl = np.stack([hcl2[:, :, 0], hcl2[:, :, 1], hcl1[:, :, 2]], axis=-1)
    
    # Convert the result back to RGB
    return hcl_to_rgb(result_hcl)

def luminosity(image1, image2):
    # Convert both images from RGB to HCL
    hcl1 = rgb_to_hcl(image1)
    hcl2 = rgb_to_hcl(image2)
    
    # Create the resulting HCL image by taking the hue and saturation from image1 and the lightness from image2
    result_hcl = np.stack([hcl1[:, :, 0], hcl1[:, :, 1], hcl2[:, :, 2]], axis=-1)
    
    # Convert the result back to RGB
    return hcl_to_rgb(result_hcl)

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
        
    elif blend_mode == 'darken':
        blended_image = np.minimum(image1, image2)
        
    elif blend_mode == 'multiply':
        blended_image = image1 * image2
        
    elif blend_mode == 'color burn':
        # Avoid division by zero and prevent values greater than 1
        blended_image = 1 - np.minimum(1, (1 - image1) / np.clip(image2, epsilon, 1))
    
    elif blend_mode == 'linear burn':
        blended_image = np.maximum(0, image1 + image2 - 1)    
    
    elif blend_mode == 'darker color':
        # Apply the color brightness formula
        brightness_image1 = calculate_color_brightness(image1)
        brightness_image2 = calculate_color_brightness(image2)
        # Find the minimum sum between the two images
        min_sum = np.minimum(brightness_image1, brightness_image2)
        # Use np.where to select colors based on the minimum sum
        mask = (brightness_image1 == min_sum)
        blended_image = np.where(mask[:, :, None], image1, image2)
        
    elif blend_mode == 'lighten':
        blended_image = np.maximum(image1, image2)    
    
    elif blend_mode == 'screen':
        blended_image = screen(image1, image2)
        
    elif blend_mode == 'color dodge':
        # Avoid division by zero and prevent values greater than 1
        blended_image = np.clip(image1 / (1 - image2 + epsilon), 0, 1)
        
    elif blend_mode == 'linear dodge':
        blended_image = np.clip(image1 + image2, 0, 1)    
    
    elif blend_mode == 'lighter color':
        # Apply the color brightness formula
        brightness_image1 = calculate_color_brightness(image1)
        brightness_image2 = calculate_color_brightness(image2)
        # Find the maximum sum between the two images
        min_sum = np.maximum(brightness_image1, brightness_image2)
        # Use np.where to select colors based on the maximum sum
        mask = (brightness_image1 == min_sum)
        blended_image = np.where(mask[:, :, None], image1, image2) 
        
    elif blend_mode == 'overlay':
        blended_image = np.where(
            image1 < 0.5,
            2 * image2 * image1,
            1 - 2 * (1 - image2) * (1 - image1)
        )   
        
    elif blend_mode == 'soft light':
        blended_image = np.where(
            image2 <= 0.5,
            image1 * (1 - (1 - 2 * image2) * (1 - image1)),
            image1 + (2 * image2 - 1) * (np.sqrt(image1) - image1)
        )
        
    elif blend_mode == 'hard light':
        blended_image = np.where(
            image2 < 0.5,
            2 * image2 * image1,
            1 - 2 * (1 - image2) * (1 - image1)
        )   
        
    elif blend_mode == 'vivid light':
        blended_image = np.where(
            image2 <= 0.5,
            1 - (1 - image1) / (2 * image2 + 1e-10),
            image1 / (2 * (1 - image2) + 1e-10)
        )
     
    elif blend_mode == 'linear light':
        blended_image = image1 + 2 * image2 - 1
        
    elif blend_mode == 'pin light':
        blended_image = np.where(
            image2 <= 0.5,
            np.minimum(image1, 2 * image2),
            np.maximum(image1, 2 * (image2 - 0.5))
        )
        
    elif blend_mode == 'hard mix':
        blended_image = np.where(image1 + image2 >= 1, 1, 0)    
        
    elif blend_mode == 'difference':
        blended_image = np.abs(image1[:,:,0:3] - image2[:,:,0:3])       
        
    elif blend_mode == 'exclusion':
        blended_image = np.abs(image1 + image2 - 2 * image1 * image2)
        
    elif blend_mode == 'subtract':
        blended_image = np.clip(image1 - image2, 0, 1)
    
    elif blend_mode == 'divide':
        # Avoid division by zero by adding a small value to image2
        blended_image = np.divide(image1, np.clip(image2, epsilon, 1))
        
    elif blend_mode == 'hue':
        blended_image = hue(image1, image2)
        
    elif blend_mode == 'saturation':
        blended_image = saturation(image1, image2)
        
    elif blend_mode == 'color':
        blended_image = color(image1, image2)
        
    elif blend_mode == 'luminosity':
        blended_image = luminosity(image1, image2)
        
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