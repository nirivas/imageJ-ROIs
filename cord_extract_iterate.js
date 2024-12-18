importClass(Packages.ij.gui.Roi);
importClass(Packages.ij.plugin.frame.RoiManager);
importClass(Packages.java.io.FileWriter);
importClass(Packages.java.io.BufferedWriter);
importClass(Packages.java.io.File);

// Specify the folder containing .zip files and the output folder
var inputFolderPath = "C:/Users/nicor/Florida International University/Coral Reef Fisheries - Documents/1. RAPID Diadema/data/raw/CoralProcessing/Macroalgae/202210/ROIs";
var outputFolderPath = "C:/Users/nicor/Florida International University/Coral Reef Fisheries - Documents/1. RAPID Diadema/data/raw/CoralProcessing/Macroalgae/shapefiles/202206";

// Get the folder containing .zip files
var inputFolder = new File(inputFolderPath);

// Ensure the folder exists
if (!inputFolder.isDirectory()) {
    print("The specified input folder does not exist or is not a directory.");
    exit();
}

// Get a list of all .zip files in the folder
var files = inputFolder.listFiles();
for (var i = 0; i < files.length; i++) {
    var file = files[i];
    if (!file.getName().endsWith(".zip")) {
        continue; // Skip non-zip files
    }

    // Load the .zip file into the ROI Manager
    print("Processing: " + file.getName());
    var rm = RoiManager.getRoiManager(); // Get the ROI Manager instance
    rm.runCommand("Reset"); // Clear existing ROIs
    rm.runCommand("Open", file.getAbsolutePath());

    var rois = rm.getRoisAsArray(); // Get all ROIs from the .zip file

    if (rois.length == 0) {
        print("No ROIs found in " + file.getName());
        continue;
    }

    // Create a CSV file with the same name as the .zip file in the output folder
    var csvFileName = file.getName().replace(".zip", ".csv");
    var outputFilePath = outputFolderPath + "/" + csvFileName;
    var output_file = new FileWriter(outputFilePath);
    var buffered_writer = new BufferedWriter(output_file);

    // Write header to the CSV file
    buffered_writer.write("ROI_ID,X_Coords,Y_Coords\n");

    // Iterate through each ROI
    for (var j = 0; j < rois.length; j++) {
        var roi = rois[j];
        if (roi.getType() == Roi.POLYGON || roi.getType() == Roi.FREEROI || roi.getType() == Roi.TRACED_ROI) {
            // Get coordinates for polygon-like ROIs
            var x_coords = roi.getFloatPolygon().xpoints;
            var y_coords = roi.getFloatPolygon().ypoints;

            // Write ROI coordinates
            buffered_writer.write("ROI_" + (j + 1) + ",");
            for (var k = 0; k < x_coords.length; k++) {
                buffered_writer.write(x_coords[k] + "," + y_coords[k]);
                if (k < x_coords.length - 1) {
                    buffered_writer.write(";"); // Separate each coordinate pair with a semicolon
                }
            }
            buffered_writer.write("\n"); // Newline for the next ROI
        } else if (roi.getType() == Roi.RECTANGLE) {
            // Get coordinates for rectangle ROIs
            var bounds = roi.getBounds();
            var x_coords = [bounds.x, bounds.x + bounds.width, bounds.x + bounds.width, bounds.x, bounds.x];
            var y_coords = [bounds.y, bounds.y, bounds.y + bounds.height, bounds.y + bounds.height, bounds.y];

            // Write ROI coordinates
            buffered_writer.write("ROI_" + (j + 1) + ",");
            for (var k = 0; k < x_coords.length; k++) {
                buffered_writer.write(x_coords[k] + "," + y_coords[k]);
                if (k < x_coords.length - 1) {
                    buffered_writer.write(";"); // Separate each coordinate pair with a semicolon
                }
            }
            buffered_writer.write("\n"); // Newline for the next ROI
        } else {
            continue; // Skip unsupported ROI types
        }
    }

    // Close the file writer
    buffered_writer.close();
    print("Coordinates saved to: " + outputFilePath);
}

print("Processing completed.");
