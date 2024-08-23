# -*- coding: utf-8 -*-
# calculations.py
# This file contains various other functions.
#
# Author: Dani
# Created: 2022-01-22
# Last Modified: 2024-08-23
#
# Part of the Blend Mode Compendium Project
# Requires: numpy
# 
# Usage: Import this module and call the functions with appropriate parameters.
# Example:
# from calculations import calculate_absolute_error
# sae = calculate_absolute_error(image1, image2)

import numpy as np

def calculate_absolute_error(image1, image2):
    """
    Calculates the Sum of Absolute Error (SAE) between two color images.

    Parameters:
    - image1 (numpy.ndarray): First image array with values in [0, 1].
    - image2 (numpy.ndarray): Second image array with values in [0, 1].

    Returns:
    - sae (float): Sum of Absolute Error between the two images.
    """
    # Calculate SAE by summing the absolute differences across all channels
    return np.sum(np.abs(image1 - image2))