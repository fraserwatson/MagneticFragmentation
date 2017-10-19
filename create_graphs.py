
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
get_ipython().magic('matplotlib inline')
plt.rcParams['figure.figsize'] = 12, 10
plt.rcParams.update({'font.size': 12})
import csv
from datetime import datetime

posnegcounter = 0
posdates = []
posnums = []
posareas = []
posfluxes = []
negdates = []
negnums = []
negareas = []
negfluxes = []

# Open file and return arrays for dates (as datetime), latitudes (as float) and longitudes (as float)
with open('/Users/fraser/Github/MagneticFragmentationOutput/fragment_properties/AR12010/bulk_props.txt', 'r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    for row in filereader:
        if posnegcounter % 2 == 0:
            posdates.append(datetime.strptime(row[0][0:19], '%Y-%m-%d %H:%M:%S'))
            posnums.append(float(row[1]))
            posareas.append(float(row[2]))
            posfluxes.append(float(row[3]))
        else:
            negdates.append(datetime.strptime(row[0][0:19], '%Y-%m-%d %H:%M:%S'))
            negnums.append(float(row[1]))
            negareas.append(float(row[2]))
            negfluxes.append(float(row[3]))
        posnegcounter += 1


# In[2]:


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(posdates, posnums)
ax.plot(negdates, negnums)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

# rotate and align the tick labels so they look better
fig.autofmt_xdate(rotation=90)

ax.set_xlabel('Time')
ax.set_ylabel('Number of fragments')


# In[5]:


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(posdates, posareas)
ax.plot(negdates, negareas)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

# rotate and align the tick labels so they look better
fig.autofmt_xdate(rotation=90)

ax.set_xlabel('Time')
ax.set_ylabel('Total fragment area (square cm)')


# In[6]:


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(posdates, posfluxes)
ax.plot(negdates, [abs(number) for number in negfluxes])

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

# rotate and align the tick labels so they look better
fig.autofmt_xdate(rotation=90)

ax.set_xlabel('Time')
ax.set_ylabel('Total flux (Maxwells)')

