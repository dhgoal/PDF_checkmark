import cv2
import numpy as np

# Load the original image
image = cv2.imread("images/page_5.png")
height, width, _ = image.shape  # Get the dimensions of the original image

# Convert the image from BGR to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range of green color in HSV
lower_green = np.array([40, 40, 40])  # Lower bound of green
upper_green = np.array([80, 255, 255])  # Upper bound of green

# Create a mask to only keep the areas that are green
mask = cv2.inRange(hsv, lower_green, upper_green)

# Optional: Apply some morphological operations to close gaps
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize an index for naming images
index = 0

# Loop through the contours to find bounding rectangles and crop images
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # Crop the image using the rectangle's left and right boundaries
    # Extend the top and bottom to the full height of the image
    cropped_image = image[0:height, x : x + w]

    # Save the cropped image with a unique file name
    cv2.imwrite(f"crop/cropped_image_{index}.png", cropped_image)
    index += 1

    # Optionally draw the rectangle on the original image for visualization
    cv2.rectangle(image, (x, 0), (x + w, height), (0, 255, 0), 2)

# Save or display the result
cv2.imwrite(
    "result_with_cropped_areas.png", image
)  # Save the image with rectangles drawn
# cv2.imshow('Image', image)  # Display the image (uncomment this line if running locally)
# cvv.waitKey(0)              # Wait for a key press
# cvv.destroyAllWindows()     # Close the image window
