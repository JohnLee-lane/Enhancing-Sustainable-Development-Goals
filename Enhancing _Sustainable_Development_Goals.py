# Import libraries
import os
from netCDF4 import Dataset
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define the file path to the netCDF data
file = os.path.join('C:/Users/jons',
                    'Desktop',
                    "land_cover_type_from_2001_2019",
                    "LULC",
                    'g4.timeAvgMap.OCO2_GEOS_L3CO2_MONTH_10r_XCO2.20180101-20180531.180W_90S_180E_90N.nc')

# Read the netCDF data
data_landcover = Dataset(file, mode='r')  # read the data
print(type(data_landcover))  # print the type of the data
print(data_landcover.variables.keys())  # print the variables in the data

# Extract latitude, longitude, time, and land cover data from the netCDF file
lats = data_landcover.variables['lat'][:]
longs = data_landcover.variables['lon'][:]
time = data_landcover.variables['lcovtime'][:]
land_cover = data_landcover.variables['LC'][:]

# Create Basemap instance for the region
mp = Basemap(projection='merc',
             llcrnrlon=28.75,  # lower longitude
             llcrnrlat=-3,  # lower latitude
             urcrnrlon=31,  # upper longitude
             urcrnrlat=-1,  # upper latitude
             resolution='i')

# Convert coordinates into 2D arrays for plotting
lon, lat = np.meshgrid(longs, lats)
x, y = mp(lon, lat)

# Plot and save land cover images for each year in a single figure
plt.figure(figsize=(15, 13))

# Loop for all the years
years = np.arange(0, 19)  # for considering all years from 2021-2019

# Define a colormap with specific colors for each land cover type
landcover_cmap = ListedColormap(['blue', 'green', 'darkgreen', 'yellow', 'forestgreen',
                                 'olive', 'saddlebrown', 'tan', 'peru', 'orange', 
                                 'lime', 'blue', 'gray', 'red', 'yellowgreen', 'white', 'lightgray'])

# Get unique values in the land cover array
unique_values = np.unique(land_cover)

for i in years:
    # Plot land cover using pcolor
    plt.subplot(4, 5, i + 1)  # 4 rows, 5 columns, i+1 is the current subplot index
    c_scheme = mp.pcolor(x, y, np.squeeze(land_cover[i, :, :]), cmap=landcover_cmap)
    mp.readshapefile('C:/Users\jons\Desktop\MIS_Pratical\Individual_Assignment_2023_October\Co2_data_2002_2017_AIRS\Kigali_district/Rwanda_district',
                     'Kigali_district2')
    mp.drawcoastlines()
    if i + 1 < 10:
        plt.title('Year ' + str(200) + str(i + 1), size=10)
    else:
        plt.title('Year ' + str(20) + str(i + 1), size=10)

# Add a colorbar
cbar_ax = plt.axes([0.92, 0.15, 0.02, 0.7])
cbar = plt.colorbar(c_scheme, cax=cbar_ax, location='right', pad='10%')
cbar.set_label('Land Cover Type', fontsize=15)  # Set color bar label
cbar.set_ticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])  # Set specific ticks


# Set color limits and create a title for the entire figure
plt.clim(0, 16)
plt.suptitle('Majority Land Cover Type from 2001 to 2019', size=40)
plt.tight_layout(rect=[0, 0, 0.9, 0.95])

# Show the plot
plt.show()

plt.savefig(r'C:\Users\jons\Desktop\LULC\land_cover_type_from_2001_2019/image_all.jpg')
