import fitz  # PyMuPDF

pdf_document = fitz.open("pdf_checkmarks.pdf")

# Set the zoom level for scaling; x and y resolutions in dpi (e.g., 300 dpi)
zoom_x = 1.0  # 2x zoom
zoom_y = 1.0  # 2x zoom
mat = fitz.Matrix(zoom_x, zoom_y)  # Create a transformation matrix for scaling

# Define the rectangle for clipping the image
# Coordinates (x0, y0, x1, y1)
# rect = fitz.Rect(x0=10, y0=70, x1=830, y1=500)

# Iterate through the specified range of pages (page 3 to 5)
for page_number in range(2, 5):
    page = pdf_document[page_number]

    # Render page to a pixmap using the transformation matrix
    pix = page.get_pixmap(matrix=mat)
    
    # Save the pixmap as an image, naming it with the page number
    pix.save(f"origin/page_{page_number + 1}.png")

pdf_document.close()  # Close the document after processing
