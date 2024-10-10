# import packages
import obspy
from obspy import read, read_inventory, UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
import glob

# define file path 
data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/'
file_prefix = 'WOLN.XX.00.HHZ.2022.'

days = np.arange(119,259) # datasets (corresponding to recording days) in WOLN folder  
days_edit = np.arange(119,259,27)
days_edit[0] = 121
comp_plots = np.arange(0,140,5)
comp_plots = np.arange(0,5,5)

pre_filt1 = [0.05, 0.1, 80, 100] #standard bandpass parameters to remove low and high freq. signal 
pre_filt2 = [0.5, 1, 80, 100] #filter out continuous signal noise 

fig = plt.figure()

results = [] 
a = 1
#for n in comp_plots:
    #print(n)
    #a = 1
for i in days_edit: #days[n+1:n+3]:
        print(i) 
        print(a)
        station = obspy.read(data_path + file_prefix + str(i), format='MSEED')
        instr_resp = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
        station_rem=station.copy()
        station_rem.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)
        start = station_rem[0].stats.starttime
        str_start = str(start)
        end = station_rem[0].stats.endtime
        station_rem.trim(starttime=start+(20*60*60), endtime = start+(20*60*60)+60) # at noon Alaska 
        station_rem_filt = station_rem.copy()
        station_rem_filt.filter('bandpass',freqmin = 1, freqmax = 10,corners = 4,zerophase=True)
        ax = fig.add_subplot(6,1,a)
        t = np.arange(0, station_rem[0].stats.npts / station_rem[0].stats.sampling_rate, station_rem[0].stats.delta)
        ax.plot(t, station_rem_filt[0].data, "b-")
        plt.subplots_adjust(hspace=1)
        #ax[a].plot(station_rem[0].data)
        ax.set_ylim(-1*(10**-7), 1*(10**-7))
        plt.ylabel(str_start[5:10])
        #ax[a].text(0, 5000, str(start+(12*3600)))
        a=a+1
plt.xlabel("Time(s)")
plt.suptitle("Comparison of Filtered Waveforms from 6 days Across Season")
fig.savefig('1_min_traces_compare_filt.png')
 
