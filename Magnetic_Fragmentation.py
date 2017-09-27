
# coding: utf-8

# Import required modules and set up matplotlib display properties. Set up variables.

# In[10]:

import astropy.units as u
import sunpy.map
import numpy as np
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import skimage.measure as ms
import os
from split_pol_thresh import split_pol_thresh
from find_regions import find_regions
from write_props import write_props
get_ipython().magic('matplotlib notebook')
plt.rcParams['figure.figsize'] = 11, 11
plt.rcParams.update({'font.size': 12})

# Choose threshold. Any magnetic fields under this level (in Gauss) will be ignored.
threshold = 250 # Gauss
datapath = '/Users/fraser/Data/HMImag/' #location of the input data files


# Load magnetogram paths.

# In[5]:

files_to_load = os.listdir(datapath)


# Loop over files to find fragments and create text document that represents the properties of fragments in each image file.

# In[31]:

for image in range(1):#len(files_to_load)):
    # Create the full filepath of the FITS file
    filename = datapath + files_to_load[image]
    
    # Pull out the data into a SunPy map
    data = sunpy.map.Map(filename)
    
    # Choose which part of the image we want to look at using solar coordinate
    bl = SkyCoord(-590 * u.arcsec, -342 * u.arcsec)
    tr = SkyCoord(-225 * u.arcsec, -90 * u.arcsec)
    
    # Create a submap using those coordinates
    pos_submap_area = data.submap(bl, tr)
    neg_submap_area = data.submap(bl, tr)
    
    pos_submap_area.data[0][:] = 0
    pos_submap_area.data[-1][:] = 0
    pos_submap_area.data[:][0] = 0
    pos_submap_area.data[:][-1] =0
    
    neg_submap_area.data[0][:] = 0
    neg_submap_area.data[-1][:] = 0
    neg_submap_area.data[:][0] = 0
    neg_submap_area.data[:][-1] =0
    
    pos_submap_data = split_pol_thresh(pos_submap_area.data, threshold, 'pos')
    neg_submap_data = split_pol_thresh(neg_submap_area.data, threshold, 'neg')
    
    # Find the regions in the positive and negative magnetogram data
    pos_region_frame, num_pos_regions = find_regions(pos_submap_data)
    neg_region_frame, num_neg_regions = find_regions(neg_submap_data)
    
    # Convert the data into label frames that scikit-image can use
    pos_labeled_frame, pos_num_labels = ms.label(pos_region_frame.astype(int), return_num=True, connectivity=2)
    neg_labeled_frame, neg_num_labels = ms.label(neg_region_frame.astype(int), return_num=True, connectivity=2)
    
    # Use the scikit-image method 'regionprops' to get various properties on the fragments in the image data
    pos_properties = ms.regionprops(pos_labeled_frame, intensity_image=pos_submap_area.data)
    neg_properties = ms.regionprops(neg_labeled_frame, intensity_image=neg_submap_area.data)
    
    write_props(pos_properties, 'p', image, data.date, pos_submap_area)
    write_props(neg_properties, 'n', image, data.date, neg_submap_area)


# In[69]:

from sunpy.coordinates import frames

test_coord = neg_submap_area.pixel_to_world(539 * u.pix, 139 * u.pix)   
    
new_coord = test_coord.transform_to(frames.HeliographicStonyhurst)

print(new_coord)

new_coord.lon

