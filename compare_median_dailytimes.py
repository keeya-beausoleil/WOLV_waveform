

# %%
#import packages
import obspy
from obspy import read, read_inventory
import obspy.signal.filter
import numpy as np
import matplotlib.pyplot as plt
import glob
import statistics as stats


# %%

# define file path 
data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/'
file_prefix = 'WOLW.XX.00.HHZ.2022.' 

# %%
days = np.array([122,152,182,213,244])
t = [2,8,16,20]
fig = plt.figure()
# %%
for i in days: 
    pre_filt1 = [0.05, 0.1, 80, 100] #standard bandpass parameters to remove low and high freq. signal 
    station = obspy.read(data_path + file_prefix + str(i), format='MSEED')
    instr_resp = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
    station_rem=station.copy()    
    start = station_rem[0].stats.starttime
    str_start = str(start)
    end = station_rem[0].stats.endtime

    station_rem_cut1 = station_rem.copy()
    station_rem_cut1.trim(starttime=start+(2*60*60), endtime = start+(2*60*60)+60*60)
    station_rem_cut1.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)

    station_rem_filt1 = station_rem_cut1.copy()
    station_rem_filt1.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
    #envelope1 = obspy.signal.filter.envelope(station_rem_filt1[0].data)
    abs1 = abs(station_rem_filt1[0].data)
    average1 = stats.median(abs1)

    station_rem_cut4 = station_rem.copy()
    station_rem_cut4.trim(starttime=start+(8*60*60), endtime = start+(8*60*60)+60*60)
    station_rem_cut4.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)

    station_rem_filt4 = station_rem_cut4.copy()
    station_rem_filt4.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
    #envelope4 = obspy.signal.filter.envelope(station_rem_filt4[0].data)
    abs4 = abs(station_rem_filt4[0].data)
    average4 = stats.median(abs4)

    station_rem_cut2 = station_rem.copy()
    station_rem_cut2.trim(starttime=start+(16*60*60), endtime = start+(16*60*60)+60*60)
    station_rem_cut2.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)

    station_rem_filt2 = station_rem_cut2.copy()
    station_rem_filt2.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
    #envelope2 = obspy.signal.filter.envelope(station_rem_filt2[0].data)
    abs2 = abs(station_rem_filt2[0].data)
    average2 = stats.median(abs2)

    station_rem_cut3 = station_rem.copy()
    station_rem_cut3.trim(starttime=start+(20*60*60), endtime = start+(20*60*60)+60*60)
    station_rem_cut3.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)

    station_rem_filt3 = station_rem_cut3.copy()
    station_rem_filt3.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
    #envelope3 = obspy.signal.filter.envelope(station_rem_filt3[0].data)
    abs3 = abs(station_rem_filt3[0].data)
    average3 = stats.median(abs3)

    avg = [average1,average4,average2,average3]
    a = stats.median(avg)
    avg = avg - min(avg)
    plt.plot(t,avg)

plt.xticks([2,8,16,20],["6 pm","12 am","8 am", "12 pm"] )
plt.xlabel("Hr of Day")
plt.ylabel("Median Tremor Amplitude Difference")
plt.title("Relative Median Tremor Amplitude of 1Hr Samples During 24Hrs")
plt.legend(["May1/May 2","May 31/June1","June30/July1", "July31/Aug1","Aug30/Sept1"])
plt.savefig("tempp_median_daily2WOLN.png")


# Daily Subplots 
'''
t = np.arange(0, station_rem_filt1[0].stats.npts / station_rem_filt1[0].stats.sampling_rate, station_rem_filt1[0].stats.delta)
plt.subplot(411) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.title("6pm May 1st")
plt.plot(t, (station_rem_filt1[0].data), 'k') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.subplot(412) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.title("12am May 1st")
plt.plot(t, (station_rem_filt4[0].data), 'r') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.subplot(413) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.title("8am May 2nd")
plt.plot(t, (station_rem_filt2[0].data), 'b') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.subplot(414) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(0, 1.6*10**(-7))
plt.title("12pm May 2nd")
plt.plot(t, (station_rem_filt3[0].data), 'g') # plot on top of each other add colour legend etc. * use melt days = np.array([213,121])
plt.suptitle("Tremor Amplitude of 5min Periods Throughout 24 Hrs")

plt.xlabel("Time (s)")
fig.savefig('temp_daily_compare'+str(day)+'.png')
#plt.ylim(-1*(10**-7), 1*(10**-7))
#plt.ylabel(str_start[5:10])
'''



# %%
