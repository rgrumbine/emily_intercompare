#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:29:46 2019

@author: emily.niebuhr
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:18:49 2018

@author: Emily.Niebuhr
"""
#  https://stackoverflow.com/questions/8858008/how-to-move-a-file-in-python

#import pyproj

#from ftplib import FTP
#import pyproj
##  wget --user='nrltransfer' --password='NESM2017!' --no-check-certificate https://www7320.nrlssc.navy.mil/nesm/GOFS_3.1/GOFS3.1_Arctic_2019030512.tar.gz


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
                          boundinglat=0, resolution='c')
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
## GIOPS  WINTER
minGLon=-180
maxGLon=-157
minGLat=56
maxGLat=73
lonThet=195

minGLon=-180
maxGLon=-157
## GIOPS  SUMMER
minGLon=-185
maxGLon=-135
minGLat=65
maxGLat=80
#lonThet=195


minGLon = int(sys.argv[1])
maxGLon = int(sys.argv[2])
minGLat = int(sys.argv[3])
maxGLat = int(sys.argv[4])


#m=Basemap(projection='stere',lat_0=72, lon_0=200 , llcrnrlon=180, \
#  urcrnrlon=225,llcrnrlat=64,urcrnrlat=77, \
#  resolution='l')

##### ColorBar Differences and IMAGES 
diffMax=1
diffMin=-1
diffNum=20
ftitle= 25
ThNum=11
## 
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



print ("GIO RIO PLOTS Thickness PL!")




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




cmap=plt.cm.get_cmap('PRGn', ThNum)


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

yester22=mx2.day
ymos2=mx2.month
yyear2=mx2.year


yester5=mx5.day




y5mos=mx5.month
y5yr=mx5.year

###########################################
#####     Case Studies 
#########################################33
#mx1 = 2
#mx5 = 2
#
#
#
##mos = 7
##mos = 7
#########  Note all of the data is run on 12z the day before- so choose your day one day ahead 
#yr = 2019
#daye = 9
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
#ymos=4



#




##########################
# ESRL FILES
#############################
##
# GOFS  https://www7320.nrlssc.navy.mil/GLBhycomcice1-12/navo/arc_list_beauforticen.html

############## Change depending on wheather windows or linux machine 
os.path.dirname('/home/emily.niebuhr/Downloads')
dir1 = os.path.abspath('/home/emily.niebuhr/Downloads')
dir1 = os.path.abspath('/home/amos/IceOperatePL')
#os.path.dirname('C:/Users/emily.niebuhr/Downloads/')
#dir1 = os.path.abspath('C:/Users/emily.niebuhr/Downloads/')
os.chdir(dir1)


ftp_n = "ftp://ftp1.esrl.noaa.gov/RASM-ESRL/ModelOutput/" 
esrl = ftp_n + RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 

name_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
dir_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
dir2_EL = RASM+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 

f1GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D1)+nc
f2GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D2)+nc
f5GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D5)+nc
f6GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D6)+nc
f7GIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D7)+nc
ftenGIO = str(RASM)+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+tg+str("00_")+str(D10)+nc


#############################
####### KEEP
############ Download the correct file with tar.gz 

#pltry =  urllib.request.urlretrieve(esrl,name_EL)


#tar = tarfile.open(name_EL)
#tar.extractall(path=(dir1+"/"+dir_EL))
#tar.close()

#################################
#  RASM ESRL PRoblem: experimental so new data is available during the day
#  So initial condition is really day 2 ** 

######################## Plot Module ##############################
##############33 Time to access netcdf files and plot!
#dir1 = os.path.abspath('/home/emily.niebuhr/Downloads')
name_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
dir_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
dir2_EL = RASM+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 


os.chdir(dir1+"/"+dir_EL+"/"+dir2_EL)
print (os.getcwd())








######################## Plot Module ##############################
##############33 Time to access netcdf files and plot!
## Include Change Directory
##
#os.chdir(dir+"/"+dir_EL+"/"+dir2_EL)
#print (os.getcwd())
#GIO =  urllib.request.urlretrieve(GIOD5,"GIO5.nc")

ncGIO5 = Dataset("GIO5th.nc", "r", format="NETCDF4")
print(ncGIO5.variables.keys())
tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncGIO5.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO5.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_timeD5 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncGIO5.variables['latitude'][:,:]
lons =ncGIO5.variables['longitude'][:,:]

datag5 = ncGIO5.variables['iicevol'][:,:]
datag5 = datag5[0][:][:]
ncGIO5.close()
# open and read in data from second nc file
# since the grid is the same as the first, dont need lat lons from this file

ncGIO1 = Dataset("GIO001th.nc", "r", format="NETCDF4")
nctime = ncGIO1.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO1.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_timeD1 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

datag1 = ncGIO1.variables['iicevol'][:,:]
datag1 = datag1[0][:][:]
ncGIO1.close()

#ma.set_fill_value(datag1,0)
#ma.filled(datag1)

Udatag1=ma.filled(datag1,0)
Udatag5=ma.filled(datag5,0)

#go1Mask = ma.masked_equal(datago1,0)
gio5Mask = ma.masked_equal(datag5,0)

##  This adds the mask back in to show where there is no ice 
icediff = np.subtract(Udatag5,Udatag1)
#icediff[icediff==1e+20]=np.nan
icediff[datag5.mask]=np.nan


#icediff = np.subtract(datag5,datag1)
######### Mesh Data   Mask1 = data1 > 0.0  # This works PL  

# ~ does opposite
Mask41 = datag5.mask & ~datag1.mask
Mask42 = ~datag5.mask & datag1.mask


#######################################
#
#  PLOTS
#
#
#########################################

plt.figure(figsize=(14,10))

nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = nps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
cs =nps.pcolormesh(x,y,Mask42,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))

nps.drawmapboundary(fill_color='dimgrey')
nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

nps.drawcoastlines()
nps.drawmapboundary()
nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(-.9, .9);
plt.colorbar(cs,orientation='vertical', shrink=0.5)

titlenew05 = str("GIOPS New Ice"+ str(GIO_str_timeD5) )  
plt.title(titlenew05, fontsize=ftitle)
plt.savefig('plot5D_Mesh5_GIOPS.png', bbox_inches="tight")

#plt.show(cs)
plt.clf()
plt.cla()
plt.close()


#############
plt.figure(figsize=(14,10))

#  pps = polar_stere(-180, -140, 64, 77, resolution='l')   - old 
pps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = pps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
dog =pps.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu', diffNum))
   
pps.drawmapboundary(fill_color='dimgrey')
pps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
pps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
pps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
     
pps.drawcoastlines()
pps.drawmapboundary()
pps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
pps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(diffMin, diffMax);
plt.colorbar(dog,orientation='vertical', shrink=0.5)
   
titlesub05 = str("GIOPS Ice Thick Diff"+ str(GIO_str_timeD5) + " - " + str(GIO_str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)
         
plt.savefig('plotTH_diff5_GIOPS.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()
    
##########################################################
plt.figure(figsize=(14,10))

nns = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = nns(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])


cmap=plt.cm.get_cmap('PRGn', ThNum)

cat =nns.pcolormesh(x,y,datag5,shading='flat', cmap=cmap)
   
nns.drawmapboundary(fill_color='dimgrey')
nns.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
nns.drawparallels(par, linewidth=0.5, dashes=[1, 5])
nns.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

nns.drawcoastlines()
nns.drawmapboundary()
nns.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
nns.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(0.0, 1.1);
#plt.colorbar(cat,orientation='vertical', shrink=0.5)
plt.colorbar(cat,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)
  
title5 = str("GIOPS Ice Thick"+ str(GIO_str_timeD5 ))  
plt.title(title5, fontsize=ftitle)
      
  
plt.savefig('plotTH_Day_GIOPS5.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()



##########################################################
plt.figure(figsize=(14,10))

nns = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = nns(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])

cmap=plt.cm.get_cmap('PRGn', ThNum)


Roma =nns.pcolormesh(x,y,datag1,shading='flat', cmap=cmap)
   
nns.drawmapboundary(fill_color='dimgrey')
nns.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
nns.drawparallels(par, linewidth=0.5, dashes=[1, 5])
nns.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

nns.drawcoastlines()
nns.drawmapboundary()
nns.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
nns.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(0, 2.0);
plt.colorbar(Roma,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)

title5 = str("GIOPS Ice Thick"+ str(GIO_str_timeD1))  
plt.title(title5, fontsize=ftitle)
          
plt.savefig('plotTH_Day_GIOPS1.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()


##################################################################
# Open  Day 10

ncGIO10 = Dataset("GIO1010th.nc", "r", format="NETCDF4")

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncGIO10.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO10.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_timeD10 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats =ncGIO10.variables['latitude'][:,:]
lons =ncGIO10.variables['longitude'][:,:]

datag10 = ncGIO10.variables['iicevol'][:,:]
datag10 = datag10[0][:][:]





Udatag10=ma.filled(datag10,0)
Udatag1=ma.filled(datag5,0)

#go1Mask = ma.masked_equal(datago1,0)
gio10Mask = ma.masked_equal(datag10,0)

##  This adds the mask back in to show where there is no ice 
icediff = np.subtract(Udatag10,Udatag1)
#icediff[icediff==1e+20]=np.nan
icediff[datag10.mask]=np.nan

icediff = np.subtract(datag10,datag1)
ncGIO10.close()

#########  Mesh
# ~ does opposite
Mask51 = datag10.mask & ~datag1.mask
Mask52 = ~datag10.mask & datag1.mask


#######################################
#
#  PLOTS
#
#
#########################################

plt.figure(figsize=(14,10))

nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = nps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
cs =nps.pcolormesh(x,y,Mask52,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))

    
nps.drawmapboundary(fill_color='dimgrey')
nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

nps.drawcoastlines()
nps.drawmapboundary()
nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(-.9, .9);
plt.colorbar(cs,orientation='vertical', shrink=0.5)
   
titlenew10 = str("GIOPS New Ice"+ str(GIO_str_timeD10) )  
plt.title(titlenew10, fontsize=ftitle)
    
plt.savefig('GIO_plot10D_Mesh1_GIOPS.png', bbox_inches="tight")
#plt.show(cs)
plt.clf()
plt.cla()
plt.close()


#############
plt.figure(figsize=(14,10))

pps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = pps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
dog =pps.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu', diffNum))
   
pps.drawmapboundary(fill_color='dimgrey')
pps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
pps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
pps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
   
      
pps.drawcoastlines()
pps.drawmapboundary()
pps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
pps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(diffMin, diffMax);

##3 Second way to color bar:
plt.colorbar(dog,orientation='vertical', shrink=0.5)
   
   ######## Save first plot  
titlesub05 = str("GIOPS Ice Diff"+ str(GIO_str_timeD10) + " - " + str(GIO_str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)
         
    ##fig, ax = plt.figure()
plt.savefig('plotTH_diff10_GIOPS.png', bbox_inches="tight")
#plt.show()
   # plt.gcf().clear()
plt.clf()
plt.cla()
plt.close()

#####################################################
plt.figure(figsize=(14,10))

nns = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = nns(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])

cmap=plt.cm.get_cmap('PRGn', ThNum)


cat =nns.pcolormesh(x,y,datag10,shading='flat', cmap=cmap)
   
nns.drawmapboundary(fill_color='dimgrey')
nns.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
nns.drawparallels(par, linewidth=0.5, dashes=[1, 5])
nns.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

nns.drawcoastlines()
nns.drawmapboundary()
nns.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
nns.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(0, 2.0);

##3 Second way to color bar:
plt.colorbar(cat,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)

title10 = str("GIOPS Ice Thick"+ str(GIO_str_timeD10))  
plt.title(title10, fontsize=ftitle)
        
plt.savefig('plotTH_Day10_GIOPS.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()


#####################################################
## RIOPS Analysis
#####################################################

##################################################################
# RIOPS INIT

ncRIO_IT = Dataset("RIO_INITth.nc", "r", format="NETCDF4")
print(ncRIO_IT.variables.keys())

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncRIO_IT.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRIO_IT.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
RIO_str_timeIT = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncRIO_IT.variables['latitude'][:,:]
lons =ncRIO_IT.variables['longitude'][:,:]

dataRIT = ncRIO_IT.variables['iicevol'][:,:]
dataRIT = dataRIT[0][:][:]

#icediff = np.subtract(data1,data2)
ncRIO_IT.close()


########### RIO########################################
plt.figure(figsize=(14,10))

rnps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = rnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csRI =rnps.pcolormesh(x,y,dataRIT,shading='flat', cmap=cmap)

    
rnps.drawmapboundary(fill_color='dimgrey')
rnps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
rnps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
rnps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

rnps.drawcoastlines()
rnps.drawmapboundary()
rnps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
rnps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

#ticks=bounds,

plt.clim(0.1, 2.0);
plt.colorbar(csRI,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
   
titleRIOIT = str("RIOPS Model: Ice Thick"+ str(RIO_str_timeIT) )  
plt.title(titleRIOIT, fontsize=ftitle)
    
plt.savefig('PlotTH_RIO0_IT.png', bbox_inches="tight")
#plt.show(csRI)
plt.clf()
plt.cla()
plt.close()





##################################################################
# RIO 12 Hour Forecast 

ncRIO_12 = Dataset("RIO12th.nc", "r", format="NETCDF4")
print(ncRIO_12.variables.keys())

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncRIO_12.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRIO_12.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
RIO_str_time12 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncRIO_12.variables['latitude'][:,:]
lons =ncRIO_12.variables['longitude'][:,:]

dataRIT = ncRIO_12.variables['iicevol'][:,:]
dataRIT = dataRIT[0][:][:]

#icediff = np.subtract(data1,data2)
ncRIO_12.close()


########### RIO########################################
plt.figure(figsize=(14,10))

r12nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = rnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csRI12 =r12nps.pcolormesh(x,y,dataRIT,shading='flat', cmap=cmap)

    
r12nps.drawmapboundary(fill_color='dimgrey')
r12nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
r12nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
r12nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

r12nps.drawcoastlines()
r12nps.drawmapboundary()
r12nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
r12nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

#  ticks=bounds,

plt.clim(0.1, 2.0);
plt.colorbar(csRI12,orientation='vertical', shrink=0.5, spacing='proportional',  cmap=cmap)
   
titleRIOIT = str("RIOPS 12hr"+ str(RIO_str_time12) )  
plt.title(titleRIOIT, fontsize=ftitle)
    
plt.savefig('plotTH_hour12_RIOPS1.png', bbox_inches="tight")
#plt.show(csRI12)
plt.clf()
plt.cla()
plt.close()



##################################################################
# RIO 12 Hour Forecast 

ncRIO_24 = Dataset("RIO24th.nc", "r", format="NETCDF4")
print(ncRIO_24.variables.keys())

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncRIO_24.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRIO_24.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
RIO_str_time24 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncRIO_24.variables['latitude'][:,:]
lons =ncRIO_24.variables['longitude'][:,:]

dataRIT24 = ncRIO_24.variables['iicevol'][:,:]
dataRIT24 = dataRIT24[0][:][:]

ncRIO_24.close()


########### RIO########################################
plt.figure(figsize=(14,10))
r24nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = rnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csRI24 =r24nps.pcolormesh(x,y,dataRIT24,shading='flat', cmap=cmap)

r24nps.drawmapboundary(fill_color='dimgrey')
r24nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
r24nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
r24nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

r24nps.drawcoastlines()
r24nps.drawmapboundary()
r24nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
r24nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

#ticks=bounds,

plt.clim(0.1, 2.0);
plt.colorbar(csRI24,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
   
titleRIOIT = str("RIOPS 24 hr"+ str(RIO_str_time24) )  
plt.title(titleRIOIT, fontsize=ftitle)
    
plt.savefig('plotTH_hour24_RIOPS2.png', bbox_inches="tight")
#plt.show(csRI24)
plt.clf()
plt.cla()
plt.close()





##################################################################
# RIO 12 Hour Forecast 

ncRIO_36 = Dataset("RIO36th.nc", "r", format="NETCDF4")
print(ncRIO_36.variables.keys())

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncRIO_36.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRIO_36.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
RIO_str_time36 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncRIO_36.variables['latitude'][:,:]
lons =ncRIO_36.variables['longitude'][:,:]

dataRIT36 = ncRIO_36.variables['iicevol'][:,:]
dataRIT36 = dataRIT36[0][:][:]

#icediff = np.subtract(data1,data2)
ncRIO_36.close()


########### RIO########################################
plt.figure(figsize=(14,10))

r36nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = rnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csRI36 =r36nps.pcolormesh(x,y,dataRIT36,shading='flat', cmap=cmap)

    
r36nps.drawmapboundary(fill_color='dimgrey')
r36nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
r36nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
r36nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

r36nps.drawcoastlines()
r36nps.drawmapboundary()
r36nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
r36nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
# ticks=bounds,
plt.clim(0.0, 2.0);
plt.colorbar(csRI36,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
   
titleRIOIT = str("RIOPS 36 hr"+ str(RIO_str_time36) )  
plt.title(titleRIOIT, fontsize=ftitle)
    
plt.savefig('plotTH_hour36_RIOPS3.png', bbox_inches="tight")
#plt.show(csRI36)
plt.clf()
plt.cla()
plt.close()









##################################################################
# RIO 48 Hour Forecast 

ncRIO_48 = Dataset("RIO48th.nc", "r", format="NETCDF4")
print(ncRIO_48.variables.keys())

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncRIO_48.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncRIO_48.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
RIO_str_time48 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncRIO_48.variables['latitude'][:,:]
lons =ncRIO_48.variables['longitude'][:,:]

dataRIT48 = ncRIO_48.variables['iicevol'][:,:]
dataRIT48 = dataRIT48[0][:][:]

#icediff = np.subtract(data1,data2)
ncRIO_48.close()


########### RIO########################################
plt.figure(figsize=(14,10))

r4nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat,resolution='l')
x , y = rnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csRI4 =r4nps.pcolormesh(x,y,dataRIT48,shading='flat', cmap=cmap)

    
r4nps.drawmapboundary(fill_color='dimgrey')
r4nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
r4nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
r4nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

r4nps.drawcoastlines()
r4nps.drawmapboundary()
r4nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
r4nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

#ticks=bounds,

plt.clim(0.0, 2.0);
plt.colorbar(csRI4,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
   
titleRIOIT = str("RIOPS 48 hr"+ str(RIO_str_time48) )  
plt.title(titleRIOIT, fontsize=ftitle)
    
plt.savefig('plotTH_hour48_RIOPS4.png', bbox_inches="tight")
#plt.show(csRI4)
plt.clf()
plt.cla()
plt.close()




#######################################
ncGIO_IN = Dataset("GIO_INth.nc", "r", format="NETCDF4")

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncGIO_IN.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO_IN.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_timeIT = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncGIO_IN.variables['latitude'][:,:]
lons =ncGIO_IN.variables['longitude'][:,:]

dataGIT = ncGIO_IN.variables['iicevol'][:,:]
dataGIT = dataGIT[0][:][:]

ncGIO_IN.close()

#######################################
##  PLOTS
###########################################
########################################

plt.figure(figsize=(14,10))

gnps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = gnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csGI =gnps.pcolormesh(x,y,dataGIT,shading='flat', cmap=cmap)

    
gnps.drawmapboundary(fill_color='dimgrey')
gnps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
gnps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
gnps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

gnps.drawcoastlines()
gnps.drawmapboundary()
gnps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
gnps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0.0, 2.0);
#plt.colorbar(csGI ,orientation='vertical', shrink=0.5)ticks=bounds, 
plt.colorbar(csGI,orientation='vertical', shrink=0.5, spacing='proportional',  cmap=cmap)



titlenew10 = str("GIOPS- Ice Thick"+ str(GIO_str_timeIT) )  
plt.title(titlenew10, fontsize=ftitle)
    
plt.savefig('PlotTH_GIO_IT.png', bbox_inches="tight")
#plt.show(csGI)
plt.clf()
plt.cla()
plt.close()



#####################################
#######GIOPS Day 2  duplicate in datag1

#ncGIO_1 = Dataset("GIO001.nc", "r", format="NETCDF4")

#tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
#nctime = ncGIO_1.variables[tname][:] # get values# open and read in data from first nc file
#t_unit = ncGIO_1.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
#tvalue = num2date(nctime,units=t_unit)
#GIO_str_time1 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

#lats = ncGIO_1.variables['latitude'][:,:]
#lons =ncGIO_1.variables['longitude'][:,:]

#dataGIT = ncGIO_1.variables['iiceconc'][:,:]
#dataGIT = dataGIT[0][:][:]

#ncGIO_1.close()



########## PLOT
#plt.figure(figsize=(14,10))

#g1nps = polar_stere(-180, -140, 64, 77, resolution='l')
#x , y = gnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#csG1 =g1nps.pcolormesh(x,y,dataGIT,shading='flat', cmap=cmap)
    
#g1nps.drawmapboundary(fill_color='dimgrey')
#g1nps.fillcontinents(color='lightgray', lake_color='darkgrey')
#mer = np.arange(-60, 120, 10.)
#par = np.arange(0, 90, 5.)
#g1nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
#g1nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

#g1nps.drawcoastlines()
#g1nps.drawmapboundary()
#g1nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
#g1nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

#plt.clim(0.0, 1.1);
#plt.colorbar(csG1 ,orientation='vertical', shrink=0.5)
#plt.colorbar(csG1,orientation='vertical', shrink=0.5, ticks=bounds, spacing='proportional',  cmap=cmap)
 
  
#titlenew10 = str("GIOPS New Ice"+ str(GIO_str_time1) )  
#plt.title(titlenew10, fontsize=ftitle)
    
#plt.savefig('plot_GIO_Day1.png', bbox_inches="tight")
#plt.show(csG1)
#plt.clf()
#plt.cla()
#plt.close()


#####################################
#######GIOPS Day 3

ncGIO_2 = Dataset("GIO002th.nc", "r", format="NETCDF4")

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncGIO_2.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO_2.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_time2 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncGIO_2.variables['latitude'][:,:]
lons =ncGIO_2.variables['longitude'][:,:]

datag2 = ncGIO_2.variables['iicevol'][:,:]
datag2 = datag2[0][:][:]

ncGIO_2.close()



########## PLOT
plt.figure(figsize=(14,10))

g2nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = gnps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
#cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csG2 =g2nps.pcolormesh(x,y,datag2,shading='flat', cmap=cmap)

    
g2nps.drawmapboundary(fill_color='dimgrey')
g2nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
g2nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
g2nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

g2nps.drawcoastlines()
g2nps.drawmapboundary()
g2nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
g2nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0.0, 2.0);
#plt.colorbar(csG2 ,orientation='vertical', shrink=0.5)ticks=bounds,
plt.colorbar(csG2,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
 
  
titlenew10 = str("GIOPS Ice Thick"+ str(GIO_str_time2) )  
plt.title(titlenew10, fontsize=ftitle)
    
plt.savefig('plotTH_Day_GIOPS2.png', bbox_inches="tight")
#plt.show(csG2)
plt.clf()
plt.cla()
plt.close()

##############################################################################  Difference Plots ###########################


Udatag1=ma.filled(datag1,0)
Udatag2=ma.filled(datag2,0)

#go1Mask = ma.masked_equal(datago1,0)
gio2Mask = ma.masked_equal(datag2,0)

##  This adds the mask back in to show where there is no ice 
icediff = np.subtract(Udatag2,Udatag1)
#icediff[icediff==1e+20]=np.nan
icediff[datag2.mask]=np.nan



icediff = np.subtract(datag2,datag1)

######### Mesh Data   Mask1 = data1 > 0.0  # This works PL  

# ~ does opposite
Mask41 = datag2.mask & ~datag1.mask
Mask42 = ~datag2.mask & datag1.mask


#######################################
#
#  PLOTS
#
#
#########################################

plt.figure(figsize=(14,10))
nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = nps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
cs =nps.pcolormesh(x,y,Mask42,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))

nps.drawmapboundary(fill_color='dimgrey')
nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

nps.drawcoastlines()
nps.drawmapboundary()
nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(-.9, .9);
plt.colorbar(cs,orientation='vertical', shrink=0.5)

titlenew05 = str("GIOPS New Ice"+ str(GIO_str_time2) )  
plt.title(titlenew05, fontsize=ftitle)
plt.savefig('plot5D_Mesh2_GIOPS.png', bbox_inches="tight")

#plt.show(cs)
plt.clf()
plt.cla()
plt.close()


#############
plt.figure(figsize=(14,10))

pps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = pps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
dog =pps.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu',diffNum))
   
pps.drawmapboundary(fill_color='dimgrey')
pps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
pps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
pps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
     
pps.drawcoastlines()
pps.drawmapboundary()
pps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
pps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(diffMin,diffMax);
plt.colorbar(dog,orientation='vertical', shrink=0.5)
   
titlesub05 = str("GIOPS Ice Thick Diff"+ str(GIO_str_time2) + " - " + str(GIO_str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)
         
plt.savefig('plotTH_diff2_GIOPS.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()



#####################################
#######GIOPS Day 3

ncGIO_3 = Dataset("GIO003th.nc", "r", format="NETCDF4")

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncGIO_3.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO_3.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_time3 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncGIO_3.variables['latitude'][:,:]
lons =ncGIO_3.variables['longitude'][:,:]
datag3 = ncGIO_3.variables['iicevol'][:,:]
datag3 = datag3[0][:][:]

ncGIO_3.close()


########## PLOT
plt.figure(figsize=(14,10))

g3nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = g3nps(lons, lats)


#bounds = [  0.1, 0.3 , 0.4, 0.6, 0.7, 0.8, 0.9, 1.0]
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
#cmap= mpl.colors.ListedColormap(['green', 'blue', 'orange', 'purple', 'yellow'])

   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite' plt.cm.get_cmap('Blues', 9)
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csG3 =g3nps.pcolormesh(x,y,datag3,shading='flat', cmap=cmap)
    
g3nps.drawmapboundary(fill_color='dimgrey')
g3nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
g3nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
g3nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

g3nps.drawcoastlines()
g3nps.drawmapboundary()
g3nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
g3nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0.0, 2.0);
#plt.colorbar(csG3 ,orientation='vertical', shrink=0.5)  ticks=bounds,
cmap=plt.cm.get_cmap('PRGn', ThNum)

plt.colorbar(csG3,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
   

titlenew10 = str("GIOPS Ice Thick"+ str(GIO_str_time3) )  
plt.title(titlenew10, fontsize=ftitle)
    
plt.savefig('plotTH_Day_GIOPS3.png', bbox_inches="tight")
#plt.show(csG3)
plt.clf()
plt.cla()
plt.close()





##############################################################################  Difference Plots ###########################


Udatag1=ma.filled(datag1,0)
Udatag3=ma.filled(datag3,0)

#go1Mask = ma.masked_equal(datago1,0)
gio3Mask = ma.masked_equal(datag3,0)

##  This adds the mask back in to show where there is no ice 
icediff = np.subtract(Udatag3,Udatag1)
#icediff[icediff==1e+20]=np.nan




icediff = np.subtract(datag3,datag1)
icediff[datag3.mask]=np.nan

######### Mesh Data   Mask1 = data1 > 0.0  # This works PL  

# ~ does opposite
Mask41 = datag3.mask & ~datag1.mask
Mask42 = ~datag3.mask & datag1.mask


#######################################
#
#  PLOTS
#
#
#########################################

plt.figure(figsize=(14,10))
nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = nps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'
cmap=plt.cm.get_cmap('PRGn', ThNum)

cs =nps.pcolormesh(x,y,Mask42,shading='flat', cmap=plt.cm.get_cmap('RdBu', 3))

nps.drawmapboundary(fill_color='dimgrey')
nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

nps.drawcoastlines()
nps.drawmapboundary()
nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(-.9, .9);
plt.colorbar(cs,orientation='vertical', shrink=0.5)

titlenew05 = str("GIOPS New Ice"+ str(GIO_str_time3) )  
plt.title(titlenew05, fontsize=ftitle)
plt.savefig('plot5D_Mesh3_GIOPS.png', bbox_inches="tight")

#plt.show(cs)
plt.clf()
plt.cla()
plt.close()


#############
plt.figure(figsize=(14,10))

pps = polar_stere(minGLon, maxGLon, minGLat,maxGLat, resolution='l')
x , y = pps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite'

dog =pps.pcolormesh(x,y,icediff,shading='flat', cmap=plt.cm.get_cmap('RdBu', diffNum))
   
pps.drawmapboundary(fill_color='dimgrey')
pps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
pps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
pps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
     
pps.drawcoastlines()
pps.drawmapboundary()
pps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
pps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

 # plt.colorbar(cs,orientation='vertical', shrink=0.5, cmap=plt.cm.get_cmap('Blues', 5))
plt.clim(diffMin, diffMax);
plt.colorbar(dog,orientation='vertical', shrink=0.5)
   
titlesub05 = str("GIOPS Ice Thick Diff"+ str(GIO_str_time3) + " - " + str(GIO_str_timeD1))  
plt.title(titlesub05, fontsize=ftitle)
         
plt.savefig('plotTH_diff3_GIOPS.png', bbox_inches="tight")
#plt.show()
plt.clf()
plt.cla()
plt.close()













#####################################
#######GIOPS Day 3

ncGIO_4 = Dataset("GIO004th.nc", "r", format="NETCDF4")

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncGIO_4.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO_4.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_time4 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncGIO_4.variables['latitude'][:,:]
lons =ncGIO_4.variables['longitude'][:,:]
dataGIT = ncGIO_4.variables['iicevol'][:,:]
dataGIT = dataGIT[0][:][:]

ncGIO_4.close()


########## PLOT
plt.figure(figsize=(14,10))

g4nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat,resolution='l')
x , y = g4nps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite' plt.cm.get_cmap('Blues', 9)
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)


csG4 =g4nps.pcolormesh(x,y,dataGIT,shading='flat', cmap=cmap)
    
g4nps.drawmapboundary(fill_color='dimgrey')
g4nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
g4nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
g4nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

g4nps.drawcoastlines()
g4nps.drawmapboundary()
g4nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
g4nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])

plt.clim(0.0, 2.0);
#plt.colorbar(csG3 ,orientation='vertical', shrink=0.5) ticks=bounds,
plt.colorbar(csG4,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
   

titlenew10 = str("GIOPS Ice Thick"+ str(GIO_str_time4) )  
plt.title(titlenew10, fontsize=ftitle)
    
plt.savefig('plotTH_Day_GIOPS4.png', bbox_inches="tight")
#plt.show(csG4)
plt.clf()
plt.cla()
plt.close()



#####################################
#######GIOPS Day 7

ncGIO_7 = Dataset("GIO7th.nc", "r", format="NETCDF4")

tname = "time"   # sometimes doesnt work with substituding  tname with "time"  need quotes
nctime = ncGIO_7.variables[tname][:] # get values# open and read in data from first nc file
t_unit = ncGIO_7.variables[tname].units # get unit  "days since 1950-01-01T00:00:00Z"
tvalue = num2date(nctime,units=t_unit)
GIO_str_time7 = [i.strftime("%Y-%m-%d %H:%M") for i in tvalue]

lats = ncGIO_7.variables['latitude'][:,:]
lons =ncGIO_7.variables['longitude'][:,:]
dataGIT = ncGIO_7.variables['iicevol'][:,:]
dataGIT = dataGIT[0][:][:]

ncGIO_7.close()


########## PLOT
plt.figure(figsize=(14,10))

g7nps = polar_stere(minGLon, maxGLon, minGLat,maxGLat,resolution='l')
x , y = g7nps(lons, lats)
   # cs =nps.pcolormesh(x,y,icediff,shading='flat',cmap=plt.cm.seismic) PiYG RdBu  spectral' 'AntiqueWhite' plt.cm.get_cmap('Blues', 9)
cmap= mpl.colors.ListedColormap(['cornflowerblue', 'aquamarine', 'yellow', 'orange', 'red'])
cmap=plt.cm.get_cmap('PRGn', ThNum)

csG7 =g7nps.pcolormesh(x,y,dataGIT,shading='flat', cmap=cmap)
    
g7nps.drawmapboundary(fill_color='dimgrey')
g7nps.fillcontinents(color='lightgray', lake_color='darkgrey')
mer = np.arange(-60, 120, 10.)
par = np.arange(0, 90, 5.)
g7nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
g7nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])

g7nps.drawcoastlines()
g7nps.drawmapboundary()
g7nps.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
g7nps.drawmeridians(np.arange(-180.,180.,5.),labels=[1,0,0,0])
#1.1
plt.clim(0.0, 2.0);
#plt.colorbar(csG3 ,orientation='vertical', shrink=0.5)  ticks=bounds,
plt.colorbar(csG7,orientation='vertical', shrink=0.5,  spacing='proportional',  cmap=cmap)
   

titlenew10 = str("GIOPS Ice Thick"+ str(GIO_str_time7) )  
plt.title(titlenew10, fontsize=ftitle)
    
plt.savefig('plotTH_Day_GIOPS7.png', bbox_inches="tight")
#plt.show(csG7)
plt.clf()
plt.cla()
plt.close()
