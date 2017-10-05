
# coding: utf-8

# In[ ]:

def split_pol_thresh(data, threshold, polarity):

    # This function takes the input data along with a threshold, and returns
    # the same data with everything below the threshold removed. In addition,
    # if the data is negative, it is inverted so that the following routines
    # can be run on positive and negative data interchangeably.

    import numpy as np

    # Create a copy of the data
    output = np.copy(data)

    # Check polarity and invert if necessary
    if polarity == 'pos':
        pass
    elif polarity == 'neg':
        output = output * (-1)
    else:
        print('Polarity must be pos or neg.')

    # Set data below threshold to zero
    output[output < threshold] = 0

    return output

