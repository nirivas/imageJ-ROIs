import geopandas as gpd
from shapely.geometry import Polygon
import pandas as pd
import ast
import argparse
import os

# Function to convert X and Y coordinate lists into a Polygon
def create_polygon(x_coords, y_coords):
    # Combine X and Y into (x, y) tuples
    polygon_points = [(x, y) for x, y in zip(x_coords, y_coords)]
    return Polygon(polygon_points)

def process_and_save_shapefile(input_file):
    # Load the cleaned file (assuming CSV in this case)
    df = pd.read_csv(input_file)

    # Convert string representations of lists into actual lists
    df['X_Coords_List'] = df['X_Coords_List'].apply(ast.literal_eval)
    df['Y_Coords_List'] = df['Y_Coords_List'].apply(ast.literal_eval)

    # Create GeoDataFrame from the processed coordinates
    gdf = gpd.GeoDataFrame(df, geometry=df.apply(lambda row: create_polygon(row['X_Coords_List'], row['Y_Coords_List']), axis=1))

    # Set the Coordinate Reference System (CRS), assumed to be EPSG:3857
    gdf.set_crs(epsg=3857, inplace=True)

    # Generate the output file path in the same directory with '_output.shp'
    output_shp = os.path.splitext(input_file)[0] + '_output.shp'

    # Save the GeoDataFrame as a shapefile
    gdf.to_file(output_shp)
    print(f"Shapefile created successfully at {output_shp}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert CSV with coordinates into a Shapefile.")
    parser.add_argument('input_file', type=str, help='Path to the input CSV file.')

    # Parse arguments
    args = parser.parse_args()

    # Process the input file and save the shapefile
    process_and_save_shapefile(args.input_file)
