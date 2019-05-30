import time

def days():
    # returns the number of days since the epoch
    return time.time() // (60 * 60 * 24)
