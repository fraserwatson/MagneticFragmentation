# MagneticFragmentation

This repo contains the algorithms required to divide SDO/HMI magnetograms into individual magnetic fragments, based on a 'downhill' segmentation.

The algorithm allows the user to select a submap from the full HMI map (likely an active region) for the segmentation.

The code currently requires the following modules:
* AstroPy
* SunPy
* numpy
* matplotlib
* skimage (a scientific image analysis module)

Next to do:
* Build tracking algorithm to catalogue the fragments temporally.