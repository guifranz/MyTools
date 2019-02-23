import re
import datetime
import time
import glob, os, shutil
import subprocess
from urllib.request import urlopen, Request
from urllib.error import HTTPError

file_name = "run.bat"

input_file = "GFS_DOWNLOAD.dat"

url="https://nomads.ncdc.noaa.gov/data"
url_forecast_mode="https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod"

#folder="gfsanl"
number="4"
grib="grb2"

#####################################################
def read_date():
	global initial_date
	global end_date
	global number_of_runs
	global forecast_mode
	
	forecast_mode = 0
	number_of_runs = 1
	
	with open(input_file) as file:
		for line in file:
			if re.search("^FORECAST_MODE.+:", line):
				words = line.split()
				forecast_mode = int(words[2])
				
	if forecast_mode == 1:
					
		#initial_date = datetime.datetime.now() + datetime.timedelta(days = 0)
		initial_date = datetime.datetime.now() + datetime.timedelta(days = -1)
		
	else:	
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
	global folder,gfs_type
	
	gfs_type = 1
	
	with open(input_file) as file:
		for line in file:
			if re.search("^GFS_TYPE.+:", line):
				words = line.split()
				gfs_type = int(words[2])
	
	if gfs_type == 1:
		folder = "gfs4"
	elif gfs_type == 0:
		folder = "gfsanl"

#####################################################
def download_file():

	if gfs_type == 1:
	
		if forecast_mode == 1:
		
			#folder_date = initial_date + datetime.timedelta(days = -5)
		
			#path = url+"/"+folder+"/"+str(folder_date.strftime("%Y%m"))+"/"+str(folder_date.strftime("%Y%m%d"))+"/"+"gfs_4"+"_"+str(folder_date.strftime("%Y%m%d"))

			path = url_forecast_mode+"/gfs."+str(initial_date.strftime("%Y%m%d"))+"18/"
			
			hour = 3
			
			for t in range (0,39):
			
				
				times = "gfs.t18z.pgrb2.0p50.f" + str(hour).rjust(3,'0') 

				with open(file_name,"w") as file:
					file.write("set url_inv="+path+times+".idx\n")
					file.write("set url_grb="+path+times+"\n")
					file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(initial_date.strftime("%Y%m%d"))+times+"_temp."+grib+"\n")
			
				output = subprocess.call([file_name])
				
				
				# response = urlopen(path+times)
				# data = response.read()
				# filename = str(initial_date.strftime("%Y%m%d"))+times+"_temp."+grib
				# file_ = open(filename, 'wb')
				# file_.write(data)
				# file_.close()
					
				hour = hour + 3
		
		
		else:
	
			path = url+"/"+folder+"/"+str(next_start_date.strftime("%Y%m"))+"/"+str(next_start_date.strftime("%Y%m%d"))+"/"+"gfs_4"+"_"+str(next_start_date.strftime("%Y%m%d"))
			
			times = ("_0000_000","_0000_003","_0000_006","_0000_009","_0000_012","_0000_015","_0000_018","_0000_021","_0000_024")
			number_of_times = len(times)		
			
			for t in range (0,number_of_times):
			
				try:
					response = urlopen(path+times[t]+".inv")
					#inv exists
					with open(file_name,"w") as file:
						file.write("set url_inv="+path+times[t]+".inv\n")
						file.write("set url_grb="+path+times[t]+"."+grib+"\n")
						file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(next_start_date.strftime("%Y%m%d"))+times[t]+"_temp."+grib+"\n")
			
					output = subprocess.call([file_name])
		
				except HTTPError:
					#inv doesn't exist
					data = response.read()
					filename = str(next_start_date.strftime("%Y%m%d"))+times[t]+"_temp."+grib
					file_ = open(filename, 'w')
					file_.write(data)
					file_.close()
					
	else:
		
		if run == 0:
			start_date = initial_date - datetime.timedelta(days = 1)
			path = url+"/"+folder+"/"+str(start_date.strftime("%Y%m"))+"/"+str(start_date.strftime("%Y%m%d"))+"/"+folder+"_"+number+"_"+str(start_date.strftime("%Y%m%d"))
			
			times = ("_1800_003","_1800_006")
			number_of_times = len(times)		

			for t in range (0,number_of_times):
				try:
					response = urlopen(path+times[t]+".inv")
					#print "inv exists"
					with open(file_name,"w") as file:
						file.write("set url_inv="+path+times[t]+".inv\n")
						file.write("set url_grb="+path+times[t]+"."+grib+"\n")
						file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(start_date.strftime("%Y%m%d"))+times[t]+"_temp."+grib+"\n")
					
					output = subprocess.call([file_name])
				
				except HTTPError:
					#print "inv doesn't exist"
					data = response.read()
					filename = str(start_date.strftime("%Y%m%d"))+times[t]+"_temp."+grib
					file_ = open(filename, 'w')
					file_.write(data)
					file_.close()

		
		path = url+"/"+folder+"/"+str(next_start_date.strftime("%Y%m"))+"/"+str(next_start_date.strftime("%Y%m%d"))+"/"+folder+"_"+number+"_"+str(next_start_date.strftime("%Y%m%d"))
		
		times = ("_0000_003","_0000_006","_0600_003","_0600_006","_1200_003","_1200_006","_1800_003","_1800_006")
		number_of_times = len(times)		
		
		for t in range (0,number_of_times):
			try:
				response = urlopen(path+times[t]+".inv")
				#inv exists
				with open(file_name,"w") as file:
					file.write("set url_inv="+path+times[t]+".inv\n")
					file.write("set url_grb="+path+times[t]+"."+grib+"\n")
					file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(next_start_date.strftime("%Y%m%d"))+times[t]+"_temp."+grib+"\n")
				
				output = subprocess.call([file_name])

			except HTTPError:
				#inv doesn't exist
				data = response.read()
				filename = str(next_start_date.strftime("%Y%m%d"))+times[t]+"_temp."+grib
				file_ = open(filename, 'w')
				file_.write(data)
				file_.close()
		
		start_date = initial_date + datetime.timedelta(days = 1)
		path = url+"/"+folder+"/"+str(start_date.strftime("%Y%m"))+"/"+str(start_date.strftime("%Y%m%d"))+"/"+folder+"_"+number+"_"+str(start_date.strftime("%Y%m%d"))
			
		times = ("_0000_003")
		
		try:
			response = urlopen(path+times+".inv")
			#inv exists
			with open(file_name,"w") as file:
				file.write("set url_inv="+path+times+".inv\n")
				file.write("set url_grb="+path+times+"."+grib+"\n")
				file.write('PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% '+str(start_date.strftime("%Y%m%d"))+times+"_temp."+grib+"\n")
			
			output = subprocess.call([file_name])
		
		except HTTPError:
			#inv doesn't exist
			data = response.read()
			filename = str(start_date.strftime("%Y%m%d"))+times+"_temp."+grib
			file_ = open(filename, 'w')
			file_.write(data)
			file_.close()
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