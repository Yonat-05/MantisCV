import cv2 as cv
import numpy as np

class ColorTracker:
    def __init__(self):
        self.lower_yellow = np.array([30, 90, 90])
        self.upper_yellow = np.array([40, 255, 255])

    def find_target(self, frame):
        frameGaussian = cv.GaussianBlur(frame,(11,11),0)
        frameHSV = cv.cvtColor(frameGaussian, cv.COLOR_BGR2HSV)
        mask = cv.inRange(frameHSV, self.lower_yellow, self.upper_yellow)
        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            largest_contour = max(contours, key=cv.contourArea)
            
            if cv.contourArea(largest_contour) > 500:
                ((x, y), radius) = cv.minEnclosingCircle(largest_contour)
                center_point = (int(x), int(y))
                radius = int(radius)
                return center_point
            
        return None
