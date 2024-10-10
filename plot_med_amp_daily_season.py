
#%%
#import packages
import obspy
from obspy import read, read_inventory
import numpy as np
import matplotlib.pyplot as plt
import glob
import statistics as stats
from scipy.optimize import curve_fit 
import os

#%%
# define file path 
data_path = '/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLC/'
file_prefix = 'WOLC.XX.00.HHZ.2022.' 

fig = plt.figure(figsize=(12,5))

#weekly_days = np.arange(119,260,7) # WOLN

all_days = np.arange(119,260,1) 
#weekly_days[0] = 121
#weekly_days[0] = 123
#weekly_days[4] = 150 # no 143-149 data in WOLC
#weekly_days[20] = 257

daily_avg = []
date = [] 
days = []
#%%

for day in all_days:
    pre_filt1 = [0.05, 0.1, 80, 100] #standard bandpass parameters to remove low and high freq. signal 
    stn = data_path + file_prefix + str(day)
    if os.path.exists(stn):
        station = obspy.read(stn, format='MSEED')
        instr_resp = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
        station_rem=station.copy()
        station_rem.remove_response(inventory=instr_resp, water_level= None,pre_filt=pre_filt1)
        start = station_rem[0].stats.starttime
        str_start = str(start)
        end = station_rem[0].stats.endtime
        station_rem.trim(starttime=start+(20*60*60), endtime = start+(20*60*60)+60*20)
        print(len(station_rem))
        if len(station_rem)>0: 
            station_rem_filt = station_rem.copy()
            station_rem_filt.filter('bandpass',freqmin = 1.5, freqmax = 10,corners = 4,zerophase=True)
            weekly_data = abs(station_rem_filt[0].data)
            average = stats.median(weekly_data)
            daily_avg.append(average)
            date.append(str_start[5:10])
            days.append(day)

        else:
            pass 
    else:
        pass 

print(days)
print(daily_avg)
#%%
# 5min= [8.815942107718926e-09, 8.339045157045451e-09, 6.789992889781462e-09, 5.937556410837761e-09, 9.042436437342592e-09, 1.2104697209096629e-08, 2.1672824754342216e-08, 1.5056362698949945e-08, 3.001772981896927e-08, 2.3984697681035436e-08, 3.099427345254124e-08, 1.6294697271695768e-08, 1.6160971268663964e-08, 1.669725199146196e-08, 1.5539115930900364e-08, 1.8259723569811938e-08, 1.5752943999759903e-08, 1.6073930398335746e-08, 1.6398321265756305e-08, 1.565430293159867e-08, 1.5731932614913123e-08]
# 20min = [9.544455055766524e-09, 5.806612506664849e-09, 6.829046355692611e-09, 6.196221643644461e-09, 8.980288574830592e-09, 1.2402975752162065e-08, 1.8260443444223235e-08, 1.4724274322160145e-08, 2.5645707132820496e-08, 2.3328847590258983e-08, 3.170501227867278e-08, 1.6321481940228808e-08, 1.5689946572815592e-08, 1.6455368340529134e-08, 1.5545972962397756e-08, 1.8195943200676126e-08, 1.598287846965614e-08, 1.6259846868571604e-08, 1.6372588256686418e-08, 1.560977677183184e-08, 1.5966842046369167e-08]
#week = np.arange(0,21)
#week = np.arange(0,7)
plt.xticks(days, date, rotation='vertical',fontsize=4)
plt.ylabel("Median Tremor Amplitude of 20min")
plt.title("Median Daily Tremor Amp. During Season")
plt.scatter(days,daily_avg,s=1,c='k')
plt.plot(days,daily_avg,'b')
fig.savefig('temp_sn_trend_WOLC2.png')

#%%