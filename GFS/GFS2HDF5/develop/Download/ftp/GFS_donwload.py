import os
from ftplib import FTP
 
ftp = FTP("nomads.ncdc.noaa.gov")
ftp.login()
ftp.cwd("GFS/analysis_only/201403/201403024")

filematch='*.grb2'

for filename in ftp.nlst(filematch):
    fhandle=open(filename, 'wb')
    print 'Getting ' + filename
    ftp.retrbinary('RETR '+ filename, fhandle.write)
    fhandle.close()

ftp.quit()
