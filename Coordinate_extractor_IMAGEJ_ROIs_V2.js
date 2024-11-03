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
output_file = new FileWriter("C:/Users/nicor/Downloads/roi_coordinates.csv");
buffered_writer = new BufferedWriter(output_file);

// Write header to the CSV file
buffered_writer.write("ROI_ID,X_Coords,Y_Coords\n");

for (var i = 0; i < rois.length; i++) {
    roi = rois[i];
    
    // Check if the ROI is a polygon, freehand, traced ROI, or rectangle
    if (roi.getType() == Roi.POLYGON || roi.getType() == Roi.FREEROI || roi.getType() == Roi.TRACED_ROI) {
        x_coords = roi.getFloatPolygon().xpoints;
        y_coords = roi.getFloatPolygon().ypoints;
        
    } else if (roi.getType() == Roi.RECTANGLE) {
        // For rectangles, use getBounds() to get the four corner points
        bounds = roi.getBounds();
        x_coords = [bounds.x, bounds.x + bounds.width, bounds.x + bounds.width, bounds.x, bounds.x];
        y_coords = [bounds.y, bounds.y, bounds.y + bounds.height, bounds.y + bounds.height, bounds.y];
    } else {
        continue;  // Skip unsupported ROI types
    }
    
    // Write ROI ID and coordinates to the CSV file
    buffered_writer.write("ROI_" + (i + 1) + ",");
    for (var j = 0; j < x_coords.length; j++) {
        buffered_writer.write(x_coords[j] + "," + y_coords[j]);
        if (j < x_coords.length - 1) {
            buffered_writer.write(";");  // Separate each coordinate pair with a semicolon
        }
    }
    buffered_writer.write("\n");  // Newline for the next ROI
}

// Close the file writer
buffered_writer.close();
print("Coordinates saved to file.");
