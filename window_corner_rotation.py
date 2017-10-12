
# coding: utf-8

# In[ ]:


def window_corner_rotation(bl_stonyhurst, tr_stonyhurst, timedelta, time):
    
    from rotate_long import rotate_long
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    from sunpy.coordinates import frames
    
    # Bottom left corner
    [bl_rot_lat, bl_rot_lon] = rotate_long(bl_stonyhurst.lat.value, bl_stonyhurst.lon.value, timedelta)
    bl_coord = SkyCoord(bl_rot_lon*u.deg, bl_rot_lat*u.deg, frame=frames.HeliographicStonyhurst, obstime=time)
    bl_arcsecs = bl_coord.transform_to(frames.Helioprojective)
    
    # Top right corner
    [tr_rot_lat, tr_rot_lon] = rotate_long(tr_stonyhurst.lat.value, tr_stonyhurst.lon.value, timedelta)
    tr_coord = SkyCoord(tr_rot_lon*u.deg, tr_rot_lat*u.deg, frame=frames.HeliographicStonyhurst, obstime=time)
    tr_arcsecs = tr_coord.transform_to(frames.Helioprojective)
    
    return [bl_arcsecs, tr_arcsecs]

