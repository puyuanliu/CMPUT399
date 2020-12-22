
#################################################################
# This function is used to capture images from camera
# We used this function to take image of the calibration sheet
# from different angles
#################################################################

import cv2

cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    key = cv2.waitKey(1)

    if key == ord("q"):
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif key == ord("s"):
        # SPACE pressed
        img_name = "opencv_frame_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()