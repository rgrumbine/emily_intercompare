"""
Created on Tue Oct 30 10:14:08 2018

@author: Emily.Niebuhr
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:18:49 2018

@author: Emily.Niebuhr
"""
#  https://stackoverflow.com/questions/8858008/how-to-move-a-file-in-python

import urllib.request
import tarfile
import sys
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
import shutil 

from netCDF4 import Dataset,  num2date
import math
import numpy.ma as ma
import netCDF4

import mpl_toolkits.basemap as basemap
from PIL import Image

from docx import Document
from docx.shared import Inches


bounds = [  0.1, 0.3 , 0.4, 0.6, 0.7, 0.8, 0.9, 1.0]
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])



def polar_stere(lon_w, lon_e, lat_s, lat_n, **kwargs):
    '''Returns a Basemap object (NPS/SPS) focused in a region.

    lon_w, lon_e, lat_s, lat_n -- Graphic limits in geographical coordinates.
                                  W and S directions are negative.
    **kwargs -- Aditional arguments for Basemap object.

    '''
    lon_0 = lon_w + (lon_e - lon_w) / 2.
    ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
    lat_0 = math.copysign(90., ref)
    proj = 'npstere' if lat_0 > 0 else 'spstere'
    prj = basemap.Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                          boundinglat=0, resolution='h')
    #prj = pyproj.Proj(proj='stere', lon_0=lon_0, lat_0=lat_0)
    lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
    lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
    x, y = prj(lons, lats)
    ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
    ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
    return basemap.Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                           llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                           urcrnrlon=ur_lon, urcrnrlat=ur_lat, **kwargs);



##############################3
#  Latitude
###############

### GOFS
#minLon=180
#maxLon=214
#minLat=57
#maxLat=67
#lonThet=195
#latThet=72
#
### GIOPS
#minGLon=-180
#maxGLon=-157
#minGLat=57
#maxGLat=67
#lonThet=195


## GOFS
minLon=180
maxLon=214
minLat=56
maxLat=73
lonThet=195
latThet=72

## GIOPS
minGLon=-180
maxGLon=-157
minGLat=56
maxGLat=73
lonThet=195


## GOFS
## GOFS Summer
minLon=176
maxLon=249
minLat=63
maxLat=80
lonThet=195
latThet=72

minLon = int(sys.argv[1])
maxLon = int(sys.argv[2])
minLat = int(sys.argv[3])
maxLat = int(sys.argv[4])
lonThet=int(sys.argv[5])
latThet=int(sys.argv[6])
##### ColorBar Differences and IMAGES 
diffMax=1
diffMin=-1
diffNum=20
ftitle= 25

##############
D1 = "t024"
D2 = "t048"
D3 = "t072"
D4 = "t096"
D5 = "t120"
D6 = "t144"
D7 = "t144"
D8 = "t192"
D10 = "t216"

print ("RASM-ESRL PLOTS PL!")


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




print ("RASM ESRL Thickness PL!")



########################## cases study from 5 days ago ############
mx1 = datetime.now() - timedelta(days=1)
mx2 = datetime.now() - timedelta(days=2)

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

#####################  Change!!!!!!!!!!!
yester=mx1.day
ymos=mx1.month
yyear=mx1.year

yester5=mx5.day




yester22=mx2.day
ymos22=mx2.month
yyear22=mx2.year



y5mos=mx5.month
y5yr=mx5.year

###########################################
#####     Case Studies 
#########################################33

dir1 = os.path.abspath('/home/emily.niebuhr/Downloads')
dir1 = os.path.abspath('/home/amos/IceOperatePL')
#os.path.dirname('C:/Users/emily.niebuhr/Downloads/')
#dir1 = os.path.abspath('C:/Users/emily.niebuhr/Downloads/')
os.chdir(dir1)

ftp_n = "ftp://ftp1.esrl.noaa.gov/RASM-ESRL/ModelOutput/" 
esrl = ftp_n + RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
gis_NAME = "ShpFile_"+ str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) +".zip"
 
name_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
dir_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
dir2_EL = RASM+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 

f1GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D1)+nc
f2GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D2)+nc
f5GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D5)+nc
f6GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D6)+nc
f7GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D7)+nc
ftenGIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D10)+nc

######################## Plot Module ##############################
##############33 Time to access netcdf files and plot!

os.chdir(dir1+"/"+dir_EL+"/"+dir2_EL)
print (os.getcwd())

plt.figure()
#
ncRASM5= netCDF4.Dataset(f5GIO)
lat  = ncRASM5.variables['lat'][:]
lon  = ncRASM5.variables['lon'][:]
data5 = ncRASM5.variables['aice'][0,:]

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncRASM5.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRASM5.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD5 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncRASM5.close()
# open and read in data from second nc file
# since the grid is the same as the first, dont need lat lons from this file
print(tvalue)
print(str_timeD5)

ncRASM1 = netCDF4.Dataset(f1GIO)
#print(ncfile2)

lat  = ncRASM1.variables['lat'][:]
lon  = ncRASM1.variables['lon'][:]
data11 = ncRASM1.variables['aice'][0,:]

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncRASM1.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRASM1.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD1 = [i.strftime("%Y-%m-%d %H") for i in tvalue]

##### To refer to data and no mask, simply do data1.data
#icediff = np.subtract(data5,data11)
icediff = np.subtract(data5.data,data11.data)

##  This adds the mask back in to show where there is no ice 
icediff[icediff==0]=np.nan
ncRASM1.close()

######### Mesh Data   Mask1 = data1 > 0.0  # This works PL  

# ~ does opposite
Mask8 = data5.mask & ~data11.mask
Mask9 = ~data5.mask & data11.mask



###########################################################################
###########3 Open file and do silly array math
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

# keep
cs =m.pcolormesh(x,y,Mask8,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
plt.clim(-.9, .9);
plt.colorbar(cs,orientation='vertical', shrink=0.5)
   
#########norm = matplotlib.colors.BoundaryNorm(np.arange(-1,1,0.2), cmap.N)
titlenew05 = str("ESRL New Ice by day"+ str(str_timeD5) )  
plt.title(titlenew05, fontsize=ftitle)
plt.savefig('plot5D_Mesh1_ESRL.png', bbox_inches="tight")

#plt.show(cs)
plt.clf()
plt.cla()
plt.close()
#############
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

dog =m.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu', diffNum))
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(diffMax,diffMin);
plt.colorbar(dog,orientation='vertical', shrink=0.5)
   
 ######## Save first plot  
titlesub05 = str("ESRL Ice Conc Diff"+ str(str_timeD5) + " - " + str(str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)
         
plt.savefig('plot_diff5_ESRL2.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()
    


############################### Plot DAy one and Day 2
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

cat =m.pcolormesh(x,y,data5,shading='flat', cmap=cmap)
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(0.0, 1.1);
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
plt.colorbar(cat,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)
   
  
  ######## Save first plot  
title5 = str("Ice Conc ESRL"+ str(str_timeD5))  
plt.title(title5, fontsize=ftitle)
plt.savefig('plot_Day5_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()

############################### Plot DAy one and Day 2

plt.figure(figsize=(14,10))


m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')


x, y = m(*np.meshgrid(lon,lat))

cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
bird =m.pcolormesh(x,y,data11,shading='flat', cmap=cmap)
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
plt.clim(0, 1.1);

##3 Second way to color bar:,  cmap=cmap
plt.colorbar(bird,orientation='vertical', shrink=0.5)
title11 = str("Ice Conc ESRL "+ str(str_timeD1))  
plt.title(title11, fontsize=ftitle)
plt.savefig('plot_Day1_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()


################################################################
####################### Plot for DAy 10 

ncRASM10= netCDF4.Dataset(ftenGIO)
lat  = ncRASM10.variables['lat'][:]
lon  = ncRASM10.variables['lon'][:]
data10 = ncRASM10.variables['aice'][0,:]


###########3 Open file and do silly array math
nctime = ncRASM10.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRASM10.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD10 = [i.strftime("%Y-%m-%d %H") for i in tvalue]


print(str_timeD10)
ncRASM10.close()

##  This adds the mask back in to show where there is no ice 
#icediff[icediff==0]=np.nan


icediff = np.subtract(data10.data,data11.data)
icediff[icediff==0]=np.nan

######### Mesh Data Mask1 = data1 > 0.0  # This works PL
# ~ does opposite
Mask7 = data10.mask & ~data11.mask
Mask10 = ~data10.mask & data11.mask


###########################################################################
## Plot to show new ice growth
#####################################################
#cs =nps.pcolormesh(x,y,Mask10,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))

plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

# keep
x, y = m(*np.meshgrid(lon,lat))
cs =m.pcolormesh(x,y,Mask7,shading='flat', cmap=plt.cm.get_cmap('RdBu', 5))

    
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
    
cmap=plt.cm.get_cmap('RdBu', 5)
cmap=plt.cm.RdBu
  
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(-.9, .9);
## color bar does not really make sense here- just included 
plt.colorbar(cs,orientation='vertical', shrink=0.5)
   
####norm = matplotlib.colors.BoundaryNorm(np.arange(-1,1,0.2))
titlenew10 = str("New Ice ESRL"+ str(str_timeD10) )  
plt.title(titlenew10, fontsize=ftitle)
plt.savefig('plot10D_Mesh1_ESRL.png', bbox_inches="tight")

#plt.show(cs)
plt.clf()
plt.cla()
plt.close()


#############
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')


x, y = m(*np.meshgrid(lon,lat))
dog =m.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu', diffNum))
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(diffMin,diffMax);
plt.colorbar(dog,orientation='vertical', shrink=0.5)
      ######## Save first plot  
titlesub10 = str("Ice Conc Diff"+ str(str_timeD10) + " - " + str(str_timeD1))  
plt.title(titlesub10, fontsize=ftitle)

plt.savefig('plot_diff10_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()
    


############################### Plot DAy one and Day 2
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')


x, y = m(*np.meshgrid(lon,lat))
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])

cat =m.pcolormesh(x,y,data10,shading='flat', cmap=cmap)
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0, 1.1);

##3 Second way to color bar:,  cmap=cmap
plt.colorbar(cat,orientation='vertical', shrink=0.5)

  ######## Save first plot
title10 = str("Ice Conc ESRL"+ str(str_timeD10))  
plt.title(title10, fontsize=ftitle) # Set the name of the variable to plot

plt.savefig('plot_Day10_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()


##########################################################
######################  EXTRA ESRL DAYS - No subtraction
##########################################################

f2GIO = str(RASM)+str(yr)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D2)+nc
f3GIO = str(RASM)+str(yr)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D3)+nc
f4GIO = str(RASM)+str(yr)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D4)+nc

##############  ESRL Day 2
ncRASM2 = Dataset(f3GIO, "r")

#ncRASM2= Dataset(f3GIO)
lats  = ncRASM2.variables['lat'][:]
lons  = ncRASM2.variables['lon'][:]
data22 = ncRASM2.variables['aice'][0,:]


###########3 Open file and do silly array math
nctime = ncRASM2.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRASM2.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD2 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncRASM2.close()

######   Plot the image
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lons,lats))

cows =m.pcolormesh(x,y,data22,shading='flat', cmap=cmap)
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
# 
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0.0, 1.1);
plt.colorbar(cows,orientation='vertical', shrink=0.5)

  ######## Save first plot  

title1 = str("Ice Conc ESRL"+ str(str_timeD2))  
plt.title(title1, fontsize=ftitle)
plt.savefig('plot_Day2_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()

##############  Difference
#################### Difference Day 1 and 2

icediff = np.subtract(data22.data,data11.data)
icediff[icediff==0]=np.nan

######### Mesh Data   Mask1 = data1 > 0.0  # This works PL  
# ~ does opposite
Mask8 = data22.mask & ~data11.mask
Mask9 = ~data22.mask & data11.mask


###########################################################################
###########3 Open file and do silly array math
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

cs =m.pcolormesh(x,y,Mask9,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))

    
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(-.9, .9);
plt.colorbar(cs,orientation='vertical', shrink=0.5)
   
#########norm = matplotlib.colors.BoundaryNorm(np.arange(-1,1,0.2), cmap.N)
titlenew05 = str("New Ice by day"+ str(str_timeD2) )  
plt.title(titlenew05, fontsize=ftitle)
plt.savefig('plot5D_Mesh2_ESRL.png', bbox_inches="tight")
#plt.show(cs)
plt.clf()
plt.cla()
plt.close()



#############
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

dog =m.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu', diffNum))
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(diffMin, diffMax);
plt.colorbar(dog,orientation='vertical', shrink=0.5)
   
 ######## Save first plot  
titlesub05 = str("Ice Conc Diff ESRL"+ str(str_timeD2) + " - " + str(str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)     
plt.savefig('plot_diff2_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()
    

# 33333333333333333333333333333333333333333333333333333333333333333
############  ESRL Day 3
#ncRASM3= Dataset(f4GIO)
ncRASM3 = Dataset(f4GIO, "r")
lats  = ncRASM3.variables['lat'][:]
lons  = ncRASM3.variables['lon'][:]
data33 = ncRASM3.variables['aice'][0,:]

###########3 Open file and do silly array math
nctime = ncRASM3.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRASM3.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD3 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncRASM3.close()


######   Plot the image
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lons,lats))


cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
horse =m.pcolormesh(x,y,data33,shading='flat', cmap=cmap)
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0.0, 1.1);
plt.colorbar(horse,orientation='vertical', shrink=0.5)

  ######## Save first plot  

title1 = str("Ice Conc ESRL"+ str(str_timeD3))  
plt.title(title1, fontsize=ftitle)
plt.savefig('plot_Day3_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()

icediff = np.subtract(data33.data,data11.data)
#ncRASM1.close()
icediff[icediff==0]=np.nan

######### Mesh Data   Mask1 = data1 > 0.0  # This works PL  
# ~ does opposite
Mask8 = data33.mask & ~data11.mask
Mask9 = ~data33.mask & data11.mask



###########################################################################
###########3 Open file and do silly array math
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))
cs =m.pcolormesh(x,y,Mask9,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))

    
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
    
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(-.9, .9);
plt.colorbar(cs,orientation='vertical', shrink=0.5)
   
#########norm = matplotlib.colors.BoundaryNorm(np.arange(-1,1,0.2), cmap.N)
titlenew05 = str("New Ice by day"+ str(str_timeD3) )  
plt.title(titlenew05, fontsize=ftitle)
plt.savefig('plot5D_Mesh3_ESRL.png', bbox_inches="tight")

#plt.show(cs)
plt.clf()
plt.cla()
plt.close()



#############
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))
dog =m.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu', diffNum))
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(diffMin,diffMax);
plt.colorbar(dog,orientation='vertical', shrink=0.5)
   
 ######## Save first plot  
titlesub05 = str("Ice Conc Diff ESRL"+ str(str_timeD3) + " - " + str(str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)
         
plt.savefig('plot_diff3_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()
    
################  ESRL Day 4
ncRASM4 = Dataset(f4GIO, "r")

#ncRASM4= Dataset(f5GIO)
lats  = ncRASM4.variables['lat'][:]
lons  = ncRASM4.variables['lon'][:]
data4 = ncRASM4.variables['aice'][0,:]

###########3 Open file and do silly array math
nctime = ncRASM4.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRASM4.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD4 = [i.strftime("%Y-%m-%d %H") for i in tvalue]

ncRASM4.close()

######   Plot the image
plt.figure(figsize=(14,10))


m=Basemap(projection='stere',lat_0=latThet, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lons,lats))

cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
pony =m.pcolormesh(x,y,data4,shading='flat', cmap=cmap)
   
m.drawmapboundary(fill_color='dimgrey')
m.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
m.drawparallels(par, linewidth=0.5, dashes=[1, 5])
m.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
# 
m.drawcoastlines()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0.0, 1.1);
plt.colorbar(pony,orientation='vertical', shrink=0.5)

  ######## Save first plot  

title1 = str("Ice Conc ESRL"+ str(str_timeD4))  
plt.title(title1, fontsize=ftitle)
plt.savefig('plot_Day4_ESRL.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()





