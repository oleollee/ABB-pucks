import cv2
from pyzbar.pyzbar import decode
import numpy as np


def QR_Scanner(img, counter=0):
    """Scan QR codes from image. Returns position, orientation and image with marked QR codes"""

    angles = [0]*5  # Orientation list for all QR codes
    positions = [0]*5  # Positions of QR codes
    pucksDetected = []  # List of pucks detected

    blur = cv2.bilateralFilter(src=img, d=9, sigmaColor=75, sigmaSpace=75)
    grayscale = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)  # Make grayscale image for filtering and thresholding
    ret,threshBlur = cv2.threshold(grayscale, 50 + counter, 255, cv2.THRESH_BINARY)  # Thresholding for greater contrast

    data = decode(threshBlur)  # Reading the QR-codes and their positions
    sorted_data = sorted(data, key=lambda x: x[0])  # Sort the QR codes in ascending order

    for QR_Code in sorted_data:  # Go through all QR codes
        polygon = np.int32([QR_Code.polygon])  # Convert from int64 to int32, polylines only accepts int32
        cv2.polylines(img, polygon, True, color=(0, 0, 255), thickness=10)  # Draw lines around QR-codes

        points = polygon[0]  # Extract corner points
        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[3][0]
        y2 = points[3][1]

        angle = np.rad2deg(np.arctan2(-(y2 - y1), x2 - x1))  # Calculate the orientation of each QR code
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        position = (sum(x) / len(points), sum(y) / len(points))  # Calculate center of each QR code

        cv2.circle(img, center=(int(position[0]), int(position[1])), radius=10, color=(255, 0, 0), thickness=-1)

        # QR codes have data as "Puck#<number>". Here, extract only the number:
        data_string = str(QR_Code.data, 'utf-8')
        pucknr = int(''.join(filter(str.isdigit, data_string)))

        # Fill in the lists of position, orientation and number of pucks detected:
        positions[pucknr-1] = position
        angles[pucknr-1] = angle
        pucksDetected.append(pucknr)

    return positions, angles, pucksDetected, img
