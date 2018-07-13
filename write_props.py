
# coding: utf-8

# In[7]:


def write_props(props, polarity, image_num, image_date, submap, act_region, thres, main):
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    from sunpy.coordinates import frames
    import numpy as np
    
    propspath= main + act_region + '_' + str(thres) + 'G_fragment_properties_v2/'
#     bulk_path = main + 'bulk_props_'+ act_region +  '_' + str(thres) +'G.txt'

    # Set up variables for bulk props
    total_frags = 0
    total_area = 0
    total_flux = 0
    
    # Create filename using the image_date and polarity
    
    filename = propspath + '{0}'.format(image_date.strftime('%Y%m%d_%H%M%S'))+'_'+polarity+'.txt'####<-------
     #------- COMMENT OUT THIS LINE TOO IF ONLY INTERESTED IN BULK PROPERTIES!!!!
    
    # Open filename for writing
    f = open(filename, 'w')####<-------------- COMMENT OUT THIS LINE TOO IF I ONLY INTERESTED IN BULK PROPERTIES!!!!
    for region in props:
        # Check to see if the area of the fragment is 12 pixels or larger
        if region.area >= 12:
            # Add one new fragment to the bulk fragment properties
            total_frags += 1
            # Get the pixel coordinates from the region.centroid and cast them as
            # pixels in astropy units. Then, use the sunpy submap to convert those
            # pixel coordinates to image coordinates (x-arcsecs and y-arcsecs)
            # The numbers here seem inverted because skimage.measure.regionprops gives properties 
            #as (row,col,) which means (y,x)
            arcsecs_coord = submap.pixel_to_world(region.centroid[1] * u.pix,
                                                  region.centroid[0] * u.pix)
            # Now convert the coordinates to Heliographic latitude and longitude (degrees) as
            # that is what we need to rotate coordinates in time later on
            latlong_coord = arcsecs_coord.transform_to(frames.HeliographicStonyhurst)
            # Record the area in sqcm (1 pixel at disk centre is 1.31 million square km) deprojected to disk centre
            area = region.area * 1.31 * np.power(10, 16) / (np.cos(np.deg2rad(latlong_coord.lat.value)) * np.cos(np.deg2rad(latlong_coord.lon.value)))
            total_area += area
            # Record the eccentricity of each fragment
            # position {4} in the write command
            ecc=region.eccentricity

            # Record the bounding box of each fragment
            # The bounding box is an array. It is much easier to save each element of the array seperately.
            # min col (xmin) position {5} in the write command
            # min row (ymin) position {6} in the write command
            # max col (xmax) position {7} in the write command 
            # max row (ymax) position {8} in the write command
            # Get the pixel coordinates from the region.bbox and cast them as
            # pixels in astropy units. Then, use the sunpy submap to convert those
            # pixel coordinates to image coordinates (x-arcsecs and y-arcsecs)
            arcsecs_bbox_min_coords = submap.pixel_to_world(region.bbox[1] * u.pix,
                                                            region.bbox[0] * u.pix)
            # Now convert the coordinates to Heliographic latitude and longitude (degrees) as
            # that is what we need to rotate coordinates in time later on
            frag_bbox_xy_min=arcsecs_bbox_min_coords.transform_to(frames.HeliographicStonyhurst)
            
            arcsecs_bbox_max_coords = submap.pixel_to_world(region.bbox[3] * u.pix,
                                                  region.bbox[2] * u.pix)
            frag_bbox_xy_max=arcsecs_bbox_max_coords.transform_to(frames.HeliographicStonyhurst)

            # Record the area of the bounding box of each fragment
            # The bbox_area source code has a bug, gives out the area of whole submap, don't use!
            # position {9} in the write command
            area_bbox=region.image.size

            # Record the centroid of the bounding box of each fragment
            # row of bbox centroid position {10} in the write command
            # col of bbox centroid position {11} in the write command
            cen_bbox_y=region.local_centroid[0]
            cen_bbox_x=region.local_centroid[1]

            # Record the flux of each label in Maxwells . Its sum is the total flux of the pixels inside the bounding box
            # If some of these pixels correspong to the opposite polarity, we get back 0s.
            #Intensity_image gives the value of each pixel inside the bounding box
            # position {12} in the write command
            flux = (np.sum(region.intensity_image) / region.area) * area
            total_flux += flux

            # Record the min flux of each label in Maxwells
            # position {13} in the write command
            min_flux= (np.sum(region.min_intensity) / region.area) * area

            # Record the mean flux of each label in Maxwells
            # position {14} in the write command
            mean_flux= (np.sum(region.mean_intensity) / region.area) * area

            # Record the max flux of each label in Maxwells
            # position {15} in the write command
            max_flux= (np.sum(region.max_intensity) / region.area) * area
            
            # Record the magnetic field value of each fragment/label in Gauss
            # position {16} in the write command
            blos= np.sum(region.intensity_image) / region.area
            
            # Record the min magnetic field value of each fragment/label in Gauss
            # position {17} in the write command
            min_blos= np.sum(region.min_intensity) / region.area
            
            # Record the mean flux of each label in Maxwells
            # position {18} in the write command
            mean_blos= np.sum(region.mean_intensity) / region.area

            # Record the max flux of each label in Maxwells
            # position {19} in the write command
            max_blos= np.sum(region.max_intensity) / region.area
            
            #Record weighted_local_centroid: Centroid coordinate tuple (row, col), 
            #relative to region bounding box, weighted with intensity image.
            # y position {20} in the write command
            # x position {21} in the write command
            arcsecs_wc = submap.pixel_to_world(region.weighted_centroid[1] * u.pix,
                                               region.weighted_centroid[0] * u.pix)
            wc_xy_coord = arcsecs_wc.transform_to(frames.HeliographicStonyhurst) 
            
            #Record orientation angle
            #position {22} in the write command
            ori=region.orientation
            
            #Record major axis length of the fitted ellipse
             #position {23} in the write command
            major=region.major_axis_length
            
            #Record minor axis length of the fitted ellipse
             #position {24} in the write command
            minor=region.minor_axis_length
            
            
            
            

            #Write the data to the file
            f.write('{0}, {1:01.1f}, {2:01.1f}, {3}, {4:.1f}, {5}, {6}, {7}, {8}, {9}, {10:.2f}, {11:.2f}, {12:.1f}, {13:.1f},{14:.1f}, {15:.1f}, {16:.1f}, {17:.1f}, {18:.1f}, {19:.1f}, {20:.1f}, {21:.1f}, {22:.1f}, {23:.1f}, {24:.1f}\n'.format(image_date,
                                                         latlong_coord.lat.value, latlong_coord.lon.value,
                                                         area,ecc,
                                                         frag_bbox_xy_min.lon.value, frag_bbox_xy_min.lat.value,
                                                         frag_bbox_xy_max.lon.value, frag_bbox_xy_max.lat.value,
                                                         area_bbox, cen_bbox_y, cen_bbox_x,
                                                         flux, min_flux, mean_flux, max_flux, blos, min_blos, 
                                                         mean_blos, max_blos,
                                                         wc_xy_coord.lat.value, wc_xy_coord.lon.value,
                                                         ori, major, minor))  #\n means "new line"
            

    # Close the file
    f.close()
    
#     # Open bulk properties file for writing. I need this to make plots like in Fraser's thesis.
#     g = open(bulk_path, 'a')
#     g.write('{0}, {1:4.0f}, {2:5.0f}, {3:8.0f}\n'.format(image_date, total_frags, total_area, total_flux))
#     g.close()

