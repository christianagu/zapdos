import os
import cv2
import numpy as np

# Define the path to your directory containing calibration images
directory_path = "./configPics"

# Retrieve all files in the directory
all_files = os.listdir(directory_path)

# Filter for image files
calibration_image_filenames = [os.path.join(directory_path, f) for f in all_files if f.endswith('.jpg')]

# Termination criteria for refining chessboard corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points: (0,0,0), (1,0,0), (2,0,0) ..., (6,5,0)
objp = np.zeros((6*7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

objpoints = []  # 3D points in real-world space
imgpoints = []  # 2D points in image plane

for fname in calibration_image_filenames:
    print(f"Processing: {fname}")
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (4, 6), None)

    if ret:
        objpoints.append(objp)
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners_refined)
        
        # Visualize detected corners
        cv2.drawChessboardCorners(img, (7, 6), corners_refined, ret)
        cv2.imshow('Corners', img)
        cv2.waitKey(0)

    # Calibrate camera after processing all images
    if len(objpoints) > 0 and len(imgpoints) > 0:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    else:
        print("No valid image points and object points found for calibration.")



    if ret:
        objpoints.append(objp)
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners_refined)
         
        # Visualize detected corners
        cv2.drawChessboardCorners(img, (7, 6), corners_refined, ret)
        cv2.imshow('Corners', img)
        cv2.waitKey(0)


# Calibrate camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
