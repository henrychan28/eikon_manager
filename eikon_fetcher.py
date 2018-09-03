import multiprocessing
from multiprocessing import Pool
import pandas as pd
import concurrent.futures

from eikon_manager_builder import build_eikon_manager
from helper import timer

def get_daily_timeseries_wrapper(args):
    return build_eikon_manager().get_timeseries(*args)

@timer
def get_daily_timeseries_bucket(syms, start_date, end_date, interval, GMT=8):

    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size)
    args = [(sym, start_date, end_date, interval, GMT) for sym in syms]
    pool_outputs = pool.map(get_daily_timeseries_wrapper, args)
    pool.close()
    pool.join()

    '''
    with concurrent.futures.ThreadPoolExecutor(max_workers=) as executor:
        args = [(sym, start_date, end_date, interval, GMT) for sym in syms]
        futures = {executor.submit(get_daily_timeseries_wrapper, arg): arg for arg in args}
        result = [future.result() for future in concurrent.futures.as_completed(futures)]
    '''
    return None
