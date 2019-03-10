import os, subprocess

dirpath = os.getcwd()

GFS2HDF5_dir = (dirpath+"\GFS\GFS2HDF5")
CMEMSPHY_dir = (dirpath+"\CMEMS\GLOBAL_ANALYSIS_FORECAST_PHY")
CMEMSBIO_dir = (dirpath+"\CMEMS\GLOBAL_ANALYSIS_FORECAST_BIO")

os.chdir(GFS2HDF5_dir)
output = subprocess.call(["GFS2HDF5.bat"])

os.chdir(CMEMSPHY_dir)
output = subprocess.call(["CMEMS2HDF5.bat"])

os.chdir(CMEMSBIO_dir)
output = subprocess.call(["CMEMS_BIO2HDF5.bat"])