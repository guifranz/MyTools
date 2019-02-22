import re
import datetime
import time
import glob, os, shutil
import subprocess

file_name = "run.bat"

input_file = "CMEMS_DOWNLOAD.dat"

url="http://nrtcmems.mercator-ocean.fr/motu-web/Motu"
product="GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS"
dataset="global-analysis-forecast-phy-001-024"
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
def read_keyword_value(keyword_name): 
	with open(input_file) as file:
		for line in file:
			if re.search("^"+keyword_name+".+: ", line):
				words = line.split()
				#value = int(words[2])
				value = words[2]
				return value
#####################################################
def write_download_file():

	#Take also the previous day for running Mohid
	start_date = next_start_date - datetime.timedelta(days = 1)
	
	with open(file_name,"w") as file:
		file.write(python_bin_directory+" "+motu_python_script_directory+" -u "+user+" -p "+password+" -m "+url+" -s "+product+" -d "+dataset+ 
			        " -x "+lon_min+" -X "+lon_max+" -y "+lat_min+" -Y "+lat_max+" -t "+'"'+str(start_date.strftime("%Y-%m-%d "))+" 12:00:00"+'"'+" -T "+
					'"'+str(next_end_date.strftime("%Y-%m-%d "))+" 12:00:00"+'"'+" -z "+start_depth+" -Z "+end_depth+" -v zos -v so -v thetao -v uo -v vo -o "+output_directory+" -f "+
					output_file_name+".nc")	

	# with open(file_name,"w") as file:
		# file.write(python_bin_directory+" "+motu_python_script_directory+" -u "+user+" -p "+password+" -m "+url+" -s "+product+" -d "+dataset+ 
			        # " -x "+lon_min+" -X "+lon_max+" -y "+lat_min+" -Y "+lat_max+" -t "+'"'+str(next_start_date.strftime("%Y-%m-%d "))+" 12:00:00"+'"'+" -T "+
					# '"'+str(next_end_date.strftime("%Y-%m-%d "))+" 12:00:00"+'"'+" -z "+start_depth+" -Z "+end_depth+" -v zos -v so -v thetao -v uo -v vo -o "+output_directory+" -f "+
					# output_file_name+".nc")	
			
#####################################################
def next_date (run):
	global next_start_date
	global next_end_date
	global old_start_date
	global old_end_date
		
	next_start_date = initial_date + datetime.timedelta(days = run)
	next_end_date = initial_date + datetime.timedelta(days = run+1)

#####################################################
#Read main keywords 

keyword_name = ("path_to_your_python_bin_directory","path_to_your_motu_python_script_directory","your_user","your_password", "lon_min",
                "lon_max","lat_min","lat_max","start_depth","end_depth","your_output_directory","your_output_file_name")

number_of_keywords = len(keyword_name)

keyword_value = [0]*number_of_keywords
for n in range (0,number_of_keywords):
	keyword_value[n] = read_keyword_value(keyword_name[n])

python_bin_directory = keyword_value[0]
motu_python_script_directory = keyword_value[1]
user = keyword_value[2]
password = keyword_value[3]
lon_min = keyword_value[4]
lon_max = keyword_value[5]
lat_min = keyword_value[6]
lat_max = keyword_value[7]
start_depth = keyword_value[8]
end_depth = keyword_value[9]
output_directory = keyword_value[10]
output_file_name = keyword_value[11]

read_date()

######################################################

for run in range (0,number_of_runs):	
	
	#Update dates
	next_date (run)
	
	write_download_file()
	
	output = subprocess.call([file_name])