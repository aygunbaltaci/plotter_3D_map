#!/usr/bin/env python3

#####################################################
# 04.06.2020
#
# This code plots the input data on a 3D arcgis map. 
# input data is provided at:  
# inputfiles/plot_maps_input.csv
# 
# Note: you need to have an internet connection to 
# fetch map image from arcgic server for the first
# time. Then, the image is saved at the directory: 
# baseimages/
#  
# Prerequisites: pip3 basemap matplotlib numpy 
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

import os
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data
from datetime import datetime
import math 
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable
import mpl_toolkits.mplot3d.art3d as art3d

# ============= Variables
azimAng = 330 # azimuth angle of image
elev = 40 # elevation angle of image
minAltitude = 0 
maxAltitude = 50
extraSpaceBaseImg = 0.00001 # This number determines how much extra space (coord) to plot beyond min/max coord values from input data
baseImgRes = 10 # base image resolution, 1 = best, 10 = worst (?)
xLimMult = 0.03 # required for setting x-limit correctly on the plot, don't change
yLimMult = 0.04 # required for setting y-limit correctly on the plot, don't change
baseDir = 'baseimages'
inputFile = 'input_plot_maps.csv'
inputDir = 'inputfiles'
defaultDelimeter = ','
defaultEncoding = 'utf-8-sig'
figDate = datetime.now().strftime('%Y%m%d_%H%M%S')
figDimX = 19.2 # save the figure in 1920x1080 format
figDimY = 10.8
figDpi = 1000 # image resolution
axisLabelSize = 15 
titleLabelSize = 25
labelDist = 15 # increase distance between label name and axis, found from https://kaleidoscopicdiaries.wordpress.com/2015/05/30/distance-between-axes-label-and-axes-in-matplotlib/
figFormat = 'pdf'
figSaveDir = 'outputfiles'
figSaveName = 'plot_maps_output'
figTitle = 'test'
saveFig = figSaveDir + os.sep + figDate + '_' + figSaveName + '.' + figFormat
inputData = []
defaultLegendName = []

# ============= Fetch Input Data
with open(inputDir + os.sep + inputFile,'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = defaultDelimeter)
    
    # Fetch the inputData from each row
    for row in plots:
        inputData.append(row)
    
    inputData = list(map(list, zip(*inputData))) # transpose the inputData: rows -> columns
    numData = len(inputData)
    
    # Update default label names if labels are given in the input file
    if not (inputData[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
        defaultXLabel = inputData[0][0]
        defaultYLabel = inputData[1][0]
        defaultZLabel = inputData[2][0]
        for i in range(3, numData):
            defaultLegendName.append(inputData[i][0])
        # Delete labels
        for i in range(numData):
            del inputData[i][0]
    
    # convert input inputData to float  
    for i in range(numData): # iterate over each column    
        inputData[i] = list(map(float, inputData[i]))  # convert inputData to float

# ============= Set Borders of Base Image, Setup File Name and Directory Path 
llcrnrlat = min(inputData[0]) - extraSpaceBaseImg
urcrnrlat = max(inputData[0]) + extraSpaceBaseImg
llcrnrlon = min(inputData[1]) - extraSpaceBaseImg
urcrnrlon = max(inputData[1]) + extraSpaceBaseImg
basePicFileName = str(llcrnrlat) + '_' + str(urcrnrlat) + '_' + str(llcrnrlon) + '_' + str(urcrnrlon)
basePicFileName = basePicFileName.replace('.', '') 
baseFileLoc = os.getcwd() + os.sep + baseDir + os.sep + basePicFileName + '.png'

# ============= Initialize Figure
fig = plt.figure(figsize = (figDimX, figDimY))

# ============= Fetch the Base Image
if not os.path.exists(baseFileLoc): # fetch the maps image if it is not already fetched before
    m = Basemap(llcrnrlat = llcrnrlat, llcrnrlon = llcrnrlon, urcrnrlat = urcrnrlat, urcrnrlon = urcrnrlon, resolution = 'f', epsg = 3857) # 3857 is the projection that Google Maps uses. Check out https://gis.stackexchange.com/questions/48949/epsg-3857-or-4326-for-googlemaps-openstreetmap-and-leaflet
    m.arcgisimage(service = 'ESRI_Imagery_World_2D', xpixels = 2000, verbose= True)
    fig.savefig(baseDir + os.sep + basePicFileName, bbox_inches = 'tight', pad_inches = 0)

ax = fig.add_subplot(projection = '3d')
ax.view_init(azim = azimAng, elev = elev)
ax.set_zlim(minAltitude, maxAltitude)

fn = get_sample_data(baseFileLoc) 
arr = read_png(fn)
height, width = arr.shape[:2]
stepX, stepY = (urcrnrlat - llcrnrlat) / width, (urcrnrlon - llcrnrlon) / height

X1 = np.arange(llcrnrlat, urcrnrlat, stepX)
Y1 = np.arange(llcrnrlon, urcrnrlon, stepY)
X1, Y1 = np.meshgrid(X1, Y1)
ax.plot_surface(X1, Y1, np.atleast_2d(0), rstride = baseImgRes, cstride = baseImgRes, facecolors = arr)

ax.set_xlim(llcrnrlat - ((llcrnrlat - urcrnrlat) * xLimMult),urcrnrlat - ((urcrnrlat - llcrnrlat) * xLimMult))
ax.set_ylim(llcrnrlon - ((llcrnrlon - urcrnrlon) * yLimMult),urcrnrlon - ((urcrnrlon - llcrnrlon) * yLimMult))

inputData[0] = [e-0.00002 for e in inputData[0]]
inputData[1] = [e for e in inputData[1]]
inputData[2] = [e for e in inputData[2]]
plotResult = ax.scatter(inputData[0], inputData[1], inputData[2], c = inputData[3], cmap='autumn')
	
ax.xaxis._axinfo["grid"]['linewidth'] = 0 # taken from https://stackoverflow.com/questions/41923161/changing-grid-line-thickness-in-3d-surface-plot-in-python-matplotlib
ax.yaxis._axinfo["grid"]['linewidth'] = 0
ax.zaxis._axinfo["grid"].update({"linewidth":0.5, "color" : "gray"})

cbar = fig.colorbar(plotResult, ax = ax, fraction=0.046, pad=0.04)
cbar.set_label("Data Rate (kbpms)")

# Draw a circle on the x=0 'wall'
'''
p = Circle((48.181975, 11.614124), 30)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0, zdir="x")
'''

ax.set_xlabel(defaultXLabel, size = axisLabelSize, labelpad = labelDist)
ax.set_ylabel(defaultYLabel, size = axisLabelSize, labelpad = labelDist)
ax.set_zlabel(defaultZLabel, size = axisLabelSize, labelpad = labelDist)

print("Please enter the title name. \nDefault is: \'%s\'" %figTitle)
userInput = input()
if userInput == '':
    figTitle = figTitle
else: 
    figTitle = userInput
plt.title(figTitle, size = titleLabelSize)
plt.savefig(saveFig, format = figFormat, dpi = figDpi)
plt.tight_layout() # to adjust spacing between graphs and labels
plt.show()