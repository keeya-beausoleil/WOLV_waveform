#import packages
import obspy
from obspy import read, read_inventory
import numpy as np
import matplotlib.pyplot as plt
import obspy.signal.filter
import glob

# define file path 
data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/'
file_prefix = 'WOLN.XX.00.HHZ.2022.' 

day = 121
pre_filt1 = [0.05, 0.1, 80, 100] #standard bandpass parameters to remove low and high freq. signal 
station = obspy.read(data_path + file_prefix + str(day), format='MSEED')
instr_resp = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
station_rem=station.copy()
station_rem.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)
start = station_rem[0].stats.starttime
str_start = str(start)
end = station_rem[0].stats.endtime
station_rem_cut1 = station_rem.copy()
station_rem_cut1.trim(starttime=start+(20*60*60)+775, endtime = start+(20*60*60)+850) # 20 = 12 noon Alaska
station_rem_filt1 = station_rem_cut1.copy()
station_rem_filt1.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
t = np.arange(0, station_rem_filt1[0].stats.npts / station_rem_filt1[0].stats.sampling_rate, station_rem_filt1[0].stats.delta)
#envelope = obspy.signal.filter.envelope(station_rem_filt1[0].data)
fig = plt.figure()
plt.ylabel(str_start)
plt.plot(t, station_rem_filt1[0].data)
fig.savefig("temp_quake.png")