from obspy import read 
single_channel = read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.119", format="MSEED")
#st.plot()
single_channel.plot(outfile='sc.XX.00.HHE.2022.119.png')
