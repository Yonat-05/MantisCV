import cv2 as cv
import numpy as np

def cameraView():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        exit()

    _, dummyFrame = cap.read()
    height, width, _ = dummyFrame.shape
    frame_center_x = width // 2
    frame_center_y = height // 2

    while True:
        ret, frame = cap.read() #ret(return) is boolean

        if ret:
            frameGaussian = cv.GaussianBlur(frame,(11,11),0)
            frameHSV = cv.cvtColor(frameGaussian, cv.COLOR_BGR2HSV)
            lower_yellow = np.array([22, 50, 50])
            upper_yellow = np.array([38, 255, 255])
            mask = cv.inRange(frameHSV, lower_yellow, upper_yellow)
            contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            #frameContour = cv.drawContours(frame, contours, -1, (0, 0, 255), 3) #uncomment if you want to view the contour

            if len(contours) > 0:
                largest_contour = max(contours, key=cv.contourArea)
                
                if cv.contourArea(largest_contour) > 500:
                    ((x, y), radius) = cv.minEnclosingCircle(largest_contour)
                    center_point = (int(x), int(y))
                    radius = int(radius)
                    cv.circle(frame, center_point, radius, (255, 0, 0), 2)
                    cv.circle(frame, center_point, 5, (0, 0, 255), -1)
            cv.drawMarker(frame, (frame_center_x, frame_center_y), (255, 255, 255), 
            markerType=cv.MARKER_CROSS, 
            markerSize=20, 
            thickness=2)
            cv.imshow('Webcam', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    cameraView()
