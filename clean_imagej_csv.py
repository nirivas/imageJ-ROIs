import pandas as pd
import os
import argparse

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

def process_and_save(input_file):
    # Load the input CSV file
    df = pd.read_csv(input_file, sep='\t', engine='python')

    # Split the ROI data
    df_split = df.iloc[:, 0].apply(split_roi_data)

    # Process X and Y coordinates
    df_split[['X_Coords_List', 'Y_Coords_List']] = df_split['Y_Coords'].apply(process_coordinates)

    # Save the cleaned data to CSV in the same directory
    output_csv = os.path.splitext(input_file)[0] + '_processed.csv'
    df_split.to_csv(output_csv, index=False)

    print(f"Processed CSV saved as {output_csv}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process ROI coordinates from a CSV file and save the cleaned version.")
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')

    # Parse arguments
    args = parser.parse_args()

    # Process the input file and save the output
    process_and_save(args.input_file)

