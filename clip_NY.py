import rasterio

from rasterio.windows import from_bounds

# Define the bounding box coordinates
west, south, east, north = -74.3, 40.5, -73.7, 40.9

import pyproj

def reproject_bbox(west, south, east, north, source_crs, target_crs):
    # Define the source and target CRS
    in_proj = pyproj.Proj(proj='latlong', datum='WGS84')
    out_proj = pyproj.Proj(proj='moll', datum='WGS84')  # Mollweide
    
    # Reproject the lower left and upper right coordinates
    west, south = pyproj.transform(in_proj, out_proj, west, south)
    east, north = pyproj.transform(in_proj, out_proj, east, north)
    
    return west, south, east, north

# Your original bounding box in WGS84
west, south, east, north = -74.3, 40.5, -73.7, 40.9

# Reproject the bounding box to Mollweide
west, south, east, north = reproject_bbox(west, south, east, north, 'EPSG:4326', 'EPSG:54009')

# print(west, south, east, north)


with rasterio.open('GHS_BUILT_S_E2018_GLOBE_R2023A_54009_10_V1_0.tif') as src:
    # Calculate the window to extract based on the bounding box
    window = from_bounds(west, south, east, north, src.transform)
    
    # Read the data from the window
    data = src.read(window=window)
    
    # Define the metadata for the new GeoTIFF
    profile = src.profile
    profile['width'] = window.width
    profile['height'] = window.height
    profile['transform'] = rasterio.windows.transform(window, src.transform)

    # Save the extracted data to a new GeoTIFF
    with rasterio.open('nyc_original.tif', 'w', **profile) as dest:
        dest.write(data)
