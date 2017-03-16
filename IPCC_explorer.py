import sys
import re
import utm
import os
import csv
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def main():
	print 'hi'
	cwd = os.getcwd()
	filename = r'fig13.20.nc'
	path = os.path.join(cwd,filename)
	#print path
	dataset = Dataset(path)
	print dataset.file_format
	print dataset.dimensions.keys()
	print dataset.variables.keys()
	print dataset.variables['panelA']
	lats = dataset.variables['lat'][:]
	lons = dataset.variables['lon'][:]
	rcp26 = dataset.variables['panelA'][:]


	lon_o = lons.mean()
	print lon_o
	lat_o = lats.mean()
	print lat_o

	m = Basemap(resolution ='l', projection='robin',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=0,urcrnrlon=360,lat_ts=40,lat_0=lat_o,lon_0=lon_o)
	lon,lat = np.meshgrid(lons,lats)
	xi,yi = m(lon,lat)

	 #Plot Data
	cs = m.pcolor(xi,yi,np.squeeze(rcp26))

	# Add Grid Lines
	m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
	m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

	# Add Coastlines, States, and Country Boundaries
	m.drawcoastlines()
	m.drawstates()
	m.drawcountries()

	# Add Colorbar
	cbar = m.colorbar(cs, location='bottom', pad="10%")
	cbar.set_label(rcp26)

	# Add Title
	plt.title('Sea Level Rise')

	plt.show()




if __name__ == '__main__':
	main()