
# coding: utf-8

# In[ ]:


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
    bbox_min_row = []
    bbox_min_col = []
    bbox_max_row = []
    bbox_max_col = []
    area_bbox = []
    cen_bbox_row = []
    cen_bbox_col = []
    flux = []
    min_flux = []
    mean_flux = []
    max_flux = []

    # Open file and return arrays for dates (as datetime), latitudes (as float) and longitudes (as float)
    with open(file, 'r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        for row in filereader:
            dates.append(datetime.strptime(row[0][0:19], '%Y-%m-%d %H:%M:%S'))
            latitudes.append(float(row[1]))
            longitudes.append(float(row[2]))
            area.append(float(row[3]))
            eccentricity.append(float(row[4]))
            bbox_min_row.append(int(row[5]))
            bbox_min_col.append(int(row[6]))
            bbox_max_row.append(int(row[7]))
            bbox_max_col.append(int(row[8]))
            area_bbox.append(int(row[9]))
            cen_bbox_row.append(float(row[10]))
            cen_bbox_col.append(float(row[11]))
            flux.append(float(row[12]))
            min_flux.append(float(row[13]))
            mean_flux.append(float(row[14]))
            max_flux.append(float(row[15]))
    
    return [dates, latitudes, longitudes, area, eccentricity, bbox_min_row, bbox_min_col, bbox_max_row, 
            bbox_max_col, area_bbox, cen_bbox_row, cen_bbox_col, flux, min_flux,
            mean_flux, max_flux]

