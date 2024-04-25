from pdfquery import PDFQuery
from lxml import etree
import cv2

pdf = PDFQuery("pdf_checkmarks.pdf")

for i in range(2, 5):
    pdf.load(i)

    image = cv2.imread(f"origin/page_{i + 1}.png")
    image = cv2.flip(image, 1)

    pdf.tree.write(f"{i + 1}.xml", pretty_print=True)

    tree = etree.parse(f"{i + 1}.xml")
    elements = tree.xpath("//LTFigure")

    for element in elements:
        x0 = float(element.get('x0'))
        y0 = float(element.get('y0'))
        x1 = float(element.get('x1'))
        y1 = float(element.get('y1'))
        matrix = element.get('matrix')
        

        top_left_corner = (int(x0), int(y0))
        bottom_right_corner = (int(x1), int(y1))

        if x1 - x0 < 8 and y1 - y0 < 8:
            # print(f"{x0}, {y0}, {x1}, {y1}")
            # cv2.putText(image, id, top_left_corner, 2, 1, (255, 0, 0))
            cv2.rectangle(image, top_left_corner, bottom_right_corner, (0, 255, 0), 1)

    image = cv2.flip(image, 1)
    cv2.imwrite(
        f"res_{i + 1}.png", image
    )