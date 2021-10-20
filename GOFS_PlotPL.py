#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:09:30 2019

@author: emily.niebuhr
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:18:49 2018

@author: Emily.Niebuhr
"""
#  https://stackoverflow.com/questions/8858008/how-to-move-a-file-in-python

#import pyproj



import urllib.request
import sys
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
import shutil 
import sys
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
minLon=176
maxLon=214
minLat=53
maxLat=72
lonThet=195
latThet=72
#SummerGOFS
minLat=60
maxlat=85
minLon=181
maxLon=240


minLon = int(sys.argv[1])
maxLon = int(sys.argv[2])
minLat = int(sys.argv[3])
maxLat = int(sys.argv[4])
lonThet = int(sys.argv[5])
latThet = int(sys.argv[6])





#fcstHour = int(sys.argv[1])
#mos = int(sys.argv[2])
#daye = int(sys.argv[3])
#yr = int(sys.argv[4])

##### ColorBar Differences and IMAGES 
diffMax=1
diffMin=-1
diffNum=20
ftitle= 25

## m=Basemap(projection='stere',lat_0=72, lon_0=200 , llcrnrlon=180, \
#  urcrnrlon=225,llcrnrlat=64,urcrnrlat=77, \
#  resolution='l')
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

print ("GOFS PLOTS PL!")


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







########################## cases study from 5 days ago ############
#x1=datetime.now() - timedelta(days=4)
#x2=datetime.now() - timedelta(days=3)
#x3=datetime.now() - timedelta(days=2)
#x4=datetime.now() - timedelta(days=1)
#x5=datetime.now() 
#x7=datetime.now() + timedelta(days=2)


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





#mos = 7
mos = x.month
#mos = 7

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

#########  Note all of the data is run on 12z the day before- so choose your day one day ahead 
#yr = 2019
#daye = 20
#tom = 21
#day2 = 22
#day3 = 23
#day4 = 24
#day5 = 25
#day7 = 26
####
#########################  Change!!!!!!!!!!!
#yester=19
#ymos=11
#yyear=2019
###
#yester5=14
#yester = 6
#yr = 2019
#daye = 11
#tom = 12
#day2 = 18
#day3 = 19
#day4 = 20
#day5 = 21
#day7 = 22
###
########################  Change!!!!!!!!!!!
#yester=14

#SCRIPTDIR=
##############33 Time to access netcdf files and plot!
dir1 = os.path.abspath('/home/amos/IceOperatePL')
name_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
dir_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
dir2_EL = RASM+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 


os.chdir(dir1+"/"+dir_EL+"/"+dir2_EL)
print (os.getcwd())

###########################################
#####     Case Studies 
#########################################33
#mx1 = 2
#mx5 = 2
#
#
#
#mos = 7


#mos = 3
#####  Note all of the data is run on 12z the day before- so choose your day one day ahead 
#yr = 2019
#daye = 16
#tom = 10
#day2 = 11
#day3 = 12
#day4 = 13
#day5 = 14
#day7 = 15
###
########################  Change!!!!!!!!!!!
#yester=8
#ymos=4
#yyear=2019
##
#yester5=2
#y5mos=4
#y5yr=2019
#y4mos=4
#y3mos=4
#
#y2mos=4
#
#ymos=5
#
#



#yester5 = 

#yester=9
#mos=5
#yyear=2019
#yester=19


ftp_n = "ftp://ftp1.esrl.noaa.gov/RASM-ESRL/ModelOutput/" 
esrl = ftp_n + RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 



gis_NAME = "ShpFile_"+ str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) +".zip"
 

name_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
dir_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
dir2_EL = RASM+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
#
#
#os.path.dirname('/home/emily.niebuhr/Downloads')
#dir1 = os.path.abspath('/home/emily.niebuhr/Downloads')
#os.path.dirname('C:/Users/emily.niebuhr/Downloads/')
#dir1 = os.path.abspath('C:/Users/emily.niebuhr/Downloads/')
os.chdir(dir1)
#
#
os.chdir(dir1+"/"+dir_EL+"/"+dir2_EL)
print ("puppy")
print (os.getcwd())

nam_GOFS = "GOFS3.1_Arctic_" +  str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+gzz
#
##olldd = str(oldDir+nam_GOFS)
##nwldd = str(Curr_Dirr+nam_GOFS)
#
### keep
#copy2((oldDir+nam_GOFS), (Curr_Dirr+nam_GOFS))
#
#os.chdir(Curr_Dirr)
#
#print (os.getcwd())
#
#tarG = tarfile.open(nam_GOFS)
#tarG.extractall(path=(dir1+"/"+dir_EL))
#tarG.close()


######## grab data from 5 days ago 

#nameFTP = ftp_n

#  https://www7320.nrlssc.navy.mil/nesm/GOFS_3.1/GOFS3.1_Arctic_2018112612.tar.gz
###############################

#####################################

######GIOPS Day 3
# Print variables:  nctst_2
#hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t168.nc"
#ncgo_7 = Dataset(hycom, "r", format="NETCDF4")
#
#lat  = ncgo_7.variables['lat'][:]
#lon  = ncgo_7.variables['lon'][:]
#datago7 = ncgo_7.variables['aice'][0,:]
#datago7[datago7==0]=np.nan



#
#
#
#
#
#
########GIOPS Day 3
### Print variables:  nctst_2
hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t168.nc"
ncgo_7 = Dataset(hycom, "r", format="NETCDF4")

lat  = ncgo_7.variables['lat'][:]
lon  = ncgo_7.variables['lon'][:]
datago7 = ncgo_7.variables['aice'][0,:]

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncgo_7.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncgo_7.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD7 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncgo_7.close()
print(str_timeD7)

hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t120.nc"
ncgo_5 = Dataset(hycom, "r", format="NETCDF4")

lat  = ncgo_5.variables['lat'][:]
lon  = ncgo_5.variables['lon'][:]
datago5 = ncgo_5.variables['aice'][0,:]


tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncgo_5.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncgo_5.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD5 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncgo_5.close()

hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t096.nc"
ncgo_4 = Dataset(hycom, "r", format="NETCDF4")

lat  = ncgo_4.variables['lat'][:]
lon  = ncgo_4.variables['lon'][:]
datago4 = ncgo_4.variables['aice'][0,:]


tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncgo_4.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncgo_4.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD4 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncgo_4.close()

hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t072.nc"

ncgo_3 = Dataset(hycom, "r", format="NETCDF4")

lat  = ncgo_3.variables['lat'][:]
lon  = ncgo_3.variables['lon'][:]
datago3 = ncgo_3.variables['aice'][0,:]

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncgo_3.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncgo_3.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD3 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncgo_3.close()

hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t048.nc"

ncgo_2 = Dataset(hycom, "r", format="NETCDF4")

lat  = ncgo_2.variables['lat'][:]
lon  = ncgo_2.variables['lon'][:]
datago2 = ncgo_2.variables['aice'][0,:]


tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncgo_2.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncgo_2.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD2 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncgo_2.close()

hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t024.nc"

ncgo_1 = Dataset(hycom, "r", format="NETCDF4")
lat  = ncgo_1.variables['lat'][:]
lon  = ncgo_1.variables['lon'][:]
datago1 = ncgo_1.variables['aice'][0,:]


tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncgo_1.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncgo_1.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD1 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncgo_1.close()

hycom = "hycom-cice_inst_ARCu0.08_930_"+str(yyear)+str("{:02d}".format(ymos))+str("{:02d}".format(yester))+"12_t000.nc"

ncgo0 = netCDF4.Dataset(hycom)
lat  = ncgo0.variables['lat'][:]
lon  = ncgo0.variables['lon'][:]
datago0 = ncgo0.variables['aice'][0,:]



tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncgo0.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncgo0.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
str_timeD0 = [i.strftime("%Y-%m-%d %H") for i in tvalue]
ncgo0.close()

#data2 = ncRASM1.variables['aice'][:,:]
#data2 = data2[0][:][:]



#icediff = np.subtract(data5.data,data11.data)

##  This adds the mask back in to show where there is no ice 
#icediff[icediff==0]=np.nan

icediff = np.subtract(datago5.data,datago1.data)
icediff[icediff==0]=np.nan

######### Mesh Data   Mask1 = data1 > 0.0  # This works PL  
# ~ does opposite
###############################3
#  This methodology handles if there is no mask 
go1Mask = ma.masked_equal(datago1,0)
go5Mask = ma.masked_equal(datago5,0)


Mask8 = go5Mask.mask & ~go1Mask.mask
Mask9 = ~go5Mask.mask & go1Mask.mask


###########################################################################
###########3 Open file and do silly array math
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
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
titlenew05 = str("GOFS Ice by day"+ str(str_timeD5) )  
plt.title(titlenew05, fontsize=ftitle)
plt.savefig('plot5D_Mesh1_GOFS.png', bbox_inches="tight")

#plt.show(cs)
plt.clf()
plt.cla()
plt.close()



#############
plt.figure(figsize=(14,10))

m=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
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
titlesub05 = str("GOFS Ice Conc Diff "+ str(str_timeD5) + " - " + str(str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)
         
plt.savefig('plot_diff5_GOFS.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()
    

##################################
##  MAke pretty plots and make everything grey

####################  This part eliminates any extra blue!! 

datago2[datago0==0]=np.nan
datago3[datago3==0]=np.nan
datago0[datago0==0]=np.nan
datago1[datago1==0]=np.nan
datago4[datago4==0]=np.nan
datago5[datago5==0]=np.nan
datago7[datago7==0]=np.nan


plt.figure(figsize=(14,10))


m=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

cat =m.pcolormesh(x,y,datago5,shading='flat', cmap=cmap)
   
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
title5 = str("Ice Conc GOFS"+ str(str_timeD5))  
plt.title(title5, fontsize=ftitle)
plt.savefig('GOFS_goDay5.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()


##################################

plt.figure(figsize=(14,10))


m=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

cats =m.pcolormesh(x,y,datago7,shading='flat', cmap=cmap)
   
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
plt.colorbar(cats,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)
   
  
  ######## Save first plot  
title5 = str("Ice Conc GOFS"+ str(str_timeD7))  
plt.title(title5, fontsize=ftitle)
plt.savefig('GOFS_goDay7.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()




##################################

plt.figure(figsize=(14,10))


m=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')

x, y = m(*np.meshgrid(lon,lat))

cats =m.pcolormesh(x,y,datago0,shading='flat', cmap=cmap)
   
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
plt.colorbar(cats,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)
   
  
  ######## Save first plot  
title5 = str("Ice Conc GOFS"+ str(str_timeD0))  
plt.title(title5, fontsize=ftitle)
plt.savefig('GOFS_INIT.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()




############################### Plot DAy one and Day 2

plt.figure(figsize=(14,10))


m=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')


x, y = m(*np.meshgrid(lon,lat))

cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
bird =m.pcolormesh(x,y,datago1,shading='flat', cmap=cmap)
   
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
title11 = str("Ice Conc GOFS"+ str(str_timeD1))  
plt.title(title11, fontsize=ftitle)
plt.savefig('GOFS_goDay1.png', bbox_inches="tight")
#plt.show()
   # plt.gcf().clear()
plt.clf()
plt.cla()
plt.close()




############################### Plot DAy one and Day 2

plt.figure(figsize=(14,10))


md=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')


x, y = md(*np.meshgrid(lon,lat))

cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
lion2 =md.pcolormesh(x,y,datago2,shading='flat', cmap=cmap)
   
md.drawmapboundary(fill_color='dimgrey')
md.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
md.drawparallels(par, linewidth=0.5, dashes=[1, 5])
md.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
md.drawcoastlines()
md.drawmapboundary()
md.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
md.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
plt.clim(0, 1.1);

##3 Second way to color bar:,  cmap=cmap
plt.colorbar(lion2,orientation='vertical', shrink=0.5)
title11 = str("Ice Conc GOFS"+ str(str_timeD2))  
plt.title(title11, fontsize=ftitle)
plt.savefig('GOFS_goDay2.png', bbox_inches="tight")
#plt.show()
   # plt.gcf().clear()
plt.clf()
plt.cla()
plt.close()


############################### Plot DAy one and Day 2

plt.figure(figsize=(14,10))


mff=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')


x, y = mff(*np.meshgrid(lon,lat))

cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
lion =mff.pcolormesh(x,y,datago3,shading='flat', cmap=cmap)
   
mff.drawmapboundary(fill_color='dimgrey')
mff.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
mff.drawparallels(par, linewidth=0.5, dashes=[1, 5])
mff.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
mff.drawcoastlines()
mff.drawmapboundary()
mff.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
mff.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
plt.clim(0, 1.1);

##3 Second way to color bar:,  cmap=cmap
plt.colorbar(lion,orientation='vertical', shrink=0.5)
title11 = str("Ice Conc GOFS"+ str(str_timeD3))  
plt.title(title11, fontsize=ftitle)
plt.savefig('GOFS_goDay3.png', bbox_inches="tight")
#plt.show()
   # plt.gcf().clear()
plt.clf()
plt.cla()
plt.close()

############################### Plot DAy one and Day 2

plt.figure(figsize=(14,10))


mf=Basemap(projection='stere',lat_0=72, lon_0=lonThet , llcrnrlon=minLon, \
  urcrnrlon=maxLon,llcrnrlat=minLat,urcrnrlat=maxLat, \
  resolution='h')


x, y = mf(*np.meshgrid(lon,lat))

cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
lion3 =mf.pcolormesh(x,y,datago4,shading='flat', cmap=cmap)
   
mf.drawmapboundary(fill_color='dimgrey')
mf.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
mf.drawparallels(par, linewidth=0.5, dashes=[1, 5])
mf.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
mf.drawcoastlines()
mf.drawmapboundary()
mf.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
mf.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
plt.clim(0, 1.1);

##3 Second way to color bar:,  cmap=cmap
plt.colorbar(lion3,orientation='vertical', shrink=0.5)
title11 = str("Ice Conc GOFS"+ str(str_timeD4))  
plt.title(title11, fontsize=ftitle)
plt.savefig('GOFS_goDay4.png', bbox_inches="tight")
#plt.show()
   # plt.gcf().clear()
plt.clf()
plt.cla()
plt.close()
