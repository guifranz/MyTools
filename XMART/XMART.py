import re, datetime, time
import glob, os, shutil
import subprocess, sys

dirpath = os.getcwd()

input_file = "XMART.dat"

exe_dir = (dirpath+"\\Level_1\\exe")
mohid_log = (exe_dir+"\\Mohid.log")

#Define number of domains
number_of_domains = 1

#Define directories (comment when not applicable)
results_dir = [0]*number_of_domains
results_dir [0] = (dirpath+"\\Level_1\\res")
#results_dir [1] = (dirpath+"\\Level_1\\Level_2\\res")

data_dir = [0]*number_of_domains
data_dir [0] = (dirpath+"\\Level_1\\data")
#data_dir [1] = (dirpath+"\\Level_1\\Level_2\\data")

backup_dir = [0]*number_of_domains
backup_dir [0] = (dirpath+"\\Backup\\Level_1")
#backup_dir [1] = (dirpath+"\\Backup\\Level_2")


#interpolate_gfs_dir = (dirpath+"\\Work\\GFS\\Interpolate")
#file_name_gfs = "GFS_Plataforma_SE.hdf5"

dir_meteo = ("F:\\Aplica_OP\\Work\\GFS\\GFS2HDF5\\Backup")
file_name_meteo = "gfs.hdf5"

boundary_conditions_dir = (dirpath+"\\Level_1\\General Data\\Boundary Conditions")

dir_father_phy_results = ("F:\\Aplica_OP\\Work\\CMEMS\\GLOBAL_ANALYSIS_FORECAST_PHY\\Backup")
file_name_phy = "Plataforma_SE.hdf5"
#file_name_phy = "Hydrodynamic_2.hdf5"


dir_father_bio_results = ("F:\\Aplica_OP\\Work\\CMEMS\GLOBAL_ANALYSIS_FORECAST_BIO\Backup")
file_name_bio = "Plataforma_SE_Bio.hdf5"
#file_name_bio ="WaterProperties_2.hdf5"

#####################################################
def read_date():
	global initial_date
	global end_date
	global number_of_runs
	
	forecast_mode = 0
	refday_to_start = 0
	number_of_runs = 0
	
	with open(input_file) as file:
		for line in file:
			if re.search("^FORECAST_MODE.+:", line):
				number = line.split()
				forecast_mode = int(number[2])
				
	if forecast_mode == 1:
		with open(input_file) as file:
			for line in file:
				if re.search("^REFDAY_TO_START.+:", line):
					number = line.split()
					refday_to_start = int(number[2])
				elif re.search("^NUMBER_OF_RUNS.+:", line):
					number = line.split()
					number_of_runs = int(number[2])
					
		initial_date = datetime.datetime.now() + datetime.timedelta(days = refday_to_start)
		end_date = initial_date + datetime.timedelta(days = number_of_runs-1)
		
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
			file_lines[n] = "START " + ": " + str(next_start_date.strftime("%Y %m %d ")) + "0 0 0\n"
			#file_lines[n] = "START " + ": " + str(next_start_date.strftime("%Y %m %d %H %M %S")) + "\n"

		elif re.search("^END.+:", line):	
			file_lines[n] = "END " + ": " + str(next_end_date.strftime("%Y %m %d ")) + "0 0 0\n"
			#file_lines[n] = "END " + ": " + str(next_end_date.strftime("%Y %m %d %H %M %S")) + "\n"
			
	with open(file_name,"w") as file:
		for n in range(0,number_of_lines) :
			file.write(file_lines[n])

#####################################################
def interpolate_gfs():

	os.chdir(interpolate_gfs_dir)
		
	write_date("Interpolate.dat")	
	output = subprocess.call(["Interpolate.bat"])
	
	hdf_files = glob.iglob(os.path.join(interpolate_gfs_dir, file_name_gfs))
	for file in hdf_files:
		shutil.copy(file, boundary_conditions_dir)
	
	files = glob.glob("*.hdf5")
	for filename in files:
		os.remove(filename)		
#####################################################
def copy_initial_files(level):

	initial_files_dir = (backup_dir[level]+"\\"+str(old_start_date.strftime("%Y%m%d")) + "_" + str(old_end_date.strftime("%Y%m%d")))
	
	if os.path.exists(initial_files_dir):
		
		os.chdir(results_dir[level])
		
		files = glob.glob("*.fin*")
		for filename in files:
			os.remove(filename)
		
		files_fin = glob.iglob(os.path.join(initial_files_dir,"*_2.fin*"))
		for file in files_fin:
			if os.path.isfile(file):
				shutil.copy(file, results_dir[level])
					
		files_fin = glob.iglob(os.path.join(results_dir[level],"*_2.fin*"))
		for file in files_fin:
			if os.path.isfile(file):
				os.rename(file, file.replace("_2.fin","_1.fin"))
#####################################################
def backup(level):
	
	backup_dir_date = (backup_dir[level]+"\\"+str(next_start_date.strftime("%Y%m%d")) + "_" + str(next_end_date.strftime("%Y%m%d")))
		
	if not os.path.exists(backup_dir_date):
		os.makedirs(backup_dir_date)
		
	os.chdir(results_dir[level])
	
	files = glob.glob("MPI*.*")
	for filename in files:
		os.remove(filename)
		
	result_files = glob.iglob(os.path.join(results_dir[level],"*.hdf5"))
	for file in result_files:
		shutil.copy(file, backup_dir_date)
		
	fin_files = glob.iglob(os.path.join(results_dir[level],"*_2.fin*"))
	for file in fin_files:
		shutil.copy(file, backup_dir_date)
		
	files = glob.glob("*.fin*")
	for filename in files:
		os.remove(filename)
	
	files = glob.glob("*.hdf5")
	for filename in files:
		os.remove(filename)
#####################################################

read_date()

for run in range (0,number_of_runs):	

	#Update dates
	next_date (run)
	
	#Pre-processing
	#Interpolate GFS		
	#interpolate_gfs ()
				
	#Copy Meteo
	os.chdir(dir_meteo)

	hdf5_files = glob.iglob(os.path.join(dir_meteo,file_name_meteo))
	for file in hdf5_files:
		shutil.copy(file, boundary_conditions_dir)
					
	#Copy ocean boundary conditions
	#Hydrodynamic
	dir_date = (dir_father_phy_results+"\\"+str(next_start_date.strftime("%Y%m%d")) + "_" + str(next_end_date.strftime("%Y%m%d")))
	
	os.chdir(dir_date)
	
	hdf5_files = glob.iglob(os.path.join(dir_date,file_name_phy))
	for file in hdf5_files:
		shutil.copy(file, boundary_conditions_dir)
		
	#Water Properties
	dir_date = (dir_father_bio_results)
	#dir_date = (dir_father_bio_results+"\\"+str(next_start_date.strftime("%Y%m%d")) + "_" + str(next_end_date.strftime("%Y%m%d")))
	
	os.chdir(dir_date)
	
	hdf5_files = glob.iglob(os.path.join(dir_date,file_name_bio))
	for file in hdf5_files:
		shutil.copy(file, boundary_conditions_dir)
		

	##############################################
	#MOHID
	
	#Update dates
	for level in range (0,number_of_domains):
		os.chdir(data_dir [level])
		write_date("Model_2.dat")
	
	#Copy initial files (.fin)	
	old_start_date = next_start_date - datetime.timedelta(days = 1)
	old_end_date = next_end_date - datetime.timedelta(days = 1)
	
	for level in range (0,number_of_domains):
		copy_initial_files(level)
	
	#Run
	os.chdir(exe_dir)
	output = subprocess.call(["run_MPI.bat"])
	
	if not ("Program Mohid Water successfully terminated") in open(mohid_log).read():
		sys.exit ("Program Mohid Water was not successfully terminated"+"\n"+"Check out Mohid log file")
	
	#Backup
	for level in range (0,number_of_domains):
		backup(level)
	