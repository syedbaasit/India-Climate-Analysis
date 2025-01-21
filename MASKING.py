import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import geopandas as gpd
from shapely.geometry import Polygon


# shi_data_f array.DataArray't2m'latitude: 153longitude: 153valid_time: 123 

# Select a specific time step to plot
time_step = 23  # Plot the first time step
shi_to_plot = shi_data_f.isel(valid_time=time_step).values

# Get the latitude and longitude
lats = shi_data['latitude'].values
lons = shi_data['longitude'].values

# Load India shapefile using geopandas
india_shapefile = gpd.read_file(r"D:\HBAASIT\Monsoon_data_mn_5678\T\SHI\india_boundary.geojson")

# Create a polygon for India from the shapefile
india_polygon = india_shapefile.geometry.unary_union

# Create the Basemap
fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(
    projection='cyl',  # Cylindrical projection
    llcrnrlat=lats.min(), urcrnrlat=lats.max(),  # Latitude bounds
    llcrnrlon=lons.min(), urcrnrlon=lons.max(),  # Longitude bounds
    resolution='l',  # Resolution ('l' for low)
    ax=ax
)

# Draw coastlines, countries, and parallels/meridians
m.drawcoastlines()
# m.drawcountries()
m.drawparallels(np.arange(-90., 91., 5.), labels=[1, 0, 0, 0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 5.), labels=[0, 0, 0, 1], fontsize=10)

# Clip the SHI data based on the India boundary
lon_grid, lat_grid = np.meshgrid(lons, lats)
x, y = m(lon_grid, lat_grid)

# Create a mask where the SHI values will be clipped outside the boundary
mask = np.array([india_polygon.contains(Point(lon, lat)) for lon, lat in zip(lon_grid.flatten(), lat_grid.flatten())])
mask = mask.reshape(lon_grid.shape)

# Apply the mask to the SHI data
shi_to_plot_clipped = np.ma.masked_where(~mask, shi_to_plot)

# Plot the clipped SHI data
c = m.pcolormesh(x, y, shi_to_plot_clipped, cmap='jet', shading='auto')

# Add a color bar
plt.colorbar(c, ax=ax, orientation='vertical', label='SHI')

valid_time_dt = shi_data_f.valid_time.isel(valid_time=time_step).values
# Add a title
plt.title(f'SHI on {np.datetime_as_string(valid_time_dt, unit="D")} ', fontsize=15)

# Show the plot
plt.show()
