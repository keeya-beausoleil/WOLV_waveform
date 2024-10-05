#import packages
import obspy
from obspy import read, read_inventory
import obspy.signal.filter
import numpy as np
import matplotlib.pyplot as plt
import glob

# define file path 
data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/'
file_prefix = 'WOLN.XX.00.HHZ.2022.' 


day = 121
fig = plt.figure()


pre_filt1 = [0.05, 0.1, 80, 100] #standard bandpass parameters to remove low and high freq. signal 
station = obspy.read(data_path + file_prefix + str(day), format='MSEED')
instr_resp = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
station_rem=station.copy()
station_rem.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)
start = station_rem[0].stats.starttime
str_start = str(start)
end = station_rem[0].stats.endtime

station_rem_cut1 = station_rem.copy()
station_rem_cut1.trim(starttime=start+(2*60*60), endtime = start+(2*60*60)+60*5)
station_rem_filt1 = station_rem_cut1.copy()
station_rem_filt1.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
envelope1 = obspy.signal.filter.envelope(station_rem_filt1[0].data)

station_rem_cut4 = station_rem.copy()
station_rem_cut4.trim(starttime=start+(8*60*60), endtime = start+(8*60*60)+60*5)
station_rem_filt4 = station_rem_cut4.copy()
station_rem_filt4.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
envelope4 = obspy.signal.filter.envelope(station_rem_filt4[0].data)

station_rem_cut2 = station_rem.copy()
station_rem_cut2.trim(starttime=start+(16*60*60), endtime = start+(16*60*60)+60*5)
station_rem_filt2 = station_rem_cut2.copy()
station_rem_filt2.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
envelope2 = obspy.signal.filter.envelope(station_rem_filt2[0].data)

station_rem_cut3 = station_rem.copy()
station_rem_cut3.trim(starttime=start+(20*60*60), endtime = start+(20*60*60)+60*5)
station_rem_filt3 = station_rem_cut3.copy()
station_rem_filt3.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
envelope3 = obspy.signal.filter.envelope(station_rem_filt3[0].data)


t = np.arange(0, station_rem_filt1[0].stats.npts / station_rem_filt1[0].stats.sampling_rate, station_rem_filt1[0].stats.delta)
plt.subplot(411) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.legend(["6pm June 31st"])
plt.plot(t, (station_rem_filt1[0].data), 'k') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.subplot(412) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.legend(["12am June 31st"])
plt.plot(t, (station_rem_filt4[0].data), 'r') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.subplot(413) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.legend(["8am May 1st"])
plt.plot(t, (station_rem_filt2[0].data), 'b') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.subplot(414) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.legend(["12pm May 1st"])
plt.plot(t, (station_rem_filt3[0].data), 'g') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.suptitle("Tremor Amplitude Throughout A Day")

plt.xlabel("Time (s)")
fig.savefig('temp_daily_compare'+str(day)+'.png')
#plt.ylim(-1*(10**-7), 1*(10**-7))
#plt.ylabel(str_start[5:10])
