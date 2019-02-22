import re
import datetime
import time
import glob, os, shutil
import subprocess, math

name = "flxf06.gdas." 
#BARRAGEM DE LAJES ,UHE FONTES NOVA RES. LAJES BARRAMENTO,RIO DAS PEDRAS (LAJES) ,BARRAGEM DE SALTO ,BARRA,RIO DAS PEDRAS,FAZENDA LAPA,BARRA (LAJES),BUGIO,ROSRIO (PORTAL)
lon = [-43.87833333,-43.8808,-43.93666667,-43.87916667,-43.9583,-43.9367,-43.9953,-43.9583,-44.0289,-44.0486]
lat = [-22.70083333,-22.7022,-22.79611111,-22.7,-22.7731,-22.7961,-22.8522,-22.7731,-22.7311,-22.7908]

input_file = "CFSR_timeseries.dat"
temp_file = "temp.txt"

url="https://nomads.ncdc.noaa.gov/data/modeldata/cmd_flxf/"

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

for run in range (0,number_of_runs):	
	
	#Update dates
	next_date (run)
	
	path = url+str(next_start_date.strftime("%Y"))+"/"+str(next_start_date.strftime("%Y%m"))+"/"+str(next_start_date.strftime("%Y%m%d"))+"/"

	times = ("00","06","12","18")
	number_of_times = len(times)		

	for t in range (0,number_of_times):
	
		files = glob.glob("*.grb2")
		for filename in files:
			os.remove(filename)
			
		filename = name+str(next_start_date.strftime("%Y%m%d"))+times[t]+".grb2"
		
		os.system ('wget --no-check-certificate ' + path + filename)

		for l in range(len(lon)):
			if os.path.exists(temp_file):
				os.remove(temp_file)

			aux = str(lon[l]) + ':1:1 ' + str(lat[l]) + ':1:1 '
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":TMP:2 m above" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":UGRD:10 m above" ' + filename +  ' -no_header -lola ' + aux  + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":VGRD:10 m above" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":DLWRF:surface:6 hour" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":DSWRF:surface:6 hour" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match "HPBL:surface:6 hour" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":TCDC:entire atmosphere" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":QMAX:2 m" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":QMIN:2 m" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":PRES:surface:6 hour" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
			os.system ('wgrib2 -lon ' + str(lon[l]) + ' ' + str(lat[l]) + ' -append -match ":PRATE:surface" ' + filename +  ' -no_header -lola ' + aux + temp_file + ' text')
		
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

			specific_humidity = (float(original_value[7])+float(original_value[8]))/2
			pressure = float(original_value[9])

			relative_humidity = 0.263*pressure*specific_humidity*(math.exp(17.67*new_value[0]/(float(original_value[0])-29.95)))**-1
			new_value[7] = min(relative_humidity/100, 1.0)

			new_value[8] = float(original_value[10])*6*3600 #Precipitation rate


			number_of_values = len(new_value)

			output_file = "Meteo_TimeSeries" + str(lon[l]) + "_" + str(lat[l]) + ".dat"

			if os.path.exists(output_file):
				print ("writing to existing file " + output_file)
			else:
				with open(output_file, "w") as file:
					file.write("!Time series from" + url + "\n")
					file.write("!Location " + str(lon[l]) + " " + str(lat[l]) + "\n")
					file.write(
						"!time temp_2m(C) U_10m(m/s) V_10m(m/s) DLWR(W/m2) DSWR(W/m2) HPBL(m) Cloud_Cover RH Precipitation(mm)" + "\n")

			with open(output_file,"a") as file:
				file.write(str(next_start_date.strftime("%Y%m%d"))+times[t]+" ")
				for n in range(0,number_of_values) :
					file.write(str(new_value[n]).rstrip('\n')+" ")

				file.write("\n")
			