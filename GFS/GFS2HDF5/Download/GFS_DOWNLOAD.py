import re, sys
import datetime
import time
import glob, os, shutil
import subprocess
import urllib2

file_name = "run.bat"

input_file = "GFS_DOWNLOAD.dat"

url="https://nomads.ncdc.noaa.gov/data"
#folder="gfsanl"
number="4"
grib=".grb2"

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
def read_gfs_product_type():
	global folder, gfs_forecasts
	
	with open(input_file) as file:
		for line in file:
			if re.search("^GFS_FORECASTS.+:", line):
				words = line.split()
				gfs_forecasts = int(words[2])
	
	if gfs_forecasts == 1:
		folder = "gfs4"
	else:
		folder = "gfsanl"

#####################################################
def download_file():

	if gfs_forecasts == 1:
	
		with open(file_name,"w") as file:
	
			path = url+"/"+folder+"/"+str(next_start_date.strftime("%Y%m"))+"/"+str(next_start_date.strftime("%Y%m%d"))+"/"+"gfs_4"+"_"+str(next_start_date.strftime("%Y%m%d"))
			
			times = ("_0000_000","_0000_003","_0000_006","_0000_009","_0000_012","_0000_015","_0000_018","_0000_021","_0000_024")
			number_of_times = len(times)		
			
			for t in range (0,number_of_times):
				file.write("set url_inv="+path+times[t]+".inv\n")
				file.write("set url_grb="+path+times[t]+grib+"\n")
				file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(next_start_date.strftime("%Y%m%d"))+times[t]+"_temp"+grib+"\n")
	
		output = subprocess.call([file_name])
		
	else:
		
		if run == 0:
			start_date = initial_date - datetime.timedelta(days = 1)
			path = url+"/"+folder+"/"+str(start_date.strftime("%Y%m"))+"/"+str(start_date.strftime("%Y%m%d"))+"/"+folder+"_"+number+"_"+str(start_date.strftime("%Y%m%d"))
			
			try:
				response = urllib2.urlopen(path+"_1800_006"+".inv")
				#print("inv exists")
				inv_file_exists = True
				
			except urllib2.HTTPError:
				#print("inv doesn't exist")
				inv_file_exists = False
				
			if inv_file_exists:
				with open(file_name,"w") as file:
					file.write("set url_inv="+path+"_1800_006"+".inv\n")
					file.write("set url_grb="+path+"_1800_006"+grib+"\n")
					file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(start_date.strftime("%Y%m%d"))+"_1800_006"+"_temp"+grib+"\n")

				output = subprocess.call([file_name])
			
			else:
				grib_file = urllib2.urlopen(path+"_1800_006"+grib)
				filename = str(start_date.strftime("%Y%m%d"))+"_1800_006"+"_temp"+grib
				with open(filename, "wb") as output:
					output.write(grib_file.read())
		
		path = url+"/"+folder+"/"+str(next_start_date.strftime("%Y%m"))+"/"+str(next_start_date.strftime("%Y%m%d"))+"/"+folder+"_"+number+"_"+str(next_start_date.strftime("%Y%m%d"))
		
		times = ("_0000_003","_0000_006","_0600_003","_0600_006","_1200_003","_1200_006","_1800_003","_1800_006")
		number_of_times = len(times)		
		
		for t in range (0,number_of_times):
			try:
				response = urllib2.urlopen(path+times[t]+".inv")
				#print("inv exists")
				inv_file_exists = True
				
			except urllib2.HTTPError:
				#print("inv doesn't exist")
				inv_file_exists = False
				
			if inv_file_exists:
				with open(file_name,"w") as file:
					file.write("set url_inv="+path+times[t]+".inv\n")
					file.write("set url_grb="+path+times[t]+grib+"\n")
					file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(next_start_date.strftime("%Y%m%d"))+times[t]+"_temp"+grib+"\n")
				
				output = subprocess.call([file_name])
				
			else:
				grib_file = urllib2.urlopen(path+times[t]+grib)
				filename = str(next_start_date.strftime("%Y%m%d"))+times[t]+"_temp"+grib
				with open(filename, "wb") as output:
					output.write(grib_file.read())

#####################################################
def next_date (run):
	global next_start_date
	global next_end_date
		
	next_start_date = initial_date + datetime.timedelta(days = run)
	#next_end_date = next_start_date + datetime.timedelta(days = run+1)

#####################################################

read_date()

read_gfs_product_type ()

for run in range (0,number_of_runs):	
	
	#Update dates
	next_date (run)
	
	download_file()
	
	#output = subprocess.call([file_name])