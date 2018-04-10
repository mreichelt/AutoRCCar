"""
Reference:
OpenCV-Python Tutorials - Camera Calibration and 3D Reconstruction
http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
"""
from pathlib import Path
import cv2
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


images = glob.glob('chess_board/*.jpg')

target_folder = Path('chess_board_patterns')
target_folder.mkdir(exist_ok=True, parents=True)

for file_name in images:
    image = cv2.imread(file_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # find chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 5), None)

    # add object points, image points
    if ret:
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # draw and display the corners
        cv2.drawChessboardCorners(image, (7, 5), corners, ret)
        cv2.imwrite(str(target_folder / Path(file_name).name), image)

if __name__ == '__main__':
    pass
