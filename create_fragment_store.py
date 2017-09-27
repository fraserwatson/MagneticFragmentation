
# coding: utf-8

# In[1]:

from os import listdir
from fragment_file_reader import fragment_file_reader
from datetime import datetime
from find_closest_fragment import find_closest_fragment

# What directory are the text files stored in?
basedir = '/Users/fraser/Github/MagneticFragmentation/fragment_properties/'

# Get list of files to use
files = [basedir + i for i in listdir(basedir)]

# Split the list into two lists, one for positive fragments and one for negative fragments
neg_files = [s for s in files if 'n.' in s]
pos_files = [s for s in files if 'p.' in s]

# Set up the individual store dictionaries
neg_store = {}
neg_store_number = 0
pos_store = {}
pos_store_number = 0

# For the first image, there is no previous timestep to compare against. All fragments are put into the store.
[neg_dates, neg_latitudes, neg_longitudes] = fragment_file_reader(neg_files[0])

for i in range(len(neg_dates)):
    neg_store[str(neg_store_number)] = [neg_dates[i]], [neg_latitudes[i]], [neg_longitudes[i]]
    neg_store_number += 1

[pos_dates, pos_latitudes, pos_longitudes] = fragment_file_reader(pos_files[0])

for i in range(len(pos_dates)):
    pos_store[str(pos_store_number)] = [pos_dates[i]], [pos_latitudes[i]], [pos_longitudes[i]]
    pos_store_number += 1

# For each subsequent image (using the negative file number to keep track, but the positive one is the same)
for image in range(1, len(neg_files)):
    # Get fragments from new image
    [neg_dates_new, neg_latitudes_new, neg_longitudes_new] = fragment_file_reader(neg_files[image])
    # Get timestamp of old image to use to search the fragment store
    neg_date_old = fragment_file_reader(neg_files[image-1])[0][0]
    # Get fragments from new image
    [pos_dates_new, pos_latitudes_new, pos_longitudes_new] = fragment_file_reader(pos_files[image])
    # Get timestamp of old image to use to search the fragment store
    pos_date_old = fragment_file_reader(pos_files[image-1])[0][0]
    
    # Search the region store and pull out all fragments that are in the old image
    # Reset the negative key list and old lat long lists
    neg_key_list = []
    neg_latitudes_old = []
    neg_longitudes_old = []
    for key in neg_store:
        if neg_store[key][0][0] == neg_date_old:
            # Find which keys in the dictionary contain fragments from the previous image and get their key, lat, and long
            neg_key_list.append(key)
            neg_latitudes_old.append(neg_store[key][1])
            neg_longitudes_old.append(neg_store[key][2])
    
    # Reset the positive key list and old lat long lists
    pos_key_list = []
    pos_latitudes_old = []
    pos_longitudes_old = []
    for key in pos_store:
        if pos_store[key][0][0] == pos_date_old:
            # Find which keys in the dictionary contain fragments from the previous image and get their key, lat, and long
            pos_key_list.append(key)
            pos_latitudes_old.append(pos_store[key][1])
            pos_longitudes_old.append(pos_store[key][2])
    
    # Calculate the time difference between the old and new images to remove solar rotation
    time_delta = (neg_dates_new[0] - neg_date_old).seconds/86400
    # For each fragment in the new image, find the closest one in space in the old image
    for fragment in range(len(neg_latitudes_new)):
        index = find_closest_fragment(neg_latitudes_new[fragment], neg_longitudes_new[fragment], neg_latitudes_old, neg_longitudes_old, time_delta)


# In[2]:

print(index)

