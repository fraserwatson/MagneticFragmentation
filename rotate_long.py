
# coding: utf-8

# In[1]:


def rotate_long(lat, long, timestep):
    
    # Converts a solar longitude into a new 
    # longitude at a different time given solar rotation
    # timestep is the time delta, in earth days
    
    import numpy as np
    
    # Convert latitude into radians
    latrad = np.deg2rad(lat)
    
    # Calculate rotation in given number of days
    rotation = 0.000001 * timestep * (2.894 - (0.428 * np.power((np.sin(latrad)), 2)) - (0.37 * np.power(np.sin(latrad), 4))) * 24 * np.rad2deg(3600)   
    
    newlat = lat
    newlong = long + rotation
    
    return [newlat, newlong]

