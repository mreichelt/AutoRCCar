import numpy as np


def find_subarray(array, subarray):
    arr = [x for x in range(len(array)) if array[x:x + len(subarray)] == subarray]
    if len(arr) == 0:
        return -1
    return arr[0]


def rolling_window(array, window):
    if len(array) < window:
        return None
    shape = array.shape[:-1] + (array.shape[-1] - window + 1, window)
    strides = array.strides + (array.strides[-1],)
    return np.lib.stride_tricks.as_strided(array, shape=shape, strides=strides)


def find_subarray_np(array, subarray):
    temp = rolling_window(array, len(subarray))
    if temp is None:
        return None
    result = np.where(np.all(temp == subarray, axis=1))[0]
    return result[0] if len(result) > 0 else None
