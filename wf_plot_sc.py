from obspy import read 
single_channel = read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.119", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.120", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.121", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.122", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.123", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.124", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.125", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.126", format="MSEED")
single_channel += read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.127", format="MSEED")

#st.plot()
single_channel.plot(outfile='sc.2022.png')
#dt = single_channel[0].stats.starttime
#single_channel.plot(starttime=dt + 60*60, endtime=dt + 60*60 + 60, outfile='sc.2022.119_hour.png')