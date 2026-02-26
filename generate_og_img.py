import cv2
import os

# Set paths
video_path = 'assets/loop_hd.mp4'
output_path = 'assets/og-preview.jpg'

# Open the video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get total frames to pick a good shot (e.g., halfway through)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
target_frame = total_frames // 2

# Navigate to target frame
cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
ret, frame = cap.read()

if ret:
    # Save frame as JPG
    cv2.imwrite(output_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"Successfully saved high-quality frame to {output_path}")
else:
    print("Error: Could not read frame.")

cap.release()
