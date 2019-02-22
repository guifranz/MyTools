import os

path = "D:\CMEMS\Plataforma_SE\GLOBAL_ANALYSIS_FORECAST_BIO\Backup"
file_name = "ConvertToHDF5Action.dat"

with open(file_name,"w") as file:
	file.write("<begin_file>\n")
	file.write("ACTION                   : GLUES HDF5 FILES\n")
	file.write("OUTPUTFILENAME           : Plataforma_SE_Bio.hdf5\n")
	file.write("<<begin_list>>\n")
	for filename in os.listdir(path):
		print(path + "\\" + filename + "\\Plataforma_SE_Bio.hdf5")
		file.write(path + "\\" + filename + "\\Plataforma_SE_Bio.hdf5")
		file.write("\n")
	file.write("<<end_list>>\n")
	file.write("<end_file>\n")