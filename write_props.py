
# coding: utf-8

# In[1]:

def write_props(props, polarity, image_num, image_date, submap):
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    from sunpy.coordinates import frames
    
    filename = '{num:04d}'.format(num = image_num)+polarity+'.txt'
    f = open(filename, 'w')
    for region in props:
        arcsecs_coord = submap.pixel_to_world(region.centroid[1] * u.pix, region.centroid[0] * u.pix)
        latlong_coord = arcsecs_coord.transform_to(frames.HeliographicStonyhurst)
        area = region.area
        f.write('{0}, {1:01.1f}, {2:01.1f}\n'.format(image_date, latlong_coord.lat.value, latlong_coord.lon.value, area))
    f.close()

