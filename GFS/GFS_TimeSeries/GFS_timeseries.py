import re
import datetime
import time
import glob, os, shutil
import subprocess, math

name = "gfs_4_" 
lon = "-43.95" 
lat = "-22.8"
 
input_file = "GFS_TimeSeries.dat"
temp_file = "temp.txt"

url="https://nomads.ncdc.noaa.gov/data"
folder = "gfs4"

output_file = "Meteo_GFS_TimeSeries.dat"

#####################################################
def read_date():
	global initial_date
	global end_date
	global number_of_runs
	
	with open(input_file) as file:
		for line in file:
			if re.search("^START.+:", line):
				words = line.split()
				initial_date = datetime.datetime(int(words[2]),int(words[3]),int(words[4]),int(words[5]),int(words[6]),int(words[7]))
			elif re.search("^END.+:", line):
				words = line.split()
				end_date = datetime.datetime(int(words[2]),int(words[3]),int(words[4]),int(words[5]),int(words[6]),int(words[7]))
					
	interval = end_date - initial_date
	
	number_of_runs = interval.days
	
#####################################################
#####################################################
def next_date (run):
	global next_start_date
	#global next_end_date

	next_start_date = initial_date + datetime.timedelta(days = run)
	#next_end_date = next_start_date + datetime.timedelta(days = run+1)

#####################################################

read_date()

if os.path.exists(output_file):
	print ("writing to existing file " + output_file)
else:
	with open(output_file,"w") as file:
		file.write("!Time series from" + url + "\n")
		file.write("!Location " + lon + " " + lat + "\n")
		file.write("!time temp_2m(C) U_10m(m/s) V_10m(m/s) DLWR(W/m2) DSWR(W/m2) HPBL(m) Cloud_Cover RH Precipitation(kg m-2 s-1)"+"\n")
			
for run in range (0,number_of_runs):	
	
	#Update dates
	next_date (run)
	
	#path = url+str(next_start_date.strftime("%Y"))+"/"+str(next_start_date.strftime("%Y%m"))+"/"+str(next_start_date.strftime("%Y%m%d"))+"/"

	#times = ("00","06","12","18")
	#number_of_times = len(times)	

	path = url+"/"+folder+"/"+str(next_start_date.strftime("%Y%m"))+"/"+str(next_start_date.strftime("%Y%m%d"))+"/"
			
	times = ("_0000_003","_0000_006","_0000_009","_0000_012","_0000_015","_0000_018","_0000_021","_0000_024")
	number_of_times = len(times)	

	for t in range (0,number_of_times):
	
		files = glob.glob("*.grb2")
		for filename in files:
			os.remove(filename)
			
		filename = name+str(next_start_date.strftime("%Y%m%d"))+times[t]+".grb2"
		
		os.system ('wget --no-check-certificate ' + path + filename)
		
		if os.path.exists(temp_file):
			os.remove(temp_file)

		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":TMP:2 m above" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":UGRD:10 m above" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":VGRD:10 m above" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":DLWRF:surface" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":DSWRF:surface" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match "HPBL:surface" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":TCDC:entire atmosphere" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		#os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":QMAX:2 m" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		#os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":QMIN:2 m" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		#os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":PRES:surface" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":RH:2 m above" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		os.system ('wgrib2 -lon ' + lon + ' ' + lat + ' -append -match ":PRATE:surface" ' + filename +  ' -no_header -lola -43.95:1:1 -22.8:1:1 ' + temp_file + ' text')
		
		with open(temp_file) as file:
			original_value = file.readlines()
		
		new_value = [0]*9
		
		new_value[0] = float(original_value[0]) - 273.15 # air temperature
		new_value[1] = float(original_value[1]) # u-component of wind
		new_value[2] = float(original_value[2]) # v-component of wind
		new_value[3] = float(original_value[3]) # Downward longwave radiation flux
		new_value[4] = float(original_value[4]) # Downward shortwave radiation flux
		new_value[5] = float(original_value[5]) # Planetary Boundary Layer Height
		new_value[6] = float(original_value[6])/100 # Total cloud cover
		
		#specific_humidity = (float(original_value[7])+float(original_value[8]))/2
		#pressure = float(original_value[9]) 
		 
		#relative_humidity = 0.263*pressure*specific_humidity*(math.exp(17.67*new_value[0]/(float(original_value[0])-29.95)))**-1 
		#new_value[7] = min(relative_humidity/100, 1.0)
		
		new_value[7] = min(float(original_value[7])/100, 1.0) #Relative Humidity
		new_value[8] = float(original_value[8]) #Precipitation rate
		
		
		number_of_values = len(new_value)

		with open(output_file,"a") as file:
			file.write(str(next_start_date.strftime("%Y%m%d"))+times[t]+" ")
			for n in range(0,number_of_values) :
				file.write(str(new_value[n]).rstrip('\n')+" ")

			file.write("\n")
			