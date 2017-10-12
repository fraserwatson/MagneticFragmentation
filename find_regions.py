
# coding: utf-8

# In[1]:


def find_regions(data):

    import numpy as np

    # Flatten frame into a 1d array
    flat = np.ndarray.flatten(data, 'C')
    # Get the index sort of field values
    indexorder = np.argsort(flat)[::-1]
    # Count how many pixels are above the threshold value
    num_pixels = np.count_nonzero(flat)
    # Truncate the index array to that length
    indexorder = indexorder[0:num_pixels]

    # Set up region frame
    region_frame = np.zeros(data.shape)

    # Initialise region number and data shape
    num_regions = 0
    rows, cols = data.shape

    # For each pixel to be checked...
    for index in indexorder:

        # ... convert back to 2D indices
        row = index // cols
        col = index % cols

        # Get surrounding region values
        regtl = region_frame[row-1, col-1]
        regtm = region_frame[row-1, col]
        regtr = region_frame[row-1, col+1]
        regcl = region_frame[row, col-1]
        regcr = region_frame[row, col+1]
        regbl = region_frame[row+1, col-1]
        regbm = region_frame[row+1, col]
        regbr = region_frame[row+1, col+1]

        # Create region array
        reg_values = [regtl, regtm, regtr, regcl, regcr, regbl, regbm, regbr]

        # Assign pixel to region by first checking if any surronding pixels
        # belong to a region
        if max(reg_values) == 0:
            num_regions += 1
            region_frame[row, col] = num_regions
        else:
            reg_values.sort()
            reg_values = np.trim_zeros(reg_values)
            region_frame[row, col] = min(reg_values)
            
    # The region_frame array is padded by zeros to a width of one pixel. Return the array without that padding.
    return region_frame[1:-1, 1:-1], num_regions

