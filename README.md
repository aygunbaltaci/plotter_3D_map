# 3D Maps Plotter

This code plots the input data on a 3D Arcgis map. 

## Prerequisites
**Python 3**
> sudo apt update

> sudo apt install python3.6 (or any other python3 version) 

**Basemap library**

Install the basemap library to your PC from the link below:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap

Then, install it with the command (in the directory where *.whl* file is located): 
> pip3 install basemap-1.0.8-cp38-none-win_amd64.whl (modify the name according your file name)

**Csv, Matplotlib and Numpy libraries**
> pip3 install csv matplotlib numpy

## Input File
The program takes input file: 
*inputfiles/input_plot_maps.csv*

1st column: Latitude
2nd column: Longitude
3rd column: Height
4rd column: Your input data

## Usage
> python3 plot_maps.py

Note: you need to have an internet connection to fetch map image from arcgic server for the first time. Then, the image is saved at the directory: 
*baseimages/*

As long as the latitude and longitude information does not change, the program will use the saved map image in this directory so the internet connection won't be required. 

If the program takes long time to produce the graph, you can play with the value of the variable *baseImgRes* to reduce the resolution of the base image.

## Result
The result is saved in the directory below with the corresponding date (YYYYMMDD_HHMMSS):
*outputfiles/*

Perform *Text to Columns* conversion with *space* character as delimeter on the output csv file. 

## Copyright
This code is licensed under GNU General Public License v3.0. For further information, please refer to [LICENSE](LICENSE)
