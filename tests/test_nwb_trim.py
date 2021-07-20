import datetime
from nwb_tools import nwb_trim
import numpy as np
# import os
from pynwb import NWBFile, NWBHDF5IO, TimeSeries


nwbfile = NWBFile(
    session_description='session_description',
    identifier='identifier',
    session_start_time=datetime.datetime.now(datetime.timezone.utc),
)

ts = TimeSeries(
    name='TimeSeries',
    data=np.arange(100000).reshape(10000, 10),
    unit='unit',
    rate=1.
)

nwbfile.add_acquisition(ts)

filename_in = 'nwbfile.nwb'
filename_out = 'nwbfile_trim.nwb'

try:
    with NWBHDF5IO(filename_in, 'w') as io:
        io.write(nwbfile)

    nwb_trim(filename_in, filename_out)
finally:
    pass
    # if os.path.exists(filename_in):
    #     os.remove(filename_in)
    # if os.path.exists(filename_out):
    #     os.remove(filename_out)
