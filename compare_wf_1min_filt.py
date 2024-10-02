# import packages
import obspy
from obspy import read, read_inventory , UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
import glob

# define file path 
data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/'
file_prefix = 'WOLN.XX.00.HHZ.2022.'

days = np.arange(119,259) # datasets (corresponding to recording days) in WOLN folder  
day_num = 121 #change 

pre_filt1 = [0.05, 0.1, 80, 100] #standard bandpass parameters to remove low and high freq. signal 
pre_filt2 = [0.5, 1, 80, 100] #filter out continuous signal noise 

station = obspy.read(data_path + file_prefix + str(day_num), format='MSEED')
instr_resp = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
station_rem=station.copy()
station_rem.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)
#station_rem.plot(outfile=str(119) +'_removal_temp.png')

start = station_rem[0].stats.starttime
end = station_rem[0].stats.endtime
station_rem.trim(starttime=start+(12*60*60), endtime = start+(12*60*60)+60*1)


# Low Pass Filter 
station_rem_lp_filt = station_rem.copy()
station_rem_lp_filt.filter('lowpass',freq = 1.0, corners = 2,zerophase=True)
#station_rem_lp_filt.plot(outfile='1min_' + str(day_num) + '_lowpass.png')

station_rem_hp_filt = station_rem.copy()
station_rem_hp_filt.filter('highpass',freq = 10, corners = 2,zerophase=True)

station_rem_bp_filt = station_rem.copy()
station_rem_bp_filt.filter('bandpass',freqmin = 1, freqmax = 10,corners = 4,zerophase=True)

t = np.arange(0, station_rem[0].stats.npts / station_rem[0].stats.sampling_rate, station_rem[0].stats.delta)
plt.subplot(411) #sharex=true
plt.subplots_adjust(hspace=1)
plt.ylim(-1*10**(-7), 1*10**(-7))
#plt.plot(t, station_rem[0].data, 'k')
plt.plot(t,station_rem[0].data, 'k')
plt.ylabel('Raw Data')

plt.subplot(412)
plt.subplots_adjust(hspace=1)
plt.ylim(-1*10**(-7), 1*10**(-7))
#plt.plot(t, station_rem_filt[0].data, 'k')
plt.plot(t,station_rem_lp_filt[0].data, 'k')
plt.ylabel('LP Data')

plt.subplot(413)
plt.subplots_adjust(hspace=1)
plt.ylim(-1*10**(-7), 1*10**(-7))
plt.plot(t,station_rem_hp_filt[0].data, 'k')
plt.ylabel('HP Data')

plt.subplot(414)
plt.subplots_adjust(hspace=1)
#plt.plot(t, station_rem_filt[0].data, 'k')
plt.plot(t,station_rem_bp_filt[0].data, 'k')
plt.ylim(-1*10**(-7), 1*10**(-7))
plt.ylabel('BP Data')
plt.xlabel('Time [s]')

plt.suptitle(station_rem[0].stats.starttime)
plt.savefig('1_min_' + str(day_num)+'_filtered.png')
