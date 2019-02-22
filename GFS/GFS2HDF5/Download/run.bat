set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110101/gfsanl_4_20110101_1800_006.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110101/gfsanl_4_20110101_1800_006.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110101_1800_006_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0000_003.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0000_003.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_0000_003_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0000_006.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0000_006.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_0000_006_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0600_003.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0600_003.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_0600_003_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0600_006.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_0600_006.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_0600_006_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1200_003.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1200_003.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_1200_003_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1200_006.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1200_006.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_1200_006_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1800_003.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1800_003.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_1800_003_temp.grb2
set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1800_006.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201101/20110102/gfsanl_4_20110102_1800_006.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20110102_1800_006_temp.grb2
