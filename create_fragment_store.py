
# coding: utf-8

# In[3]:

# The datetime library gives us an easy way to manage dates and times in the code
from datetime import datetime
# Pickle lets us save objects to disk that can be loaded back into other python routines later on
import pickle
from os import listdir
from fragment_file_reader import fragment_file_reader
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

# For each fragment from the first image, create a new fragment record in the dictionary. Keys start at '0' and
# go up one every time a new fragment is added
for i in range(len(neg_dates)):
    neg_store[str(neg_store_number)] = [neg_dates[i]], [neg_latitudes[i]], [neg_longitudes[i]]
    neg_store_number += 1

# Do the same thing for the positive fragment data
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
    time_delta = (neg_dates_new[0] - neg_date_old).seconds/86400
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

            # And remove that fragment from the 'old' list as only one new can link to one old
            if len(neg_latitudes_old) > 1:
                del neg_key_list[index]
                del neg_latitudes_old[index]
                del neg_longitudes_old[index]
            else:
                break
        
        else:
            # If no old fragments are close enough, create a new record for this new fragment
            neg_store[str(neg_store_number)] = [neg_dates_new[fragment]], [neg_latitudes_new[fragment]], [neg_longitudes_new[fragment]]
            neg_store_number += 1

    # Calculate the time difference between the old and new images to remove solar rotation
    time_delta = (pos_dates_new[0] - pos_date_old).seconds/86400
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

            # And remove that fragment from the 'old' list as only one new can link to one old
            if len(pos_latitudes_old) > 1:
                del pos_key_list[index]
                del pos_latitudes_old[index]
                del pos_longitudes_old[index]
            else:
                break
        
        else:
            # If no old fragments are close enough, create a new record for this new fragment
            pos_store[str(pos_store_number)] = [pos_dates_new[fragment]], [pos_latitudes_new[fragment]], [pos_longitudes_new[fragment]]
            pos_store_number += 1

# Save the fragment store objects to disk for later analysis
output = open('negative_fragment_store.pkl', 'wb')
pickle.dump(neg_store, output)
output.close()
output = open('positive_fragment_store.pkl', 'wb')
pickle.dump(pos_store, output)
output.close()


# In[2]:

neg_store

