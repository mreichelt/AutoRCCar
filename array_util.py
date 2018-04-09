def find_subarray(array, subarray):
    arr = [x for x in range(len(array)) if array[x:x + len(subarray)] == subarray]
    if len(arr) == 0:
        return -1
    return arr[0]
