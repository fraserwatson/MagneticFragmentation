
# coding: utf-8

# In[11]:


def fragment_file_reader(file):
    
    # This function takes a file containing fragment data for a single
    # image and reads out the data into arrays of the correct format.
    # If the write_props function is changed to add more properties to the files,
    # this function has to be changed to read those files.
    
    import csv
    from datetime import datetime

    # Initialize variables for dates, latitudes, and longitudes
    dates = []
    latitudes = []
    longitudes = []
    area = []
    eccentricity = []
    bbox_x_min = []
    bbox_y_min = []
    bbox_x_max = []
    bbox_y_max = []
    area_bbox = []
    cen_bbox_y = []
    cen_bbox_x = []
    flux = []
    min_flux = []
    mean_flux = []
    max_flux = []
    blos = []
    min_blos = []
    mean_blos = []
    max_blos = []
    w_cen_lat = []
    w_cen_lng = []
    ori = []
    major= []
    minor = []
    cen_y=[]
    cen_x=[]
    wcen_y=[]
    wcen_x=[]
    
    

    # Open file and return arrays for dates (as datetime), latitudes (as float) and longitudes (as float)
    with open(file, 'r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        for row in filereader:
            dates.append(datetime.strptime(row[0][0:19], '%Y-%m-%d %H:%M:%S'))
            latitudes.append(float(row[1]))
            longitudes.append(float(row[2]))
            area.append(float(row[3]))
            eccentricity.append(float(row[4]))
            bbox_x_min.append(float(row[5]))
            bbox_y_min.append(float(row[6]))
            bbox_x_max.append(float(row[7]))
            bbox_y_max.append(float(row[8]))
            area_bbox.append(int(row[9]))
            cen_bbox_y.append(float(row[10]))
            cen_bbox_x.append(float(row[11]))
            flux.append(float(row[12]))
            min_flux.append(float(row[13]))
            mean_flux.append(float(row[14]))
            max_flux.append(float(row[15]))
            blos.append(float(row[16]))
            min_blos.append(float(row[17]))
            mean_blos.append(float(row[18]))
            max_blos.append(float(row[19]))
            w_cen_lat.append(float(row[20]))
            w_cen_lng.append(float(row[21]))
            ori.append(float(row[22]))
            major.append(float(row[23]))
            minor.append(float(row[24]))
            cen_y.append(float(row[25]))
            cen_x.append(float(row[26]))
            wcen_y.append(float(row[27]))
            wcen_x.append(float(row[28]))
                       
    return [dates, latitudes, longitudes, area, eccentricity,
            bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max, 
            area_bbox, cen_bbox_x, cen_bbox_y, flux, min_flux, 
            mean_flux, max_flux, blos, min_blos, mean_blos, max_blos, w_cen_lat, w_cen_lng,
            ori, major, minor, cen_y, cen_x, wcen_y, wcen_x]

