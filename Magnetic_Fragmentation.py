
# coding: utf-8

# Import required modules and set up matplotlib display properties. Set up variables.

# In[1]:

import astropy.units as u
import sunpy.map
import numpy as np
import matplotlib.pyplot as plt
import skimage.measure as ms
from split_pol_thresh import split_pol_thresh
from find_regions import find_regions
get_ipython().magic('matplotlib notebook')
plt.rcParams['figure.figsize'] = 11, 11
plt.rcParams.update({'font.size': 12})

import warnings
warnings.filterwarnings('ignore')

# Choose threshold. Any magnetic fields under this level (in Gauss) will be ignored.
threshold = 250 # Gauss


# Load magnetogram data into a SunPy map object.

# In[2]:

file_to_load = '' # insert HMI FITS file path between quotes

hmi = sunpy.map.Map(file_to_load)


# Display HMI magnetogram with coordinate grid overplotted.

# In[3]:

hmi.peek(draw_grid=True)


# Create submap and split submap into positive and negative magnetic field so that fragments can be found independently using the same code.

# In[4]:

hmi_submap = hmi.submap([-225, -590]*u.arcsec, [-342, -90]*u.arcsec)

submap_data = np.copy(hmi_submap.data)

# Zero all edges to remove edge effects
submap_data[0, :] = 0
submap_data[-1, :] = 0
submap_data[:, 0] = 0
submap_data[:, -1] = 0

# Split into positive and negative data frames
pos_data = split_pol_thresh(submap_data, threshold, 'pos')
neg_data = split_pol_thresh(submap_data, threshold, 'neg')


# In[30]:

pos_region_frame, num_pos_regions = find_regions(pos_data)
neg_region_frame, num_neg_regions = find_regions(neg_data)

pos_labeled_frame, pos_num_labels = ms.label(pos_region_frame.astype(int), return_num=True, connectivity=2)
neg_labeled_frame, neg_num_labels = ms.label(neg_region_frame.astype(int), return_num=True, connectivity=2)

pos_properties = ms.regionprops(pos_labeled_frame, intensity_image=pos_data)
neg_properties = ms.regionprops(neg_labeled_frame, intensity_image=neg_data)

hmi_submap.peek()

for region in pos_properties:
    x = region.centroid[1]
    y = region.centroid[0]
    plt.plot(x, y, 'rx')
    
for region in neg_properties:
    x = region.centroid[1]
    y = region.centroid[0]
    plt.plot(x, y, 'yx')


# ## Next steps
# 
# Save the positive and negative region data in a file format suitable for parsing in time.
# 
# Build tracking algorithm to catalogue the fragments temporally.
