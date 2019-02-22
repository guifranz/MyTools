import os, re, subprocess

input_file_name = "InputConvertToHDF5Action.dat"
output_file_name = "ConvertToHDF5Action.dat"


with open(input_file_name,"r") as infile:
	with open(output_file_name,"w") as outfile:
		for line in infile:
			outfile.write(line)
			if re.search("<<begin_input_files>>", line):
				break
		
		for file in os.listdir(os.curdir):
			if file.endswith(".nc"):
				outfile.write(file+"\n")
		
		outfile.write("<<end_input_files>>\n")
		outfile.write("<end_file>\n")
		
output = subprocess.call(["ConvertToHdf5_release_single.exe"])