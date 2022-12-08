import pandas as pd
import geopandas as gpd
import fiona as fi
from shapely.geometry import Point, LineString, Polygon
import numpy
import csv
import shapely
import rasterstats
import rasterio 

Dist01 = pd.read_csv('C:\lab2\districts\district01.txt', sep='\t')
Dist05 = pd.read_csv('C:\lab2\districts\district05.txt', sep='\t')
Dist06 = pd.read_csv('C:\lab2\districts\district06.txt', sep='\t')


df1 = pd.DataFrame(Dist01) 
df1 = df1.assign(district='01') 
df1["num_coords"] = gpd.points_from_xy(df1.X, df1.Y)
df1 = df1.groupby('district').agg(
        geometry = pd.NamedAgg(column='num_coords', aggfunc = lambda x: Polygon(x.values))
    ).reset_index()
gdf1 = gpd.GeoDataFrame(df1, geometry='geometry')
 
    
df5 = pd.DataFrame(Dist05) 
df5 = df5.assign(district='05')
df5["num_coords"] = gpd.points_from_xy(df5.X, df5.Y)
df5 = df5.groupby('district').agg(
        geometry = pd.NamedAgg(column='num_coords', aggfunc = lambda x: Polygon(x.values))
    ).reset_index()
gdf5 = gpd.GeoDataFrame(df5, geometry='geometry')


df6 = pd.DataFrame(Dist06) 
df6 = df6.assign(district='06')
df6["num_coords"] = gpd.points_from_xy(df6.X, df6.Y)
df6 = df6.groupby('district').agg(
        geometry = pd.NamedAgg(column='num_coords', aggfunc = lambda x: Polygon(x.values))
    ).reset_index()
gdf6 = gpd.GeoDataFrame(df6, geometry='geometry')



raster1 = rasterio.open(r'C:\Users\lreyr\OneDrive\Documents\lab2\data\agriculture\GLOBCOVER_2004_lab2.tif')
finalraster = raster1.read(1).astype("float")
affine1 = raster1.transform
array1 = raster1.read(1)

RS1 = rasterstats.zonal_stats(gdf1, finalraster, affine = affine1, nodata=numpy.nan, stats = ['count', 'sum'], geojson_out = True) 
RS2 = rasterstats.zonal_stats(gdf5, finalraster, affine = affine1, nodata=numpy.nan, stats = ['count', 'sum'], geojson_out = True) 
RS3 = rasterstats.zonal_stats(gdf6, finalraster, affine = affine1, nodata=numpy.nan, stats = ['count', 'sum'], geojson_out = True) 

RS1_percent_04 = round(35922.0/89799 * 100)
RS2_percent_04 = round(6639.0/18585 * 100)
RS3_percent_04 = round(39629.0/86459 * 100)


raster2 = rasterio.open(r'C:\Users\lreyr\OneDrive\Documents\lab2\data\agriculture\GLOBCOVER_2009_lab2.tif')
finalraster2 = raster2.read(1).astype("float")
affine2 = raster1.transform

RS4 = rasterstats.zonal_stats(gdf1, finalraster2, affine = affine2, nodata=numpy.nan, stats = ['count', 'sum'], geojson_out = True) 
RS5 = rasterstats.zonal_stats(gdf5, finalraster2, affine = affine2, nodata=numpy.nan, stats = ['count', 'sum'], geojson_out = True) 
RS6 = rasterstats.zonal_stats(gdf6, finalraster2, affine = affine2, nodata=numpy.nan, stats = ['count', 'sum'], geojson_out = True) 

RS4_percent_09 = round(49487/89799 * 100)
RS5_percent_09 = round(6449.0/18585 * 100)
RS6_percent_09 = round(39185/86459 * 100)


print(f'The amount of agricultural land of district 1 in 2004 is {RS1_percent_04}%')
print(f'The amount of agricultural land of district 1 in 2009 is {RS4_percent_09}%')
print(f'The amount of agricultural land of district 5 in 2004 is {RS2_percent_04}%')
print(f'The amount of agricultural land of district 1 in 2009 is {RS5_percent_09}%')
print(f'The amount of agricultural land of district 1 in 2004 is {RS3_percent_04}%')
print(f'The amount of agricultural land of district 1 in 2009 is {RS6_percent_09}%')

