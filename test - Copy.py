import sys
import cv2
import numpy as np
import time


ROOT_NODE = -1

misc = '''
All parameters are chosen to solve the problem in the tests, more general parameters would be useful
'''

authors = '''
Emanuel Di Nardo
Antonio Riviezzo
Liliana Romano
'''


def usage():
    print
    'python countobj.py [mode][fidelity][fidelityValue]'
    print
    '\tmode : video (default) | image | h-help | info'
    print
    '\tfidelity : activate fidelity range'
    print
    '\tfidelityValue : [0.0, 1.0] default 0.7'
    print
    '\tFor help digits h or help'
    print
    '\tInfo for authors and disclaimer'


if __name__ == '__main__':
    mode = 'image'
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    if mode == 'video':
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print
            'No video devices'

        mog = cv2.BackgroundSubtractorMOG()

        while camera.grab():
            _, frame = camera.retrieve()
            frame = frame[50:700, 200:1000]  # Restrict the a ROI
            # frame = cv2.blur(frame, (13, 13)) # Some defects
            # frame = cv2.bilateralFilter(frame, 15, 100, 10) # Too slow
            frame = cv2.medianBlur(frame, 15)  # Preserve edges (if it is applicable)
            framebw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, framet = cv2.threshold(framebw, 125, 255,
                                      cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # Thresholding using otsu

            framet = cv2.morphologyEx(framet, cv2.MORPH_OPEN, (
            5, 5))  # Remove survived noise and simplify objects (less inner contours and false contours)

            bgs = mog.apply(framet,
                            learningRate=0.05)  # This step is useful to stop counting when an object is placed/removed

            cv2.imshow('bgs', bgs)
            k = cv2.waitKey(33)

            if (np.count_nonzero(bgs) > 300):
                continue

            frame2 = framet.copy()
            c, h = cv2.findContours(frame2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # Find contours
            print(c,h)
            totalContours = 0
            br = []
            for i in xrange(len(c)):
                if h[0][i][3] == ROOT_NODE and cv2.contourArea(
                        c[i]) > 50:  # Only external contours are useful for counting, small area are removed
                    totalContours += 1
                    poly = cv2.approxPolyDP(c[i], 5, True)
                    print(poly)
                    br.append(cv2.boundingRect(poly))
            for b in br:
                cv2.rectangle(frame, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 3)
            cv2.imshow('frame', frame)
            k = cv2.waitKey(33)
            if k == ord('q'):
                break
            print
            'Total contours: ', totalContours

        camera.release()
    elif mode == 'image':
        print("Time is", time.time())
        a = time.time()
        time.sleep(2)
        print("Time is", time.time())
        b = time.time()
        print("difference is", b-a)

        fidelity = False
        fidelityValue = .7
        if len(sys.argv) > 2:
            fidelity = bool(sys.argv[2])
        if len(sys.argv) > 3:
            fidelityValue = float(sys.argv[3])

        # For images
        img = cv2.imread('test.png')
        imgCopy = img.copy()
        img = cv2.medianBlur(img, 15)
        redLower = np.array([170, 100, 100])
        redUpper = np.array([179, 255, 255])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, redLower, redUpper)
        mask = cv2.erode(mask, None, iterations=2)
        img = cv2.dilate(mask, None, iterations=2)
        # img = cv2.adaptiveBilateralFilter(img, (5, 5), 150) # Preserve edges
        # img = cv2.blur(img, (3,3))
        imgt = img
        cv2.imshow('temp', imgt)
        # _, imgt = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY_INV)
        imgt = cv2.morphologyEx(imgt, cv2.MORPH_OPEN, (5, 5))

        img2 = imgt.copy()
        _,c, h = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        fidelityRange = 0
        if fidelity:
            maxArea = .0
            for i in c:  # With images it is convenient to know the greater area
                area = cv2.contourArea(i)
                if area > maxArea:
                    maxArea = area
            fidelityRange = maxArea - (
                        maxArea * fidelityValue) # If objects have same size it prevents false detection

        totalContours = 0

        br = []
        for i in range(len(c)):
            if h[0][i][3] == ROOT_NODE and cv2.contourArea(c[i]) >= fidelityRange:
                totalContours += 1
                approx = cv2.approxPolyDP(c[i], 3, True)
                print(approx)
                br.append(cv2.boundingRect(approx))
        for b in br:
            #cv2.rectangle(imgCopy, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 3)
            cv2.circle(imgCopy, (int((b[0]+b[0] + b[2])/2), int((b[1]+b[1] + b[3])/2)),23, (255, 255, 0), 3)
        cv2.imshow('image', imgCopy)
        cv2.waitKey(0)