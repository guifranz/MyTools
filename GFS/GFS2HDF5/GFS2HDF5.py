import re
import datetime
import time
import glob, os, shutil
import subprocess

dirpath = os.getcwd()

input_file = "GFS2HDF5.dat"

download_dir = (dirpath+"\Download")
ConvertToNetcdf_dir = (dirpath+"\ConvertToNetcdf")
ConvertToHdf5_dir = (dirpath+"\ConvertToHdf5")

backup_path =  dirpath

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
def next_date (run):
	global next_start_date
	global next_end_date
		
	next_start_date = initial_date + datetime.timedelta(days = run)
	next_end_date = next_start_date + datetime.timedelta(days = 1)

#####################################################
def write_date(file_name):
		
	with open(file_name) as file:
		file_lines = file.readlines()
		
	number_of_lines = len(file_lines)
	
	for n in range(0,number_of_lines):
		line = file_lines[n]		
		if re.search("^START.+:", line):
			file_lines[n] = "START " + ": " + str(next_start_date.strftime("%Y %m %d %H %M %S")) + "\n"

		elif re.search("^END.+:", line):	
			file_lines[n] = "END " + ": " + str(next_end_date.strftime("%Y %m %d %H %M %S")) + "\n"
			
	with open(file_name,"w") as file:
		for n in range(0,number_of_lines) :
			file.write(file_lines[n])

#####################################################

read_date()

for run in range (0,number_of_runs):	
	
	#Update dates
	next_date (run)
	
	#Download
	os.chdir(download_dir)
	
	files = glob.glob("*.grb*")
	for filename in files:
		os.remove(filename)
		
	file_name = "GFS_DOWNLOAD.DAT"
	write_date(file_name)	
	output = subprocess.call(["GFS_DOWNLOAD.bat"])
	
	grib_files = glob.iglob(os.path.join(download_dir,"*.grb*"))
	for file in grib_files:
		shutil.copy(file, ConvertToNetcdf_dir)
	
	#ConvertToNetcdf
	os.chdir(ConvertToNetcdf_dir)
		
	files = glob.glob("*.nc")
	for filename in files:
		os.remove(filename)
	
	output = subprocess.call(["GFS_Convert2Netcdf.bat"])
	
	nc_files = glob.iglob(os.path.join(ConvertToNetcdf_dir,"*.nc"))
	for file in nc_files:
		shutil.copy(file, ConvertToHdf5_dir)
		
	files = glob.glob("*.grb2")
	for filename in files:
		os.remove(filename)
		
	#ConvertToHdf5
	os.chdir(ConvertToHdf5_dir)
	
	files = glob.glob("*.hdf*")
	for filename in files:
		os.remove(filename)
		
	output = subprocess.call(["Convert2Hdf5.bat"])
	
	output_dir = backup_path+"\\"+str(next_start_date.strftime("%Y"))+"\\"+str(next_start_date.strftime("%m"))+"\\"+str(next_start_date.strftime("%Y%m%d")) + "_" + str(next_end_date.strftime("%Y%m%d"))
		
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	
	hdf_files = glob.iglob(os.path.join(ConvertToHdf5_dir,"*.hdf*"))
	for file in hdf_files:
		shutil.copy(file, output_dir)
	
	files = glob.glob("*.nc")
	for filename in files:
		os.remove(filename)