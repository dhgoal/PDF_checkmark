from pdfquery import PDFQuery
from lxml import etree
import cv2
import fitz
import numpy as np
import pandas as pd

low_limit = 22
high_limit = 42

pdf_document = fitz.open("pdf_checkmarks.pdf")

for page_number in range(2, 5):
    page = pdf_document[page_number]
    pix = page.get_pixmap()
    pix.save(f"origin/page_{page_number + 1}.png")

pdf_document.close()

pdf = PDFQuery("pdf_checkmarks.pdf")

with pd.ExcelWriter('output.xlsx', engine="xlsxwriter") as writer:
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
        fields = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            pts.append((x, x + w))

        if len(pts) < 1:
            continue

        pdf.tree.write(f"{i + 1}.xml", pretty_print=True)

        tree = etree.parse(f"{i + 1}.xml")
        elements = tree.xpath("//LTTextBoxVertical")

        df = pd.DataFrame()

        for element in elements:
            x0 = float(element.get("x0"))
            y0 = float(element.get("y0"))
            x1 = float(element.get("x1"))
            y1 = float(element.get("y1"))

            flg = False

            for pt in pts:
                if pt[0] < x1 and x0 < pt[1]:
                    flg = True
                    break
            if not flg:
                continue
            fields.append(element)
        
        texts = []
        for field in fields:
            col = []

            f_x0 = float(field.get("x0"))
            f_x1 = float(field.get("x1"))
            f_y0 = float(field.get("y0"))
            f_y1 = float(field.get("y1"))

            text = field.text

            elements = tree.xpath("//LTFigure")

            for element in elements:
                x0 = float(element.get("x0"))
                y0 = float(element.get("y0"))
                x1 = float(element.get("x1"))
                y1 = float(element.get("y1"))

                if not (x1 - x0 < 8 and y1 - y0 < 8):
                    continue

                if f_x0 < x1 and x0 < f_x1:
                    col.append((y0, y1))

            col = sorted(col, reverse=True)

            res = []

            # gap check
            start = col[0][0]
            while True:
                if start < f_y0 - low_limit and start > f_y0 - high_limit:
                    break
                start += 28.5
                res.append("")

            for item in col:
                res.append("yes")
            df[text] = res
            texts.append(text)

        df = df[texts[::-1]]
        df.to_excel(writer, sheet_name=f"page_{i + 1}", index=False)
