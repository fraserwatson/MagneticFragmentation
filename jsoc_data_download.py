
# coding: utf-8

# Import the drms module and creating a drms. Provide an email address and turn on status messages by enabling the verbose flag.

# In[ ]:


import drms
c = drms.Client(email='k.loumou.1@research.gla.ac.uk', verbose=True)


# In[ ]:


import os
out_dir = "/Users/dina/Desktop/test"


# Define an export request. In order to obtain FITS files that include keyword data in their headers, we then need to use protocol='fits' when submitting the request using Client.export()

# In[ ]:


ds = 'hmi.M_45s[2014.04.09_08:07:30_TAI/7h]{magnetogram}'
r = c.export(ds, method='url', protocol='fits')
r


# Download the data

# In[ ]:


r.download(out_dir)

