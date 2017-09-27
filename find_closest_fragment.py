
# coding: utf-8

# In[ ]:

def find_closest_fragment(lat_new, long_new, lats_old, longs_old, time_delta):
    
    from rotate_long import rotate_long
    import numpy as np
    
    # Rotate new coordinate back to the time of the old image
    [lat_rot, long_rot] = rotate_long(lat_new, long_new, -time_delta)
    
    # Calculate distance from each of the old fragments
    distances = []
    for coord in range(len(lats_old)):
        new_coord = np.array([lat_rot, long_rot])
        old_coord = np.array([lats_old[coord], longs_old[coord]])
        distances.append(np.linalg.norm(new_coord - old_coord))
    
    return distances

