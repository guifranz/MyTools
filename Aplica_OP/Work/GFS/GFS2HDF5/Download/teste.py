#import urllib2

from urllib.error import HTTPError
from urllib.request import urlopen

url = 'https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2019022300/gfs.t00z.pgrb2.0p25.f000'

#request = urllib2.Request(url)
#request.get_method = lambda : 'HEAD'
try:
	response = urlopen(url)
	print ("Exists!")
	
	data = response.read()
	filename = "teste"
	file_ = open(filename, 'wb')
	file_.write(data)
	file_.close()

except HTTPError:
	print ("Doesn't Exist!")
