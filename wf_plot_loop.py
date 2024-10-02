# Import packages 
from obspy import read, read_inventory 
#from obspy.core.inventory.inventory import read_inventory

## LOAD DATA

# Read a vertical channel (HHZ) data file from folder 
single_channel = read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHZ.2022.120", format="MSEED")

#glob - gets name 

# Read all data
#for station in range(120,261):
    #single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHZ.2022.%s" %(station), format="MSEED")


## COMPLETE INSTRUMENT REMOVAL (change units)

inv = read_inventory("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/resp/Wolverine_station_20240824.xml")
trace_len = len(single_channel)
#single_channel_rem=single_channel[0].copy() # multiple data files chained together 
single_channel_rem=single_channel.copy()
single_channel_rem.remove_response(inventory=inv)
single_channel_rem.plot(outfile='HHZ.120.removal_temp.png')


# running through the entire dataset
'''
for tr in range(1,trace_len +1):
    print(tr) # 
    rem_temp=single_channel[tr].copy() ##why 0???
    rem_temp.remove_response(inventory=inv)
    single_channel_rem += rem_temp

single_channel.remove_response(inventory=inv)
single_channel.plot(outfile='sc.2022.rem_respp.png')
'''




# Plot waveform 
#single_channel.plot(outfile='sc.2022.png')

# Restrict time frame  
dt_start = single_channel_rem[0].stats.starttime
dt_end = single_channel_rem[trace_len-1].stats.endtime
time = 1*60*60 # hours 
single_channel_rem.plot(starttime=dt_start+time , endtime=dt_start + time + 60*60 , outfile='sc.2022.120_hour.png')
#single_channel_rem.plot(starttime=dt_start+time , endtime=dt_end , outfile='sc.2022.119_hour.png') # end block 

# could make a for loop that plots each hour vertically and automattically identifies the last section 
'''
POI found at: 
2022-04-29 19:45 --  likely noise associated with leaving the site. 

'''
