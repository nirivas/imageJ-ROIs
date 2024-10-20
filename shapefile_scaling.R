
library(sf)
library(tidyverse)

# Replace with the actual file path
shapefile <- st_read("C:/Users/nicor/OneDrive - Florida International University/Desktop/New folder (2)/roi_coordinates_output.shp")

# Replace ROI_ID with known feature label i.e., last ROI in csv
known_feature <- shapefile %>%
  filter(ROI_ID == "ROI_326")

# Get the coordinates of the polygon
coords <- st_coordinates(known_feature)

# Calculate pairwise distances between all points
dist_matrix <- as.matrix(dist(coords[, 1:2]))  # Only consider x and y coordinates

# Find the maximum distance
max_width <- max(dist_matrix)

# Print the longest width
print(max_width)

# Define the desired width, .5 for scale bars .3175 for clipboards
desired_width <- 0.5  # in meters

# Calculate the scale factor
scale_factor <- desired_width / max_width

# Scale all features
shapefile_scaled <- shapefile %>%
  mutate(geometry = st_geometry(geometry) * scale_factor)

# Save the scaled shapefile
st_write(shapefile_scaled, "C:/Users/nicor/OneDrive - Florida International University/Desktop/New folder (2)/scaled_shapefile.shp")

# Check the original CRS of the shapefile
original_crs <- st_crs(shapefile)

# Apply the original CRS to the scaled shapefile
st_crs(shapefile_scaled) <- original_crs

# Now write the scaled shapefile again
st_write(shapefile_scaled, "C:/Users/nicor/OneDrive - Florida International University/Desktop/New folder (2)/scaled_shapefile2.shp")


