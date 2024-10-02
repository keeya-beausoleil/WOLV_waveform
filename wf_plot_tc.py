from obspy import read 
three_channel_E = read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHE.2022.119", format="MSEED")
three_channel_N = read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHN.2022.119", format="MSEED")
three_channel_Z = read("/data/stor/basic_data/seismic_data/day_vols/WOLVERINE/WOLN/WOLN.XX.00.HHZ.2022.119", format="MSEED")
three_channel = three_channel_E +three_channel_N + three_channel_Z
#channel.plot()
three_channel.plot(outfile='tc.2022.119.png')
