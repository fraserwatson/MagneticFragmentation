
# coding: utf-8

# With this code I re-create images produced by MagneticFragmantentation and overplot the bounding boxes of the fragments, as well as the centroids of the bounding boxes, per magnetogram.

# I need to reproduce the same image I made with Magnetic Fragmentation, with the same threshold. I then need to restore the properties I saved out and get the info about the position of the bounding boxes and the position of the centroids for each fragment. In the end, I want to plot the image and overplot the info of the bounding boxes.

# Sidenote: Although data.date gives the 'date_obs' of the hmi, the hmi .fits file itself has been named according to 't_rec'.
# 't_rec' has a format of '2014.03.23_00:00:00_TAI'. If I want to convert this to datetime object I keep only the 20 first digits and convert: #date_meta=dateparser.parse(data.meta.get('t_rec')[0:19])

# Import required modules and set up matplotlib display properties. Set up variables.

# In[ ]:


# astropy.units allows us to use physical units throughout the code and easily
# perform calculations on them
import astropy.units as u
# sunpy.map handles the coordinates of the data we are using
import sunpy.map
from sunpy.coordinates import frames
# numpy is a package that makes handling arrays much easier
#import numpy as np
# The SkyCoord object lets us convert between astronomical coordinate systems
from astropy.coordinates import SkyCoord
# matplotlib.pyplot is the standard plotting tool in python
import matplotlib.pyplot as plt
#importing csv module so I can read the output of write_props
import csv
from datetime import datetime
#mac seems to need glod to get rid of the .DS store file
import glob
#Readsav reads IDL .dat files
from scipy.io import readsav
#Needs installation: http://dateparser.readthedocs.io/en/latest/index.html
#It is very versatile but slows things down a lot
import dateparser
#Fraser's functions
from rotate_long import rotate_long
from window_corner_rotation import window_corner_rotation
from datetime import timedelta    
# The next three lines are for plotting in a Jupyter notebook
# explanation of difference between: %matplotlib notebook and %matplotlib inline here:
# https://github.com/matplotlib/matplotlib/issues/4879
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = 11, 11
plt.rcParams.update({'font.size': 12})

# Choose threshold. Magnetic fields under this level (Gauss) will be ignored
threshold = 200 # Gauss 

act_region='AR12010'
datapath = '/Users/dina/phd-mac/large_folders/Lucie_hmi_data/'
main_path = '/Users/dina/phd-mac/large_folders/MagneticFragmentation_github/output/'
fl_props_path_dat='/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/mag_flux_flarelists/fl_ar12010_properties.dat'
#whole region
bottom_left =[-120, -50] 
top_right =[120, -230]
images_path= main_path + 'bbox_boxes_flares_/'+str(threshold)+'G/'
propspath= main_path +act_region+'_'+str(threshold)+'G_fragment_properties/'


# First I need a sunpy object. Load the path with the hmi .fits files.

# In[ ]:


files_to_load=glob.glob(datapath+"/*")


# Load the path with the properties of fragments .txt files

# In[ ]:


props_to_load=glob.glob(propspath+"/*")


# Load the structure that contains information about all the RHESSI flares that happenned around the time the for loop will run later. 

# In[ ]:


#This might help: https://docs.python.org/3.3/reference/lexical_analysis.html#string-literals
f=readsav(fl_props_path_dat)

#See which arrays I have saved inside f, not the data
#[i for i in f]


# I need to load in the very first magnetogram. Its data and time will be stored. I will use this to transform the bottom left and top right points of the window from arcseconds to degrees as well as to perform differential rotation later.

# In[ ]:


filename =files_to_load[0]

data = sunpy.map.Map(filename).rotate()
initial_obs_time = data.date #it's a datetime object, gives the 'date_obs' of the hmi

#transform pixel to arcseconds
bl = SkyCoord(bottom_left_sub[0] * u.arcsec,
              bottom_left_sub[1] * u.arcsec, frame=frames.Helioprojective, obstime=initial_obs_time)  
tr = SkyCoord(top_right_sub[0] * u.arcsec,
              top_right_sub[1] * u.arcsec, frame=frames.Helioprojective, obstime=initial_obs_time) 
#transform arcseconds to degrees
bl_stonyhurst = bl.transform_to(frames.HeliographicStonyhurst)
tr_stonyhurst = tr.transform_to(frames.HeliographicStonyhurst)


# In[ ]:


#For loop for all magnetograms
for image in range(59,65):#len(files_to_load)):
    print(image)
    # Create the full filepath of the FITS file
    filename =files_to_load[image] #if I use glob

    # Pull out the data into a rotated,in an angle according to the hmi header, SunPy map
    data = sunpy.map.Map(filename).rotate()
    
    # Transform the initial window coordinates into lat/long coordinates at the time of this image
    # Calculate the timedifference in the form [days.fraction_of_day] from the original image in days
    # The brackets at total_seconds() indicate that this is a function attached to the variable
    timediff = (data.date - initial_obs_time).total_seconds()/86400
    [bl, tr] = window_corner_rotation(bl_stonyhurst, tr_stonyhurst, timediff, data.date) 

    # Create a submap using those coordinates
    submap_area = data.submap(bl, tr)
    
    #I want to load the correct fragment properties file, for the fragments with negative and positive flux.
    #To do this I use the 'date-obs' from the hmi header, which is given from the data.date
    #I convert this to the exact format the properties files have been stored.
    neg_properties=propspath+'{0}'.format(data.date.strftime('%Y%m%d_%H%M%S'))+'_n.txt'
    pos_properties=propspath+'{0}'.format(data.date.strftime('%Y%m%d_%H%M%S'))+'_p.txt'
    
    #I define new arrays to read in what I want to use later.
    #Here, the latitide and longitude of the centroids of the fragments (in degrees)
    #and the 4 outer points of the bounding box of each fragment:
    #bb_min_row,bb_max_row, bb_max_col, bb_max_row (in degress).
    nc_lat=[]
    nc_lng=[]
    n_x_min=[]
    n_y_min=[]
    n_x_max=[]
    n_y_max=[]
    
    #read the properties in, if they exist. Else move on with the loop.
    my_file = Path(neg_properties)
    if my_file.is_file():
        with open(neg_properties,'r') as neg:
            filereader = csv.reader(neg, delimiter=',')
            for column in filereader:
                nc_lat.append(float(column[1])) #latitude of centroids 
                nc_lng.append(float(column[2])) #longitude of centroids 
                n_x_min.append(float(column[5])) #xmin of bounding box 
                n_y_min.append(float(column[6])) #ymin of bounding box
                n_x_max.append(float(column[7])) #xmax of bounding box 
                n_y_max.append(float(column[8])) #ymax of bounding box 
    else:
        continue
            
    
    pc_lat=[] 
    pc_lng=[]
    p_x_min=[]
    p_y_min=[]
    p_x_max=[]
    p_y_max=[]
    
    with open(pos_properties,'r') as pos:
        filereader = csv.reader(pos, delimiter=',')
        for column in filereader:
            pc_lat.append(float(column[1]))
            pc_lng.append(float(column[2]))  
            p_x_min.append(float(column[5]))
            p_y_min.append(float(column[6]))
            p_x_max.append(float(column[7]))
            p_y_max.append(float(column[8]))
    
            
    #From the flares I loaded before, I want only the ones that happened around the time of each hmi magnetogram   
    fl_lat_sel=[]
    fl_lng_sel=[]
    fl_stim_sel=[]
    fl_ptim_sel = []
    fl_etim_sel = []
    fl_bsgclass_sel = []
    for i in range(len(f.fl_stim)):
        #Look at the time period 
        #[stim-time between two consecutive magnetograms,etim+time between two consecutive magnetograms]
        if dateparser.parse(str(f.fl_stim[i])) >= data.date-timedelta(minutes=24)        and dateparser.parse(str(f.fl_etim[i])) <= data.date+timedelta(minutes=24):
            fl_lat_sel.append(f.fl_lat[i])
            fl_lng_sel.append(f.fl_lng[i])
            fl_stim_sel.append(f.fl_stim[i])
            fl_ptim_sel.append(f.fl_ptim[i])
            fl_etim_sel.append(f.fl_etim[i])
            fl_bsgclass_sel.append(f.fl_bsgclass[i])

     #Plot out a map and save it
    
    #Plot the submap
    ax=plt.subplot(projection=submap_area)
    submap_area.plot()
    ax.set_autoscale_on(False) 
   
    #Overplot the bounding boxes  
    #The overpolotting on the boxes is in helioprojectve coordinates.
    #Explanation: Centroids and flares are considered as points on the map and therefore are in Stonyhurst.
    #The boxes are considered as projected in the sky, so they are on helioprojective coordinates.
    hpc_out=sunpy.coordinates.Helioprojective(observer="earth", obstime=submap_area.date)

    for j in range(0,1):#len(n_x_min)):
        bottom_left_frag = SkyCoord(n_x_min[j]* u.deg, n_y_min[j]* u.deg, frame="heliographic_stonyhurst")
        top_right_frag = SkyCoord(n_x_max[j]* u.deg, n_y_max[j]* u.deg, frame="heliographic_stonyhurst")
        
        blf_p=bottom_left_frag.transform_to(hpc_out)
        trf_p=top_right_frag.transform_to(hpc_out)
        width=abs(blf_p.Tx.value-trf_p.Tx.value)
        height=abs(blf_p.Ty.value-trf_p.Ty.value)
        
        submap_area.draw_rectangle(top_right_frag, width*u.arcsec, height*u.arcsec,color='y')
        
    for j in range(0,1):#len(p_x_min)):
        bottom_left_frag = SkyCoord(p_x_min[j]* u.deg, p_y_min[j]* u.deg, frame="heliographic_stonyhurst")
        top_right_frag = SkyCoord(p_x_max[j]* u.deg, p_y_max[j]* u.deg, frame="heliographic_stonyhurst")
        
        blf_p=bottom_left_frag.transform_to(hpc_out)
        trf_p=top_right_frag.transform_to(hpc_out)
        #The width will be the angle theta on the horisontal plane field of the sky
        width=abs(blf_p.Tx.value-trf_p.Tx.value)
        #The height will be the angle theta on the vertical plane field of the sky
        height=abs(blf_p.Ty.value-trf_p.Ty.value)
        
        submap_area.draw_rectangle(top_right_frag, width*u.arcsec, height*u.arcsec,color='b')
            
        
    #Overplot the centroids
    c = SkyCoord(nc_lng * u.deg, nc_lat* u.deg, frame="heliographic_stonyhurst")
    ax.plot_coord(c, 'yx')

    c = SkyCoord(pc_lng * u.deg, pc_lat * u.deg, frame="heliographic_stonyhurst")
    ax.plot_coord(c, 'bx')
   
    #Overplot the flares
    c = SkyCoord(fl_lng_sel * u.deg, fl_lat_sel * u.deg, frame="heliographic_stonyhurst")
    ax.plot_coord(c, 'ro', markersize=14)

#     imagefilename = images_path + 'HMI_bboxes_'+str(threshold)+'G_' + str(image).zfill(4)
#     plt.savefig(imagefilename)
#     plt.clf()

