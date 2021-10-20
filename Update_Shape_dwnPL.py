#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:40:54 2019

@author: emily.niebuhr
"""
###########################
# This downloads the shapefile everytime this is run - to help with verification


import urllib.request
import tarfile
from datetime import datetime, timedelta
from shutil import copy2
import os
import matplotlib as mpl
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




####  DATES
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

yester22=mx2.day
ymos22=mx2.month
yyear22=mx2.year

yester5=mx5.day
y5mos=mx5.month
y5yr=mx5.year


tg=str("-")
dg=str("-")
nc = str(".nc")
gzz = str(".tar.gz")

gis_NAME = "ShpFile_"+ str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) +".zip"


RASM= str("RASM-ESRL_")
RASM_N= str("RASM-ESRL_4NIC_")

name_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester))+gzz 
dir_EL = RASM_N + str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
dir2_EL = RASM+str(yyear)+tg+str("{:02d}".format(ymos))+tg+str("{:02d}".format(yester)) 
#
#
os.path.dirname('/home/emily.niebuhr/Downloads')
dir1 = os.path.abspath('/home/emily.niebuhr/Downloads')
dir1 = os.path.abspath('/home/amos/IceOperatePL')

os.chdir(dir1)

os.chdir(dir1+"/"+dir_EL+"/"+dir2_EL)
print (os.getcwd())

synop= "https://ocean.weather.gov/shtml/arctic/UA_LATEST.gif"
names =  urllib.request.urlretrieve(synop,"Syn_today.gif")

synop= "https://ocean.weather.gov/shtml/arctic/24SFC_LATEST.gif"
names =  urllib.request.urlretrieve(synop,"Syn_24.gif")

synop= "https://ocean.weather.gov/shtml/arctic/48SFC_LATEST.gif"
names =  urllib.request.urlretrieve(synop,"Syn_48.gif")

synop= "https://ocean.weather.gov/shtml/arctic/72SFC_LATEST.gif"
names =  urllib.request.urlretrieve(synop,"Syn_72.gif")


synop5 = "https://ocean.weather.gov/shtml/arctic/96SFC_LATEST.gif"
names2 =  urllib.request.urlretrieve(synop5,"Syn_96.gif")

### Retrieve shapefile 
 
shp_Ice = "https://www.weather.gov/source/afc/icedata/full_latest.zip"
shp2=urllib.request.urlretrieve(shp_Ice,gis_NAME)


###############  ASIP Ice Data ##########
dirNow = os.getcwd()
IceName = str("IceConc") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(daye))+str(".jpg")

ASIP_Conc = "https://www.weather.gov/images/afc/ice/CT.jpg"
AS11fP =  urllib.request.urlretrieve(ASIP_Conc,"full_conc.jpg")
AS11P =  urllib.request.urlretrieve(ASIP_Conc,IceName)
#copy2((dirNow+"/"+IceName), (dirNow+"/old"+IceName))

#RHup = int(sys.argv[1])
#RHdown = int(sys.argv[2])
#LHup = int(sys.argv[3])
#LHdown = int(sys.argv[4])

RHup = 175
RHdown = 350
LHup = 875
LHdown = 940

catDog = Image.open(IceName)
width, heigh = catDog.size
catDog.size
#croppedIm = catDog.crop((175,380,875,940))
#croppedIm = catDog.crop((175,350,985,1040))
#croppedIm = catDog.crop((175,350,1050,1040))
croppedIm = catDog.crop((RHup,RHdown,LHup,LHdown))
croppedIm.save(IceName)
croppedIm.save("ASIP_currConc.jpg")


Forecst5D = str("IceForecast") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(daye))+str(".jpg")
OldForecst5D = str("IceConc") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(yester5))+str(".jpg")
ASIP_5Day = "https://www.weather.gov/images/afc/ice/Forecast.jpg"
ASIP_5DY =  urllib.request.urlretrieve(ASIP_5Day,Forecst5D)
ASIP_f5DY =  urllib.request.urlretrieve(ASIP_5Day,"full5day.jpg")
catPuppy = Image.open(Forecst5D)
width, heigh = catPuppy.size
catPuppy.size
# November croppedIm = catPuppy.crop((175,180,875,620))
#croppedIm = catPuppy.crop((175,380,875,940))

croppedIm = catPuppy.crop((175,350,1150,1040))
croppedIm.save(Forecst5D)
croppedIm.save("ASIP_Day5.jpg")

# https://www.weather.gov/images/afc/ice/SA.jpg
stagename = str("IceStg") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(daye))+str(".jpg")

ASIP_stage = "https://www.weather.gov/images/afc/ice/SA.jpg"
ASIP_st =  urllib.request.urlretrieve(ASIP_stage,stagename)
ASIP_fst =  urllib.request.urlretrieve(ASIP_stage,"curr_full_stage.jpg")
catPuppy = Image.open(stagename)
width, heigh = catPuppy.size
catPuppy.size
# November croppedIm = catPuppy.crop((175,180,875,620))
# January 
#croppedIm = catPuppy.crop((175,380,875,940))
croppedIm = catPuppy.crop((175,350,1150,1050))

croppedIm.save(stagename)
croppedIm.save("ASIP_currStage.jpg")

############# Probably not needed PL
#copy2(oldDir+"ASIP_currStage.jpg", Curr_Dirr+"old_ASIP_currStage.jpg")
#copy2(oldDir+"ASIP_Day5.jpg", Curr_Dirr+"old_ASIP_Day5.jpg")
#copy2(oldDir+"ASIP_currConc.jpg", Curr_Dirr+"old_ASIP_currConc.jpg")


Curr_Dirr = (dir1+"/"+dir_EL+"/"+dir2_EL+"/")
os.chdir(Curr_Dirr)
print (os.getcwd())



######## DOWNLOAD ICE PLOTS ANCHORAGE
# GOFS images
# https://www7320.nrlssc.navy.mil/GLBhycomcice1-12/navo/beauforticen/nowcast/icen2018082812_2018083000_930_beauforticen.001.gif



##?
#GOF_D5 = str("https://www7320.nrlssc.navy.mil/GLBhycomcice1-12/navo/beauforticen/nowcast/icen")+str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(yester))+str("12_")+str(yr)+str("0903")+str("00_930_beauforticen.001.gif")
#GOF_D7 = str("https://www7320.nrlssc.navy.mil/GLBhycomcice1-12/navo/beauforticen/nowcast/icen")+str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(yester))+str("12_")+str(yr)+str("0905")+str("00_930_beauforticen.001.gif")

##############
# To add drift images
################## US
#USDR24 = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_024_ice_drift.gif"
#USDR2D = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_048_ice_drift.gif"
#USDR3D = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_072_ice_drift.gif"
#USDR4D = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_096_ice_drift.gif"
#USDR5D = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_120_ice_drift.gif"
#USDR6D = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_144_ice_drift.gif"
#USDR7D = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_168_ice_drift.gif"
#USDR10D = "http://mag.ncep.noaa.gov/data/polar/00/polar_polar_216_ice_drift.gif"
#
#US24 =  urllib.request.urlretrieve(USDR24 ,"US_INIT.png")
#US48 =  urllib.request.urlretrieve(USDR2D ,"US_Day2.png")
#US72 =  urllib.request.urlretrieve(USDR3D ,"US_Day3.png")
#US96 =  urllib.request.urlretrieve(USDR4D ,"US_Day4.png")
#US5 =  urllib.request.urlretrieve(USDR5D ,"US_Day5.png")
#US6 =  urllib.request.urlretrieve(USDR6D ,"US_Day6.png")
#US7 =  urllib.request.urlretrieve(USDR7D ,"US_Day7.png")
#
#US10 =  urllib.request.urlretrieve(USDR10D ,"US_Day10.png")



###############  ASIP Ice Data ##########
dirNow = os.getcwd()
IceName = str("IceConc") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(daye))+str(".jpg")

ASIP_Conc = "https://www.weather.gov/images/afc/ice/CT.jpg"
AS11fP =  urllib.request.urlretrieve(ASIP_Conc,"full_conc.jpg")
AS11P =  urllib.request.urlretrieve(ASIP_Conc,IceName)
#copy2((dirNow+"/"+IceName), (dirNow+"/old"+IceName))

catDog = Image.open(IceName)
width, heigh = catDog.size
catDog.size
#croppedIm = catDog.crop((175,380,875,940))
croppedIm = catDog.crop((175,350,985,1040))
#croppedIm = catDog.crop((175,350,1400,1040))
croppedIm.save(IceName)
croppedIm.save("ASIP_currConc.jpg")


Forecst5D = str("IceForecast") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(daye))+str(".jpg")
OldForecst5D = str("IceConc") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(yester5))+str(".jpg")
ASIP_5Day = "https://www.weather.gov/images/afc/ice/Forecast.jpg"
ASIP_5DY =  urllib.request.urlretrieve(ASIP_5Day,Forecst5D)
ASIP_f5DY =  urllib.request.urlretrieve(ASIP_5Day,"full5day.jpg")
catPuppy = Image.open(Forecst5D)
width, heigh = catPuppy.size
catPuppy.size
# November croppedIm = catPuppy.crop((175,180,875,620))
#croppedIm = catPuppy.crop((175,380,875,940))
## Winter CROP is (175,350,985,1200))
croppedIm = catPuppy.crop((175,350,985,1200))
#croppedIm = catPuppy.crop((175,350,1200,1040))
croppedIm.save(Forecst5D)
croppedIm.save("ASIP_Day5.jpg")

# https://www.weather.gov/images/afc/ice/SA.jpg
stagename = str("IceStg") + str(yr)+str("{:02d}".format(mos))+str("{:02d}".format(daye))+str(".jpg")

ASIP_stage = "https://www.weather.gov/images/afc/ice/SA.jpg"
ASIP_st =  urllib.request.urlretrieve(ASIP_stage,stagename)
ASIP_fst =  urllib.request.urlretrieve(ASIP_stage,"curr_full_stage.jpg")
catPuppy = Image.open(stagename)
width, heigh = catPuppy.size
catPuppy.size
# November croppedIm = catPuppy.crop((175,180,875,620))
# January 
#croppedIm = catPuppy.crop((175,380,875,940))
croppedIm = catPuppy.crop((175,350,985,1040))
croppedIm = catPuppy.crop((175,350,985,1200))
croppedIm.save(stagename)
croppedIm.save("ASIP_currStage.jpg")

