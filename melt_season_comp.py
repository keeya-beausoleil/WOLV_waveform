# import packages
import obspy
from obspy import read, read_inventory, UTCDateTime 
import numpy as np
import matplotlib.pyplot as plt
import glob

# define file path 
data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/'
#data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLC/'
file_prefix = 'WOLN.XX.00.HHZ.2022.' 
#file_prefix = 'WOLC.XX.00.HHZ.2022.' 

fig = plt.figure(figsize=(35,6))

melt_days = np.array([121,213]) # 

#melt_days = np.array([123,213]) # 121 was not the right time period?? 

a = 1
for day in melt_days: 
    pre_filt1 = [0.05, 0.1, 80, 100] #standard bandpass parameters to remove low and high freq. signal 
    station = obspy.read(data_path + file_prefix + str(day), format='MSEED')
    instr_resp = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
    station_rem=station.copy()
    station_rem.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)

    start = station_rem[0].stats.starttime
    end = station_rem[0].stats.endtime
    station_rem.trim(starttime=start+(20*60*60), endtime = start+(20*60*60)+60*5)
    station_rem_filt = station_rem.copy()
    station_rem_filt.filter('bandpass',freqmin = 1, freqmax = 10,corners = 4,zerophase=True)
    t = np.arange(0, station_rem[0].stats.npts / station_rem[0].stats.sampling_rate, station_rem[0].stats.delta)
    ax = plt.subplot(2, 1, a)
    plt.subplots_adjust(hspace=1)
    ax.plot(t, station_rem_filt[0].data) 
    #plt.plot(t, station_rem_filt[0].data) # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
    ax.set_ylim(-1*(10**-7), 1*(10**-7))
    ax.set_title(station_rem[0].stats.starttime)
    #plt.ylabel(str(day))
    plt.xlabel("Time (s)")
    a = a+1

#fig.savefig('melt_compare_layered.png')
fig.savefig('melt_compare_5min_WOLC.png')




