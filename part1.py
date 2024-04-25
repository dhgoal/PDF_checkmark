from pdfquery import PDFQuery
from lxml import etree
import cv2
import numpy as np

pdf = PDFQuery("pdf_checkmarks.pdf")

for i in range(2, 5):
    pdf.load(i)

    image = cv2.imread(f"origin/page_{i + 1}.png")
    image = cv2.flip(image, 0)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40, 40, 40])  # Lower bound of green
    upper_green = np.array([80, 255, 255])  # Upper bound of green

    mask = cv2.inRange(hsv, lower_green, upper_green)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pts = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        pts.append((x, x+w))
    
    if len(pts) < 1:
        continue

    pdf.tree.write(f"{i + 1}.xml", pretty_print=True)

    tree = etree.parse(f"{i + 1}.xml")
    elements = tree.xpath("//LTFigure")

    for element in elements:
        x0 = float(element.get('x0'))
        y0 = float(element.get('y0'))
        x1 = float(element.get('x1'))
        y1 = float(element.get('y1'))

        flg = False

        for pt in pts:
            if pt[0] < x1 and x0 < pt[1]:
                flg = True
                break
        
        if not flg:
            continue
        
        top_left_corner = (int(x0), int(y0))
        bottom_right_corner = (int(x1), int(y1))

        if x1 - x0 < 8 and y1 - y0 < 8:
            cv2.rectangle(image, top_left_corner, bottom_right_corner, (0, 255, 0), 1)

    image = cv2.flip(image, 0)
    cv2.imwrite(
        f"res_{i + 1}.png", image
    )