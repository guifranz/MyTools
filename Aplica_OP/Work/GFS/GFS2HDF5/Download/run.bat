set url_inv=https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2019030418/gfs.t18z.pgrb2.0p50.f003.idx
set url_grb=https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2019030418/gfs.t18z.pgrb2.0p50.f003
PERL get_inv.pl %url_inv% | egrep "(:TMP:2 m above|:UGRD:10 m above|:VGRD:10 m above|:RH:2 m above|:PRMSL:|:LAND:|:TCDC:entire atmosphere|:DLWRF:surface|:DSWRF:surface|:PRATE:surface|:HPBL:surface|:ALBDO:surface)" | PERL get_grib.pl %url_grb% 20190304gfs.t18z.pgrb2.0p50.f003_temp.grb2
