#!/usr/bin/env python3

######## Image Download Time ######################

import sys
import numpy as np
import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.mlab as mlab
import numpy as np
import urllib.request
import tarfile
import datetime
import os
#from scipy.ndimage.filters import gaussian_filter

import urllib.request
import tarfile
from datetime import datetime, timedelta
from shutil import copy2
import os
import matplotlib as mpl
#import matplotlib; matplotlib.pyplot.switch_backend('agg')
import matplotlib; matplotlib.use('agg') 
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
import numpy as np

from docx import Document
from docx.shared import Inches
import math
import mpl_toolkits.basemap as basemap

import shutil

from docx.shared import Inches
import mpl_toolkits.basemap as basemap
from PIL import Image

from docx import Document
from docx.shared import Inches

# Image parameters
bounds = [  0.1, 0.3 , 0.4, 0.6, 0.7, 0.8, 0.9, 1.0]
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])


##############################
## Webname
############################

RASM= str("RASM-ESRL_")
RASM_N= str("RASM-ESRL_4NIC_")

tg=str("-")
dg=str("-")
nc = str(".nc")
gzz = str(".tar.gz")

#####  DATES
x = datetime.now() 
x1=datetime.now() + timedelta(days=1)
x2=datetime.now() + timedelta(days=2)
x3=datetime.now() + timedelta(days=3)
x4=datetime.now() + timedelta(days=4)
x5=datetime.now() + timedelta(days=5)
x7=datetime.now() + timedelta(days=7)



mx1 = datetime.now() - timedelta(days=1)
mx2 = datetime.now() - timedelta(days=2)
mx3 = datetime.now() - timedelta(days=3)
mx4 = datetime.now() - timedelta(days=4)
mx5 = datetime.now() - timedelta(days=5)
mx6 = datetime.now() - timedelta(days=6)

mx8 = datetime.now() - timedelta(days=8)
########################## cases study from 5 days ago ############
mx1 = datetime.now() - timedelta(days=1)
mx5 = datetime.now() - timedelta(days=5)
mx8 = datetime.now() - timedelta(days=8)

mp1=x1.month
mp2=x2.month
mp3=x3.month
mp4=x4.month
mp5=x5.month
mp7=x7.month

yp1=x1.year
yp2=x2.year
yp3=x3.year
yp4=x4.year
yp5=x5.year
yp7=x7.year

mos = x.month
yr = x.year
daye = x.day

tom = x1.day
day2 = x2.day
day3 = x3.day
day5 = x5.day
day4 = x4.day
day7 = x7.day

#####################  
yester=mx1.day
ymos=mx1.month
yyear=mx1.year

yester5=mx5.day
y5mos=mx5.month
y5yr=mx5.year



##########################
# ESRL FILES
#############################
##

############## Change depending on wheather windows or linux machine 
#os.path.dirname('/home/emily.niebuhr/Downloads')
dir1 = os.path.abspath('/home/emily.niebuhr/Downloads')
dir1 = os.path.abspath('/home/amos/IceOperatePL')
os.chdir(dir1)

ftp_n = "ftp://ftp1.esrl.noaa.gov/RASM-ESRL/ModelOutput/" 
esrl = ftp_n + RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
gis_NAME = "ShpFile_"+ str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) +".zip"
 
name_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
dir_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
dir2_EL = RASM+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 

#####################  Change!!!!!!!!!!!

yester2=mx2.day
y2mos=mx2.month
y2yr=mx2.year

yester3=mx3.day
y3mos=mx3.month
y3yr=mx3.year

yester4=mx4.day
y4mos=mx4.month
y4yr=mx4.year

yester5=mx5.day
y5mos=mx5.month
y5yr=mx5.year


os.chdir(dir1+"/"+dir_EL+"/"+dir2_EL)
print (os.getcwd())


num = int("15")
ftitle = int("15")
wvhgt = int("1")
wndhgt = int("50")

i = 0

#
hourNumber=int(132)



ww3 = "ak"
fcstHour = int(12)

print(fcstHour)
############# Lat Long

hList = ["f024", "f048", "f072", "f144"]


datename = str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(daye))
########################  Plot the data  ##################3333
#i = 0
for i in hList:
    
#for k in fruit: #or k range(grb):
    plt.figure()
#rtofs_glo.t00z.f024_bering_std.grb2
    RBER_Name= str("rtofs_BER_conc_")+str(i) +str("_")+datename+str(".grib2")
    RBER_Name= str("rtofs_BER_conc_")+str(i) +str("_")+datename+str(".grib2")
    RARC_Name= str("rtofs_ARC_conc_")+str(i) +str("_")+datename+str(".grib2")
    gribB = RBER_Name
    gribA = RARC_Name
    
    print(gribB)
    print(gribA)
    print(fcstHour)
    grbsA=pygrib.open(gribA)
    grbsB=pygrib.open(gribB)
    for g in grbsA:
        print(g.name)
    print(grbsA)
    grbA = grbsA.select(name='Sea ice area fraction')[0]
    grbB = grbsB.select(name='Sea ice area fraction')[0]
    dataA=(grbA.values)
    dataB=(grbB.values)
    dataB[dataB==0]=np.nan
    dataA[dataA==0]=np.nan
    dater = (grbB.validDate)
    lat,lon = grbB.latlons()
    latA,lonA = grbA.latlons()
  
    minLon=176
    maxLon=214
    minLat=53
    maxLat=72
    lonThet=195
    latThet=72
    
    minLon=172
    maxLon=218
    minLat=48
    maxLat=70
    lonThet=195
    latThet=72
    bounds = [  0.1, 0.3 , 0.4, 0.6, 0.7, 0.8, 0.9, 1.0]
    cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])

    minLon = int(sys.argv[1])
    maxLon = int(sys.argv[2])
    minLat = int(sys.argv[3])
    maxLat = int(sys.argv[4])
    lonThet = int(sys.argv[5])
    latThet = int(sys.argv[6])
    
    print(dataB)
    print(lon.min())
    print(dater)
    print("WW3")
   
    m=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

    x, y = m(lon,lat) 
    xA, yA = m(lonA,latA)
    cs = m.pcolormesh(x,y,dataB,shading='flat',cmap=cmap)
    csA = m.pcolormesh(xA,yA,dataA,shading='flat',cmap=cmap)
   # m.drawcoastlines(linewidth=5)
    m.drawcoastlines()
    m.fillcontinents()
    m.drawmapboundary(fill_color='dimgrey')
    m.fillcontinents(color='lightgray', lake_color='darkgrey')
    m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
    titleb="RTOFS Data " + str(dater) 
    plt.title(titleb, fontsize=ftitle) 
    figName100DU = "RTOFS_" + str(i) +".png"  
 #   pupppy=   plt.contour(x,y,dataB, levels = range(0,50,5), colors='k',interpolation='none')
 #   plt.clabel(pupppy)
    plt.clim(0.0, 1.1);

    plt.colorbar(cs,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)
    #plt.colorbar(cs,orientation='vertical')
    plt.savefig(figName100DU, bbox_inches="tight")

######3 Need to clear everything here: 
 #   plt.show()
    plt.clf()
    plt.cla()
    plt.close()
    
   

    
    



################# EXTRA Relv code #############3

   
#    for g in grbs:
#        print(g.level, g.name, g.typeOfLevel, g.forecastTime, g.discipline, g.parameterCategory, g.parameterNumber, g.typeOfFirstFixedSurface )       
#
#    fieldx = pygrib.index(WW3grb_Name,'name','level')
##    print(file1)
#    Wgrb=fieldx.select(name="Wind speed",level="10")
#    Wdata=(Wgrb[0]['values'])*1.4
#    
  


