importClass(Packages.ij.gui.Roi);
importClass(Packages.ij.plugin.frame.RoiManager);
importClass(Packages.java.io.FileWriter);
importClass(Packages.java.io.BufferedWriter);

// Get the ROI manager and the number of ROIs
rm = RoiManager.getInstance();
rois = rm.getRoisAsArray();

if (rois.length == 0) {
    print("No ROIs found.");
    exit();
}

// Create a file to save the ROI coordinates
output_file = new FileWriter("C:/Users.../roi_coordinates.csv");
buffered_writer = new BufferedWriter(output_file);

// Write header to the CSV file
buffered_writer.write("ROI_ID,X_Coords,Y_Coords\n");

for (var i = 0; i < rois.length; i++) {
    roi = rois[i];
    
    // Check if the ROI is a polygon or freehand (you can handle other types if needed)
    if (roi.getType() == Roi.POLYGON || roi.getType() == Roi.FREEROI || roi.getType() == Roi.TRACED_ROI) {
        x_coords = roi.getFloatPolygon().xpoints;
        y_coords = roi.getFloatPolygon().ypoints;
        
        // Write ROI id and coordinates to file
        buffered_writer.write("ROI_" + (i + 1) + ",");
        for (var j = 0; j < x_coords.length; j++) {
            buffered_writer.write(x_coords[j] + "," + y_coords[j]);
            if (j < x_coords.length - 1) {
                buffered_writer.write(";");
            }
        }
        buffered_writer.write("\n");
    }
}

buffered_writer.close();
print("Coordinates saved to file.");
