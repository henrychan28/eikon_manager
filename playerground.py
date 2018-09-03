import multiprocessing
from multiprocessing import Pool
import numpy as np
import time


def tester(num):
    for i in range(1000000):
        np.cos(num)
    return None


if __name__ == '__main__':

    starttime1 = time.time()
    pool_size = multiprocessing.cpu_count()
    print(pool_size)
    pool = multiprocessing.Pool(processes=pool_size)
    pool_outputs = pool.map(tester, range(4))
    pool.close()
    pool.join()
    endtime1 = time.time()
    timetaken = endtime1 - starttime1

    starttime2 = time.time()
    for i in range(4):
        tester(i)
    endtime2 = time.time()
    timetaken2 = endtime2 - starttime2

    print('The time taken with multiple processes:', timetaken)
    print('The time taken the usual way:', timetaken2)