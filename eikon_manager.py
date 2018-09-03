from datetime import timedelta
import pandas as pd
from eikon import EikonError

import helper


class EikonManager(object):
    def __init__(self, key, eikon):
        self.ek = eikon
        self._setup_eikon(key)

    def _setup_eikon(self, key):
        self.ek.set_app_key(key)

    def get_timeseries(self, sym, start_date, end_date, interval, GMT=8):
        dates = helper.get_dates(start_date, end_date)
        outputs = [self.get_daily_timeseries(sym, date, interval, GMT) for date in dates]
        return pd.concat(outputs)

    def get_daily_timeseries(self, sym, date, interval, GMT):
        print('sym: {0} | date: {1} '.format(sym, date))
        start_time, end_time = helper.get_local_time(date, GMT)
        if interval != 'tick':
            try:
                data = self.ek.get_timeseries(sym,
                                              start_date=start_time,
                                              end_date=end_time,
                                              interval=interval)
                data = data.reset_index()
                data['Date'] = data['Date'] + timedelta(hours=GMT)
                data['sym'] = sym
                return data
            except EikonError:
                return pd.DataFrame()
            except Exception:
                raise
        else:
            return self._get_daily_tick_timeseries(sym, start_time, end_time, GMT)

    def _get_daily_tick_timeseries(self, sym, start_time, end_time, GMT):
        # Eikon platform has a limit of retrieving 50,000 data at a time.
        # This function overcome the limitation by iteratively retrieving
        # desired data.
        frame = pd.DataFrame()
        while True:
            try:
                new_frame = self.ek.get_timeseries(sym,
                                                   start_date=start_time,
                                                   end_date=end_time,
                                                   interval="tick")
                new_frame = new_frame.reset_index()
                time = new_frame.iloc[0]['Date'] - timedelta(seconds=1)
                end_time = time.strftime('%Y-%m-%dT%H:%M:%S')
                new_frame['Date'] = new_frame['Date'] + timedelta(hours=GMT)
                new_frame['sym'] = sym
                frame = frame.append(new_frame, ignore_index=True)
            except EikonError:
                break
            except Exception:
                raise

        return frame
