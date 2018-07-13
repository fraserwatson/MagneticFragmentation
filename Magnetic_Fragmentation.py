
# coding: utf-8

# Import required modules and set up matplotlib display properties. Set up variables.

# In[ ]:


# astropy.units allows us to use physical units throughout the code and easily
# perform calculations on them
import astropy.units as u
# sunpy.map handles the coordinates of the data we are using
import sunpy.map
from sunpy.coordinates import frames
# numpy is a package that makes handling arrays much easier
import numpy as np
# The SkyCoord object lets us convert between astronomical coordinate systems
from astropy.coordinates import SkyCoord
# matplotlib.pyplot is the standard plotting tool in python
import matplotlib.pyplot as plt
# skimage.measure performs the fragmentation
import skimage.measure as ms
# os is a library of operating system functions that we use to get filepaths
import os
# The next three imports are functions written just for this purpose
from split_pol_thresh import split_pol_thresh
from find_regions import find_regions
from write_props import write_props
from rotate_long import rotate_long
from window_corner_rotation import window_corner_rotation
# The next three lines are for plotting in a Jupyter notebook
# explanation of difference between: %matplotlib notebook and %matplotlib inline
# https://github.com/matplotlib/matplotlib/issues/4879
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = 11, 11
plt.rcParams.update({'font.size': 12})

# Choose active region working on, data to be read, path to save the bulk properties and location of the submap
# * It does not accept '~/Dropbox/....' as input
# * The bulk_properties.txt contains the total number of fragments in each image, the total area in each image, 
# and the total flux in each image. We will need these to make plots like in Fraser's thesis.
# * The code allows the user to choose the bottom left and top right point of the observation window
# the submap will be created. So I choose around the active region I want to study. Then, inside find_regions.py,
# it will read in the date of each HMI folder and differencially rotate where the bl and tr should be for each
# new map. Choose the bottom left and top right of the initial observation window using solar coordinates 
#(in arcsecs from disk centre)
#
# act_region='AR11158'
# bottom_left =[-300,-170]#[-230,-300]
# top_right =[-500,-310]#[10,-165]
# datapath = '/Users/dina/phd-mac/large_folders/AR11158_hmi_data/'
# bulk_region_props_path = '/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/AR11158_bulk_properties/bulk_props.txt
# images_path='/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/AR11158_images_050218/'
#
#act_region='AR11166'
#bottom_left =[-240,450]
#top_right =[-600,100]
#datapath = '/Users/dina/phd-mac/large_folders/AR11166_hmi_data/'
#bulk_region_props_path = '/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/AR11166_bulk_properties/bulk_props.txt'
#images_path='/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/AR11166_images_050218/'
#
act_region='AR12010'
#whole region
# bottom_left =[-120, -50] 
# top_right =[120, -230]
datapath = '/Users/dina/phd-mac/large_folders/Lucie_hmi_data/'
main_path = '/Users/dina/phd-mac/large_folders/MagneticFragmentation_github/output/'
#subregion
bottom_left_sub =[-50, -170] 
top_right_sub =[50, -100]
# images_path = main_path + act_region + '_subregion/'


# Choose threshold. Magnetic fields under this level (Gauss) will be ignored
threshold = 200#50 # Gauss


# Load magnetogram paths. The files_to_load includes the '.DS_store' file. glob will get rid of it

# In[ ]:


import glob
files_to_load=glob.glob(datapath+"/*")
print(len(files_to_load))
# os.getcwd() #gives the current directory


# Read in the first image and trasform the bl and tr of the first image from arcseconds to degrees

# In[ ]:


filename =files_to_load[0]

data = sunpy.map.Map(filename).rotate()
initial_obs_time = data.date
data.peek()

bl = SkyCoord(bottom_left_sub[0] * u.arcsec,
              bottom_left_sub[1] * u.arcsec, frame=frames.Helioprojective, obstime=initial_obs_time)  
tr = SkyCoord(top_right_sub[0] * u.arcsec,
              top_right_sub[1] * u.arcsec, frame=frames.Helioprojective, obstime=initial_obs_time) 
bl_stonyhurst = bl.transform_to(frames.HeliographicStonyhurst)
tr_stonyhurst = tr.transform_to(frames.HeliographicStonyhurst)


# Loop over files to find fragments and create text document that represents the properties of fragments in each image file.

# In[ ]:


# For each image...
for image in range(25,len(files_to_load)):
    print(image)
    # Create the full filepath of the FITS file
    filename =files_to_load[image] #if I use glob

    # Pull out the data into a SunPy map
    data = sunpy.map.Map(filename).rotate()
    
    # Transform the initial window coordinates into lat/long coordinates at the time of this image
    # Calculate the time difference in the form [days.fraction_of_day] from the original image in days
    # The brackets at total_seconds() indicate that this is a function attached to the variable
    timediff = (data.date - initial_obs_time).total_seconds()/86400
    [bl, tr] = window_corner_rotation(bl_stonyhurst, tr_stonyhurst, timediff, data.date) 

    # Create a submap using those coordinates
    # We are creating two submaps that are identical because from
    # this point on, all positive polarity data will be split from
    # negative polarity data
    pos_submap_area = data.submap(bl, tr)
    neg_submap_area = data.submap(bl, tr)
    
    # Set all of the edge pixels in the submaps to zero. If not and there is a label on the edge, when the code
    # will say "look at col+1 (or row+1)" I will be asking it to look out of the image and give back an error.
    neg_submap_area_data = np.array(neg_submap_area.data)
    pos_submap_area_data = np.array(pos_submap_area.data)
    # Add a padding around the submap by converting the last pixel of each side of the submap to zero.
    neg_submap_area_data = np.pad(neg_submap_area_data, ((1, 1), (1, 1)), 'constant', constant_values=(0, 0))
    pos_submap_area_data = np.pad(pos_submap_area_data, ((1, 1), (1, 1)), 'constant', constant_values=(0, 0))

    # Strip out all negative data in the positive submap, and vice versa
    pos_submap_data = split_pol_thresh(pos_submap_area_data, threshold, 'pos')
    neg_submap_data = split_pol_thresh(neg_submap_area_data, threshold, 'neg')
    
    # Find the regions in the positive and negative magnetogram data
    pos_region_frame, num_pos_regions = find_regions(pos_submap_data)
    neg_region_frame, num_neg_regions = find_regions(neg_submap_data)

    # Convert the data into label frames that scikit-image can use
    pos_labeled_frame, pos_num_labels = ms.label(pos_region_frame.astype(int),
                                                 return_num=True,
                                                 connectivity=2)
    neg_labeled_frame, neg_num_labels = ms.label(neg_region_frame.astype(int),
                                                 return_num=True,
                                                 connectivity=2)
    
    # Use the scikit-image method 'regionprops' to get various properties on
    # the fragments in the image data
    # Cache=False means that no properties will be computed until they are specifically called in write_props
    pos_properties = ms.regionprops(pos_labeled_frame,
                                    intensity_image=pos_submap_area.data, cache=False)
    neg_properties = ms.regionprops(neg_labeled_frame,
                                    intensity_image=neg_submap_area.data, cache=False)

    # Write the properties to files. Note that to add new properties,
    # you need to do so in the 'write_props' function
    write_props(pos_properties, 'p', image, data.date, pos_submap_area, act_region, threshold)
    write_props(neg_properties, 'n', image, data.date, neg_submap_area, act_region, threshold)
    
#     pos_submap_area.plot()
#     imagefilename = images_path + 'HMI_'+str(threshold)+'_G_' + str(image).zfill(4)
#     plt.savefig(imagefilename)
#     plt.clf()
    

