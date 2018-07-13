
# coding: utf-8

# In[1]:


# The datetime library gives us an easy way to manage dates and times in the code
from datetime import datetime
# Pickle lets us save objects to disk that can be loaded back into other python routines later on
import pickle
import numpy as np
from os import listdir
from fragment_file_reader import fragment_file_reader
from find_closest_fragment import find_closest_fragment

# Which active region am I working on?
act_region='SPoCA21717'

# Choose threshold. Magnetic fields under this level (Gauss) will be ignored
threshold = 50 # Gauss 

# What directory are the text files stored in?
main='/Users/dina/phd-mac/large_folders/mag_frag_project/PhD_work_MagFrag/'
basedir = main+'output_'+act_region+'/'+act_region+'_'+str(threshold)+'G/'+act_region+'_'+str(threshold)+'G_fragment_properties/'

# Get list of files to use
files =[basedir + i for i in listdir(basedir)]

# Split the list into two lists, one for positive fragments and one for negative fragments
neg_files = [s for s in files if 'n.' in s]
pos_files = [s for s in files if 'p.' in s]

# Set up the individual store dictionaries
neg_store = {}
neg_store_number = 0
pos_store = {}
pos_store_number = 0

print(neg_files[0])
print(pos_files[0])

# For the first image, there is no previous timestep to compare against. All fragments are put into the store.
[neg_dates, neg_latitudes, neg_longitudes, neg_area, neg_eccentricity, neg_bbox_x_min, neg_bbox_y_min, neg_bbox_x_max, neg_bbox_y_max, neg_area_bbox, neg_cen_bbox_y, neg_cen_bbox_x, neg_flux, neg_min_flux, neg_mean_flux, neg_max_flux, neg_blos, neg_min_blos, neg_mean_blos, neg_max_blos, neg_w_cen_y, neg_w_cen_x, neg_ori, neg_major, neg_minor] = fragment_file_reader(neg_files[0])

# For each fragment from the first image, create a new fragment record in the dictionary. Keys start at '0' and
# go up one every time a new fragment is added
for i in range(len(neg_dates)):
    # Keys needs to be strings!
    neg_store[str(neg_store_number)] = [neg_dates[i]], [neg_latitudes[i]], [neg_longitudes[i]], [neg_area[i]], [neg_eccentricity[i]], [neg_bbox_x_min[i]], [neg_bbox_y_min[i]], [neg_bbox_x_max[i]], [neg_bbox_y_max[i]], [neg_area_bbox[i]], [neg_cen_bbox_y[i]], [neg_cen_bbox_x[i]],[neg_flux[i]], [neg_min_flux[i]], [neg_mean_flux[i]], [neg_max_flux[i]], [neg_blos[i]], [neg_min_blos[i]], [neg_mean_blos[i]], [neg_max_blos[i]], [neg_w_cen_y[i]], [neg_w_cen_x[i]], [neg_ori[i]], [neg_major[i]], [neg_minor[i]]
    neg_store_number += 1

# Do the same thing for the positive fragment data
[pos_dates, pos_latitudes, pos_longitudes, pos_area, pos_eccentricity, pos_bbox_x_min, pos_bbox_y_min, pos_bbox_x_max, pos_bbox_y_max, pos_area_bbox, pos_cen_bbox_y, pos_cen_bbox_x, pos_flux, pos_min_flux, pos_mean_flux, pos_max_flux, pos_blos, pos_min_blos, pos_mean_blos, pos_max_blos, pos_w_cen_y, pos_w_cen_x, pos_ori, pos_major, pos_minor] = fragment_file_reader(pos_files[0])

for i in range(len(pos_dates)):
    pos_store[str(pos_store_number)] = [pos_dates[i]], [pos_latitudes[i]], [pos_longitudes[i]], [pos_area[i]], [pos_eccentricity[i]], [pos_bbox_x_min[i]], [pos_bbox_y_min[i]], [pos_bbox_x_max[i]], [pos_bbox_y_max[i]], [pos_area_bbox[i]], [pos_cen_bbox_y[i]], [pos_cen_bbox_x[i]], [pos_flux[i]], [pos_min_flux[i]], [pos_mean_flux[i]], [pos_max_flux[i]], [pos_blos[i]], [pos_min_blos[i]], [pos_mean_blos[i]], [pos_max_blos[i]], [pos_w_cen_y[i]], [pos_w_cen_x[i]], [pos_ori[i]], [pos_major[i]], [pos_minor[i]]
    pos_store_number += 1


# For each subsequent image (using the negative file number to keep track, but the positive one is the same)
for image in range(1, len(neg_files)):
    print(image)
    # Get fragments from new image
    [neg_dates_new, neg_latitudes_new, neg_longitudes_new, neg_area_new, neg_eccentricity_new, neg_bbox_x_min_new, neg_bbox_y_min_new, neg_bbox_x_max_new, neg_bbox_y_max_new, neg_area_bbox_new, neg_cen_bbox_y_new, neg_cen_bbox_x_new, neg_flux_new, neg_min_flux_new,neg_mean_flux_new, neg_max_flux_new, neg_blos_new, neg_min_blos_new, neg_mean_blos_new, neg_max_blos_new, neg_w_cen_y_new, neg_w_cen_x_new, neg_ori_new, neg_major_new, neg_minor_new] = fragment_file_reader(neg_files[image])
    # Get timestamp of old image to use to search the fragment store
    neg_date_old = fragment_file_reader(neg_files[image-1])[0][0]
    
    # Get fragments from new image
    [pos_dates_new, pos_latitudes_new, pos_longitudes_new, pos_area_new, pos_eccentricity_new, pos_bbox_x_min_new, pos_bbox_y_min_new, pos_bbox_x_max_new, pos_bbox_y_max_new, pos_area_bbox_new, pos_cen_bbox_y_new, pos_cen_bbox_x_new, pos_flux_new, pos_min_flux_new, pos_mean_flux_new, pos_max_flux_new, pos_blos_new, pos_min_blos_new, pos_mean_blos_new, pos_max_blos_new, pos_w_cen_y_new, pos_w_cen_x_new, pos_ori_new, pos_major_new, pos_minor_new] = fragment_file_reader(pos_files[image])
    # Get timestamp of old image to use to search the fragment store
    pos_date_old = fragment_file_reader(pos_files[image-1])[0][0]
    
    # Search the region store and pull out all fragments that are in the old image
    # Reset the negative key list and old lat long lists
    neg_key_list = []
    neg_latitudes_old = []
    neg_longitudes_old = []

    for key in neg_store:
        if neg_store[key][0][-1] == neg_date_old:
            # Find which keys in the dictionary contain fragments from the previous image and get their key, lat, and long
            neg_key_list.append(key)
            neg_latitudes_old.append(neg_store[key][1][-1])
            neg_longitudes_old.append(neg_store[key][2][-1])
    
    # Reset the positive key list and old lat long lists
    pos_key_list = []
    pos_latitudes_old = []
    pos_longitudes_old = []

    for key in pos_store:
        if pos_store[key][0][-1] == pos_date_old:
            # Find which keys in the dictionary contain fragments from the previous image and get their key, lat, and long
            pos_key_list.append(key)
            pos_latitudes_old.append(pos_store[key][1][-1])
            pos_longitudes_old.append(pos_store[key][2][-1])
    
    # Calculate the time difference between the old and new images to remove solar rotation
    time_delta = (neg_dates_new[0] - neg_date_old).total_seconds()/86400
    # For each fragment in the new image, find the closest one in space in the old image
    for fragment in range(len(neg_latitudes_new)):
        [distance, index] = find_closest_fragment(neg_latitudes_new[fragment], neg_longitudes_new[fragment], neg_latitudes_old, neg_longitudes_old, time_delta)
        
        # Set a maximum reasonable distance based on the timedelta
        # If fragment is close enough, append it to an old entry
        # Otherwise, create a new one.
        if (distance / time_delta) < 5: 
        
            # Then append that fragments properties to the key of the old one
            append_key = neg_key_list[index]
            neg_store[append_key][0].append(neg_dates_new[fragment])
            neg_store[append_key][1].append(neg_latitudes_new[fragment])
            neg_store[append_key][2].append(neg_longitudes_new[fragment])
            neg_store[append_key][3].append(neg_area_new[fragment])
            neg_store[append_key][4].append(neg_eccentricity_new[fragment])
            neg_store[append_key][5].append(neg_bbox_x_min_new[fragment])
            neg_store[append_key][6].append(neg_bbox_y_min_new[fragment])
            neg_store[append_key][7].append(neg_bbox_x_max_new[fragment])
            neg_store[append_key][8].append(neg_bbox_y_max_new[fragment])
            neg_store[append_key][9].append(neg_area_bbox_new[fragment])
            neg_store[append_key][10].append(neg_cen_bbox_y_new[fragment])
            neg_store[append_key][11].append(neg_cen_bbox_x_new[fragment])
            neg_store[append_key][12].append(neg_flux_new[fragment])
            neg_store[append_key][13].append(neg_min_flux_new[fragment])
            neg_store[append_key][14].append(neg_mean_flux_new[fragment])
            neg_store[append_key][15].append(neg_max_flux_new[fragment])
            neg_store[append_key][16].append(neg_blos_new[fragment])
            neg_store[append_key][17].append(neg_min_blos_new[fragment])
            neg_store[append_key][18].append(neg_mean_blos_new[fragment])
            neg_store[append_key][19].append(neg_max_blos_new[fragment])
            neg_store[append_key][20].append(neg_w_cen_y_new[fragment])
            neg_store[append_key][21].append(neg_w_cen_x_new[fragment])
            neg_store[append_key][22].append(neg_ori_new[fragment])
            neg_store[append_key][23].append(neg_major_new[fragment])
            neg_store[append_key][24].append(neg_minor_new[fragment])

            # And remove that fragment from the 'old' list as only one new can link to one old
            if len(neg_latitudes_old) > 1:
                del neg_key_list[index]
                del neg_latitudes_old[index]
                del neg_longitudes_old[index]

            else:
                break
        
        else:
            # If no old fragments are close enough, create a new record for this new fragment
            neg_store[str(neg_store_number)] = [neg_dates_new[fragment]], [neg_latitudes_new[fragment]], [neg_longitudes_new[fragment]], [neg_area_new[fragment]], [neg_eccentricity_new[fragment]], [neg_bbox_x_min_new[fragment]], [neg_bbox_y_min_new[fragment]], [neg_bbox_x_max_new[fragment]], [neg_bbox_y_max_new[fragment]],[neg_area_bbox_new[fragment]], [neg_cen_bbox_y_new[fragment]],[neg_cen_bbox_x_new[fragment]], [neg_flux_new[fragment]],[neg_min_flux_new[fragment]], [neg_mean_flux_new[fragment]],[neg_max_flux_new[fragment]], [neg_blos_new[fragment]], [neg_min_blos_new[fragment]], [neg_mean_blos_new[fragment]], [neg_max_blos_new[fragment]], [neg_w_cen_y_new[fragment]], [neg_w_cen_x_new[fragment]], [neg_ori_new[fragment]], [neg_major_new[fragment]], [neg_minor_new[fragment]]
            neg_store_number += 1

    # Calculate the time difference between the old and new images to remove solar rotation
    time_delta = (pos_dates_new[0] - pos_date_old).total_seconds()/86400
    # For each fragment in the new image, find the closest one in space in the old image
    for fragment in range(len(pos_latitudes_new)):
        [distance, index] = find_closest_fragment(pos_latitudes_new[fragment], pos_longitudes_new[fragment], pos_latitudes_old, pos_longitudes_old, time_delta)
        
        # Set a maximum reasonable distance based on the timedelta
        # If fragment is close enough, append it to an old entry
        # Otherwise, create a new one.
        if (distance / time_delta) < 5:
        
            # Then append that fragments properties to the key of the old one
            append_key = pos_key_list[index]
            pos_store[append_key][0].append(pos_dates_new[fragment])
            pos_store[append_key][1].append(pos_latitudes_new[fragment])
            pos_store[append_key][2].append(pos_longitudes_new[fragment])
            pos_store[append_key][3].append(pos_area_new[fragment])
            pos_store[append_key][4].append(pos_eccentricity_new[fragment])
            pos_store[append_key][5].append(pos_bbox_x_min_new[fragment])
            pos_store[append_key][6].append(pos_bbox_y_min_new[fragment])
            pos_store[append_key][7].append(pos_bbox_x_max_new[fragment])
            pos_store[append_key][8].append(pos_bbox_y_max_new[fragment])
            pos_store[append_key][9].append(pos_area_bbox_new[fragment])
            pos_store[append_key][10].append(pos_cen_bbox_y_new[fragment])
            pos_store[append_key][11].append(pos_cen_bbox_x_new[fragment])
            pos_store[append_key][12].append(pos_flux_new[fragment])
            pos_store[append_key][13].append(pos_min_flux_new[fragment])
            pos_store[append_key][14].append(pos_mean_flux_new[fragment])
            pos_store[append_key][15].append(pos_max_flux_new[fragment])
            pos_store[append_key][16].append(pos_blos_new[fragment])
            pos_store[append_key][17].append(pos_min_blos_new[fragment])
            pos_store[append_key][18].append(pos_mean_blos_new[fragment])
            pos_store[append_key][19].append(pos_max_blos_new[fragment])
            pos_store[append_key][20].append(pos_w_cen_bbox_y_new[fragment])
            pos_store[append_key][21].append(pos_w_cen_bbox_x_new[fragment])
            pos_store[append_key][22].append(pos_ori_new[fragment])
            pos_store[append_key][23].append(pos_major_new[fragment])
            pos_store[append_key][24].append(pos_minor_new[fragment])



            # And remove that fragment from the 'old' list as only one new can link to one old
            if len(pos_latitudes_old) > 1:
                del pos_key_list[index]
                del pos_latitudes_old[index]
                del pos_longitudes_old[index]

            else:
                break
        
        else:
            # If no old fragments are close enough, create a new record for this new fragment
            pos_store[str(pos_store_number)] = [pos_dates_new[fragment]], [pos_latitudes_new[fragment]], [pos_longitudes_new[fragment]], [pos_area_new[fragment]], [pos_eccentricity_new[fragment]], [pos_bbox_x_min_new[fragment]], [pos_bbox_y_min_new[fragment]], [pos_bbox_x_max_new[fragment]], [pos_bbox_y_max_new[fragment]], [pos_area_bbox_new[fragment]], [pos_cen_bbox_y_new[fragment]], [pos_cen_bbox_x_new[fragment]], [pos_flux_new[fragment]], [pos_min_flux_new[fragment]], [pos_mean_flux_new[fragment]], [pos_max_flux_new[fragment]], [pos_blos_new[fragment]], [pos_min_blos_new[fragment]], [pos_mean_blos_new[fragment]], [pos_max_blos_new[fragment]], [pos_w_cen_y_new[fragment]], [pos_w_cen_x_new[fragment]], [pos_ori_new[fragment]], [pos_major_new[fragment]], [pos_minor_new[fragment]]
            pos_store_number += 1

# Save the fragment store objects to disk for later analysis
output = open(main+'output_'+act_region+'/'+act_region+'_'+str(threshold)+'G'+'/'+'negative_store_'+act_region+'_'+str(threshold)+'G.pkl', 'wb')
pickle.dump(neg_store, output)
output.close()
output = open(main+'output_'+act_region+'/'+act_region+'_'+str(threshold)+'G'+'/'+'positive_store_'+act_region+'_'+str(threshold)+'G.pkl', 'wb')
pickle.dump(pos_store, output)
output.close()


# In[3]:


# The datetime library gives us an easy way to manage dates and times in the code
from datetime import datetime
# Pickle lets us save objects to disk that can be loaded back into other python routines later on
import pickle
import numpy as np
from os import listdir
from fragment_file_reader import fragment_file_reader
from find_closest_fragment import find_closest_fragment

# Which active region am I working on?
act_region='SPoCA21717'

# Choose threshold. Magnetic fields under this level (Gauss) will be ignored
threshold = 50 # Gauss 

# What directory are the text files stored in?
main='/Users/dina/phd-mac/large_folders/mag_frag_project/PhD_work_MagFrag/'
basedir = main+'output_'+act_region+'/'+act_region+'_'+str(threshold)+'G/'+act_region+'_'+str(threshold)+'G_fragment_properties/'

# Get list of files to use
files =[basedir + i for i in listdir(basedir)]

# Split the list into two lists, one for positive fragments and one for negative fragments
neg_files = [s for s in files if 'n.' in s]
pos_files = [s for s in files if 'p.' in s]

# Set up the individual store dictionaries
neg_store = {}
neg_store_number = 0
pos_store = {}
pos_store_number = 0

print(neg_files[0])
print(pos_files[0])

# For the first image, there is no previous timestep to compare against. All fragments are put into the store.
[neg_dates, neg_latitudes, neg_longitudes, neg_area, neg_eccentricity, neg_bbox_x_min, neg_bbox_y_min, neg_bbox_x_max, neg_bbox_y_max, neg_area_bbox, neg_cen_bbox_y, neg_cen_bbox_x, neg_flux, neg_min_flux, neg_mean_flux, neg_max_flux, neg_blos, neg_min_blos, neg_mean_blos, neg_max_blos, neg_w_cen_y, neg_w_cen_x, neg_ori, neg_major, neg_minor] = fragment_file_reader(neg_files[0])

# For each fragment from the first image, create a new fragment record in the dictionary. Keys start at '0' and
# go up one every time a new fragment is added
for i in range(len(neg_dates)):
    # Keys needs to be strings!
    neg_store[str(neg_store_number)] = [neg_dates[i]], [neg_latitudes[i]], [neg_longitudes[i]], [neg_area[i]], [neg_eccentricity[i]], [neg_bbox_x_min[i]], [neg_bbox_y_min[i]], [neg_bbox_x_max[i]], [neg_bbox_y_max[i]], [neg_area_bbox[i]], [neg_cen_bbox_y[i]], [neg_cen_bbox_x[i]],[neg_flux[i]], [neg_min_flux[i]], [neg_mean_flux[i]], [neg_max_flux[i]], [neg_blos[i]], [neg_min_blos[i]], [neg_mean_blos[i]], [neg_max_blos[i]], [neg_w_cen_y[i]], [neg_w_cen_x[i]], [neg_ori[i]], [neg_major[i]], [neg_minor[i]]
    neg_store_number += 1

# Do the same thing for the positive fragment data
[pos_dates, pos_latitudes, pos_longitudes, pos_area, pos_eccentricity, pos_bbox_x_min, pos_bbox_y_min, pos_bbox_x_max, pos_bbox_y_max, pos_area_bbox, pos_cen_bbox_y, pos_cen_bbox_x, pos_flux, pos_min_flux, pos_mean_flux, pos_max_flux, pos_blos, pos_min_blos, pos_mean_blos, pos_max_blos, pos_w_cen_y, pos_w_cen_x, pos_ori, pos_major, pos_minor] = fragment_file_reader(pos_files[0])

for i in range(len(pos_dates)):
    pos_store[str(pos_store_number)] = [pos_dates[i]], [pos_latitudes[i]], [pos_longitudes[i]], [pos_area[i]], [pos_eccentricity[i]], [pos_bbox_x_min[i]], [pos_bbox_y_min[i]], [pos_bbox_x_max[i]], [pos_bbox_y_max[i]], [pos_area_bbox[i]], [pos_cen_bbox_y[i]], [pos_cen_bbox_x[i]], [pos_flux[i]], [pos_min_flux[i]], [pos_mean_flux[i]], [pos_max_flux[i]], [pos_blos[i]], [pos_min_blos[i]], [pos_mean_blos[i]], [pos_max_blos[i]], [pos_w_cen_y[i]], [pos_w_cen_x[i]], [pos_ori[i]], [pos_major[i]], [pos_minor[i]]
    pos_store_number += 1


# For each subsequent image (using the negative file number to keep track, but the positive one is the same)
for image in range(1, len(neg_files)):
    print(image)
    # Get fragments from new image
    [neg_dates_new, neg_latitudes_new, neg_longitudes_new, neg_area_new, neg_eccentricity_new, neg_bbox_x_min_new, neg_bbox_y_min_new, neg_bbox_x_max_new, neg_bbox_y_max_new, neg_area_bbox_new, neg_cen_bbox_y_new, neg_cen_bbox_x_new, neg_flux_new, neg_min_flux_new,neg_mean_flux_new, neg_max_flux_new, neg_blos_new, neg_min_blos_new, neg_mean_blos_new, neg_max_blos_new, neg_w_cen_y_new, neg_w_cen_x_new, neg_ori_new, neg_major_new, neg_minor_new] = fragment_file_reader(neg_files[image])
    # Get timestamp of old image to use to search the fragment store
    neg_date_old = fragment_file_reader(neg_files[image-1])[0][0]
    
    # Get fragments from new image
    [pos_dates_new, pos_latitudes_new, pos_longitudes_new, pos_area_new, pos_eccentricity_new, pos_bbox_x_min_new, pos_bbox_y_min_new, pos_bbox_x_max_new, pos_bbox_y_max_new, pos_area_bbox_new, pos_cen_bbox_y_new, pos_cen_bbox_x_new, pos_flux_new, pos_min_flux_new, pos_mean_flux_new, pos_max_flux_new, pos_blos_new, pos_min_blos_new, pos_mean_blos_new, pos_max_blos_new, pos_w_cen_y_new, pos_w_cen_x_new, pos_ori_new, pos_major_new, pos_minor_new] = fragment_file_reader(pos_files[image])
    # Get timestamp of old image to use to search the fragment store
    pos_date_old = fragment_file_reader(pos_files[image-1])[0][0]
    
    # Search the region store and pull out all fragments that are in the old image
    # Reset the negative key list and old lat long lists
    neg_key_list = []
    neg_latitudes_old = []
    neg_longitudes_old = []

    for key in neg_store:
        if neg_store[key][0][-1] == neg_date_old:
            # Find which keys in the dictionary contain fragments from the previous image and get their key, lat, and long
            neg_key_list.append(key)
            neg_latitudes_old.append(neg_store[key][1][-1])
            neg_longitudes_old.append(neg_store[key][2][-1])
    
    # Reset the positive key list and old lat long lists
    pos_key_list = []
    pos_latitudes_old = []
    pos_longitudes_old = []

    for key in pos_store:
        if pos_store[key][0][-1] == pos_date_old:
            # Find which keys in the dictionary contain fragments from the previous image and get their key, lat, and long
            pos_key_list.append(key)
            pos_latitudes_old.append(pos_store[key][1][-1])
            pos_longitudes_old.append(pos_store[key][2][-1])
    
    # Calculate the time difference between the old and new images to remove solar rotation
    time_delta = (neg_dates_new[0] - neg_date_old).total_seconds()/86400
    # For each fragment in the new image, find the closest one in space in the old image
    for fragment in range(len(neg_latitudes_new)):
        [distance, index] = find_closest_fragment(neg_latitudes_new[fragment], neg_longitudes_new[fragment], neg_latitudes_old, neg_longitudes_old, time_delta)
        
        print(distance,time_delta)      


# In[6]:


print(neg_latitudes_new)

