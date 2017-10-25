
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
#act_region='AR11158'
act_region='AR12010'

# What directory are the text files stored in?
#basedir = '/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/'+act_region+'_fragment_properties/'
#basedir = '/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/AR11158_fragment_properties/'
basedir = '/Users/fraser/Github/MagneticFragmentationOutput/fragment_properties/'

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

# For the first image, there is no previous timestep to compare against. All fragments are put into the store.
[neg_dates, neg_latitudes, neg_longitudes, neg_area, neg_eccentricity, neg_bbox_min_row, neg_bbox_min_col, neg_bbox_max_row, neg_bbox_max_col, neg_area_bbox, neg_cen_bbox_row, neg_cen_bbox_col, neg_flux, neg_min_flux, neg_mean_flux, neg_max_flux] = fragment_file_reader(neg_files[0])

# For each fragment from the first image, create a new fragment record in the dictionary. Keys start at '0' and
# go up one every time a new fragment is added
for i in range(len(neg_dates)):
    # Keys needs to be strings!
    neg_store[str(neg_store_number)] = [neg_dates[i]], [neg_latitudes[i]], [neg_longitudes[i]], [neg_area[i]], [neg_eccentricity[i]], [neg_bbox_min_row[i]], [neg_bbox_min_col[i]], [neg_bbox_max_row[i]], [neg_bbox_max_col[i]], [neg_area_bbox[i]], [neg_cen_bbox_row[i]], [neg_cen_bbox_col[i]],[neg_flux[i]], [neg_min_flux[i]], [neg_mean_flux[i]], [neg_max_flux[i]]
    neg_store_number += 1

# Do the same thing for the positive fragment data
[pos_dates, pos_latitudes, pos_longitudes, pos_area, pos_eccentricity, pos_bbox_min_row, pos_bbox_min_col, pos_bbox_max_row, pos_bbox_max_col, pos_area_bbox, pos_cen_bbox_row, pos_cen_bbox_col, pos_flux, pos_min_flux, pos_mean_flux, pos_max_flux] = fragment_file_reader(pos_files[0])

for i in range(len(pos_dates)):
    pos_store[str(pos_store_number)] = [pos_dates[i]], [pos_latitudes[i]], [pos_longitudes[i]], [pos_area[i]], [pos_eccentricity[i]], [pos_bbox_min_row[i]], [pos_bbox_min_col[i]], [pos_bbox_max_row[i]], [pos_bbox_max_col[i]], [pos_area_bbox[i]], [pos_cen_bbox_row[i]], [pos_cen_bbox_col[i]], [pos_flux[i]], [pos_min_flux[i]], [pos_mean_flux[i]], [pos_max_flux[i]]
    pos_store_number += 1


# For each subsequent image (using the negative file number to keep track, but the positive one is the same)
for image in range(1, len(neg_files)):
    print(image)
    # Get fragments from new image
    [neg_dates_new, neg_latitudes_new, neg_longitudes_new, neg_area_new, neg_eccentricity_new, neg_bbox_min_row_new, neg_bbox_min_col_new, neg_bbox_max_row_new, neg_bbox_max_col_new, neg_area_bbox_new, neg_cen_bbox_row_new, neg_cen_bbox_col_new, neg_flux_new, neg_min_flux_new,neg_mean_flux_new, neg_max_flux_new] = fragment_file_reader(neg_files[image])
    # Get timestamp of old image to use to search the fragment store
    neg_date_old = fragment_file_reader(neg_files[image-1])[0][0]
    
    # Get fragments from new image
    [pos_dates_new, pos_latitudes_new, pos_longitudes_new, pos_area_new, pos_eccentricity_new, pos_bbox_min_row_new, pos_bbox_min_col_new, pos_bbox_max_row_new, pos_bbox_max_col_new, pos_area_bbox_new, pos_cen_bbox_row_new, pos_cen_bbox_col_new, pos_flux_new, pos_min_flux_new, pos_mean_flux_new, pos_max_flux_new] = fragment_file_reader(pos_files[image])
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
            neg_store[append_key][5].append(neg_bbox_min_row_new[fragment])
            neg_store[append_key][6].append(neg_bbox_min_col_new[fragment])
            neg_store[append_key][7].append(neg_bbox_max_row_new[fragment])
            neg_store[append_key][8].append(neg_bbox_max_col_new[fragment])
            neg_store[append_key][9].append(neg_area_bbox_new[fragment])
            neg_store[append_key][10].append(neg_cen_bbox_row_new[fragment])
            neg_store[append_key][11].append(neg_cen_bbox_col_new[fragment])
            neg_store[append_key][12].append(neg_flux_new[fragment])
            neg_store[append_key][13].append(neg_min_flux_new[fragment])
            neg_store[append_key][14].append(neg_mean_flux_new[fragment])
            neg_store[append_key][15].append(neg_max_flux_new[fragment])

            # And remove that fragment from the 'old' list as only one new can link to one old
            if len(neg_latitudes_old) > 1:
                del neg_key_list[index]
                del neg_latitudes_old[index]
                del neg_longitudes_old[index]

            else:
                break
        
        else:
            # If no old fragments are close enough, create a new record for this new fragment
            neg_store[str(neg_store_number)] = [neg_dates_new[fragment]], [neg_latitudes_new[fragment]], [neg_longitudes_new[fragment]], [neg_area_new[fragment]], [neg_eccentricity_new[fragment]], [neg_bbox_min_row_new[fragment]], [neg_bbox_min_col_new[fragment]], [neg_bbox_max_row_new[fragment]], [neg_bbox_max_col_new[fragment]],[neg_area_bbox_new[fragment]], [neg_cen_bbox_row_new[fragment]],[neg_cen_bbox_col_new[fragment]], [neg_flux_new[fragment]],[neg_min_flux_new[fragment]], [neg_mean_flux_new[fragment]],[neg_max_flux_new[fragment]]
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
            pos_store[append_key][5].append(pos_bbox_min_row_new[fragment])
            pos_store[append_key][6].append(pos_bbox_min_col_new[fragment])
            pos_store[append_key][7].append(pos_bbox_max_row_new[fragment])
            pos_store[append_key][8].append(pos_bbox_max_col_new[fragment])
            pos_store[append_key][9].append(pos_area_bbox_new[fragment])
            pos_store[append_key][10].append(pos_cen_bbox_row_new[fragment])
            pos_store[append_key][11].append(pos_cen_bbox_col_new[fragment])
            pos_store[append_key][12].append(pos_flux_new[fragment])
            pos_store[append_key][13].append(pos_min_flux_new[fragment])
            pos_store[append_key][14].append(pos_mean_flux_new[fragment])
            pos_store[append_key][15].append(pos_max_flux_new[fragment])



            # And remove that fragment from the 'old' list as only one new can link to one old
            if len(pos_latitudes_old) > 1:
                del pos_key_list[index]
                del pos_latitudes_old[index]
                del pos_longitudes_old[index]

            else:
                break
        
        else:
            # If no old fragments are close enough, create a new record for this new fragment
            pos_store[str(pos_store_number)] = [pos_dates_new[fragment]], [pos_latitudes_new[fragment]], [pos_longitudes_new[fragment]], [pos_area_new[fragment]], [pos_eccentricity_new[fragment]], [pos_bbox_min_row_new[fragment]], [pos_bbox_min_col_new[fragment]], [pos_bbox_max_row_new[fragment]], [pos_bbox_max_col_new[fragment]], [pos_area_bbox_new[fragment]], [pos_cen_bbox_row_new[fragment]], [pos_cen_bbox_col_new[fragment]], [pos_flux_new[fragment]], [pos_min_flux_new[fragment]], [pos_mean_flux_new[fragment]], [pos_max_flux_new[fragment]]
            pos_store_number += 1

# Save the fragment store objects to disk for later analysis
#output = open('/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/pickles/negative_fragment_store.pkl', 'wb')
output = open('/Users/fraser/Github/MagneticFragmentationOutput/fragment_properties/negative_store.pkl', 'wb')
pickle.dump(neg_store, output)
output.close()
#output = open('/Users/dina/Dropbox/PhD/phd/work/year3/codes_yr3/mag_flux_project/MagneticFragmentation2/output/pickles/positive_fragment_store.pkl', 'wb')
output = open('/Users/fraser/Github/MagneticFragmentationOutput/fragment_properties/positive_store.pkl', 'wb')
pickle.dump(pos_store, output)
output.close()

