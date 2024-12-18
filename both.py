import geopandas as gpd
from shapely.geometry import Polygon
import pandas as pd
import argparse
import os

# Function to handle splitting the ROI data safely
def split_roi_data(row):
    parts = row.split(',', 2)  # Split into 3 parts: ROI_ID, X_Coords, Y_Coords
    if len(parts) == 3:
        return pd.Series(parts, index=['ROI_ID', 'X_Coords', 'Y_Coords'])
    else:
        return pd.Series([None, None, None], index=['ROI_ID', 'X_Coords', 'Y_Coords'])

# Function to split the coordinate pairs for X and Y
def process_coordinates(coords_str):
    x_coords = []
    y_coords = []
    coord_pairs = coords_str.split(';')
    for pair in coord_pairs:
        if ',' in pair:
            x, y = pair.split(',')
            x_coords.append(float(x))
            y_coords.append(float(y))
    return pd.Series([x_coords, y_coords], index=['X_Coords_List', 'Y_Coords_List'])

# Function to convert X and Y coordinate lists into a Polygon
def create_polygon(x_coords, y_coords):
    # Combine X and Y into (x, y) tuples
    polygon_points = [(x, y) for x, y in zip(x_coords, y_coords)]
    return Polygon(polygon_points)

def process_and_save(input_file):
    # Load the input CSV file using a tab delimiter
    df = pd.read_csv(input_file, sep='\t', engine='python')

    # Split the ROI data
    df_split = df.iloc[:, 0].apply(split_roi_data)

    # Process X and Y coordinates
    df_split[['X_Coords_List', 'Y_Coords_List']] = df_split['Y_Coords'].apply(process_coordinates)

    # Save the cleaned data to CSV in the same directory
    output_csv = os.path.splitext(input_file)[0] + '_processed.csv'
    df_split.to_csv(output_csv, index=False)

    # Create GeoDataFrame from the processed coordinates
    gdf = gpd.GeoDataFrame(df_split, geometry=df_split.apply(lambda row: create_polygon(row['X_Coords_List'], row['Y_Coords_List']), axis=1))

    # Set the Coordinate Reference System (CRS), assumed to be EPSG:3857
    gdf.set_crs(epsg=3857, inplace=True)

    # Save the GeoDataFrame as a shapefile in the same directory
    output_shp = os.path.splitext(input_file)[0] + '_output.shp'
    gdf.to_file(output_shp)

    print(f"Processed CSV saved as {output_csv}")
    print(f"Shapefile created successfully at {output_shp}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process ROI coordinates from all CSV files in a folder and save both cleaned versions and shapefiles.")
    parser.add_argument('folder_path', type=str, help='Path to the folder containing input CSV files')

    # Parse arguments
    args = parser.parse_args()

    # Validate the folder path
    folder_path = args.folder_path
    if not os.path.isdir(folder_path):
        print(f"Error: The specified folder does not exist: {folder_path}")
        exit()

    # Process all CSV files in the specified folder
    for file_name in os.listdir(folder_path):
        # Ignore files with "processed" in the name
        if file_name.endswith('.csv') and "processed" not in file_name.lower():
            input_file_path = os.path.join(folder_path, file_name)
            print(f"Processing: {input_file_path}")
            process_and_save(input_file_path)
        else:
            print(f"Skipping: {file_name} (contains 'processed')")
            
    print("Processing completed for all files.")

