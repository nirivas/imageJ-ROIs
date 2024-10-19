# imageJ-ROIs
Scripts to convert ROIs to csvs, csvs to shapefiles using JAVA and Python

Dependencies that need to be installed are  ***geopandas, shapely.geometry, Polygon, pandas, ast, argparse, os***

# To create a shapefile: 

A) To create a shapefile

  1. Open image and ROI manager in Imaje-J/FIJI
  2. Open File->New Script and switch the Language to JavaScript
  3. Copy paste "Coordinate_extractor_IMAGEJ_ROI code into the editor (or open file)
  4. Change the output destination and name on line 16

     `output_file = new FileWriter("C:/Users.../roi_coordinates.csv");`
  5. Open command terminal and switch directory to location of "both.py"
  6. In command terminal type
     
     `C:\Users\nicor> cd 'path to directory with both.py'`
     
  7. You should now see the new directory
  8. Type
     
       `python both.py 'path to .csv file created in javascript above'`

This will create a clean csv with the ROI coordinates and a shapefile in the same location as input file

# To create a SVG

  1. Open image and ROI manager in Image-J/FIGI
  2. Opel File-> New Script and switch the language to python
  3. Copy paste the svggenerator code or open file
  4. Switch output to desired destination and name on line 34
     
       `path = "C:/Users/nicor/Downloads/testsvg3.svg"`
