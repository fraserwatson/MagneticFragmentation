
# coding: utf-8

# In[3]:

def find_closest_fragment(lat_new, long_new, lats_old, longs_old, time_delta):
    
    # Given a new coordinate, a set of old coordinates, and a timedelta, this function find the closest
    # coordinate in the old set to the new one back-rotated by timedelta
    
    from rotate_long import rotate_long
    import numpy as np
    
    # Rotate new coordinate back to the time of the old image
    [lat_rot, long_rot] = rotate_long(lat_new, long_new, -time_delta)
    
    # Calculate distance from each of the old fragments
    distances = []
    for coord in range(len(lats_old)):
        new_coord = np.array([lat_rot, long_rot])
        old_coord = np.array([lats_old[coord], longs_old[coord]])
        # Calculate the Euclidean distance between the old coordinate and the back-rotated new coordinate
        distances.append(np.linalg.norm(new_coord - old_coord))
    
    # Convert to numpy array for next operation
    distances = np.array(distances)
    
    # Return the index of the minimum distance i.e. the closest fragment
    return [np.amin(distances), distances.argmin()]

