
# coding: utf-8

# In[1]:

def write_props(props, polarity, image_num, image_date):
    filename = '{num:04d}'.format(num = image_num)+polarity+'.txt'
    f = open(filename, 'w')
    for region in props:
        x = region.centroid[1]
        y = region.centroid[0]
        f.write('{0}, {1:01.1f}, {2:01.1f}\n'.format(image_date, x, y))
    f.close()
    

