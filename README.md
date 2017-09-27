# MagneticFragmentation

This repo contains the algorithms required to divide SDO/HMI magnetograms into individual magnetic fragments, based on a 'downhill' segmentation.

The algorithm allows the user to select a submap from the full HMI map (likely an active region) for the segmentation.

Also included are the codes to create fragment property lists for each image, and the code to pull them together by linking the individual fragments across images in space and time, creating a fragment store (currently factored as a dictionary) that can then be analysed.
