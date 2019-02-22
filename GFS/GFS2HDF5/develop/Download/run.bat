set url_inv=https://nomads.ncdc.noaa.gov/data/gfsanl/201411/20141114/gfsanl_4_20141114_1800_006.inv
set url_grb=https://nomads.ncdc.noaa.gov/data/gfsanl/201411/20141114/gfsanl_4_20141114_1800_006.grb2
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20141114_1800_006_temp.grb2
