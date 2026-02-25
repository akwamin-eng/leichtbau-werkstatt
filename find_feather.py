import cv2
import numpy as np

# Load image
img = cv2.imread('assets/logo-color.png', cv2.IMREAD_UNCHANGED)
if img is None:
    print("Cannot load image")
    exit()

# Assuming background is transparent (alpha channel)
alpha_channel = img[:, :, 3]

# Find contours
contours, _ = cv2.findContours(alpha_channel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f"Found {len(contours)} contours")

# Sort contours by area
contours = sorted(contours, key=cv2.contourArea, reverse=True)

for i, c in enumerate(contours[:5]):
    x, y, w, h = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    print(f"Contour {i}: x={x}, y={y}, w={w}, h={h}, area={area}")

