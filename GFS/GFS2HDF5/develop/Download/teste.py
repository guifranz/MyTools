import urllib2

url = 'https://nomads.ncdc.noaa.gov/data/gfsanl/201411/20141115/gfsanl_4_20141115_1800_006.inv'

#request = urllib2.Request(url)
#request.get_method = lambda : 'HEAD'
try:
	response = urllib2.urlopen(url)
	print "Exists!"
	
	data = response.read()
	filename = "gfsanl_4_20141115_1800_006.inv"
	file_ = open(filename, 'w')
	file_.write(data)
	file_.close()

except urllib2.HTTPError:
	print "Doesn't Exist!"
