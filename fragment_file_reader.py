
# coding: utf-8

# In[ ]:

def fragment_file_reader(file):
    
    import csv
    from datetime import datetime
    
    # This function takes a file containing fragment data for a single
    # image and reads out the data into arrays of the correct format
    
    # Initialize variables for dates, latitudes, and longitudes
    dates = []
    latitudes = []
    longitudes = []

    # Open file and return arrays for dates (as datetime), latitudes (as float) and longitudes (as float)
    with open(file, 'r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        for row in filereader:
            dates.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
            latitudes.append(float(row[1]))
            longitudes.append(float(row[2]))
    
    return [dates, latitudes, longitudes]

