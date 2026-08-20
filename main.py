import cv2 as cv
from vision import ColorTracker
from control import PIDController

def main():
    tracker = ColorTracker()
    pan_pid = PIDController(0.02, 0, 0)
    tilt_pid = PIDController(0.02, 0, 0)

    cap = cv.VideoCapture(0)
    _, dummyFrame = cap.read()
    height, width, _ = dummyFrame.shape
    frame_center_x = width // 2
    frame_center_y = height // 2
    pan_angle = 90.0
    tilt_angle = 90.0

    while True:
        ret, frame = cap.read()
        
        if ret:
            target = tracker.find_target(frame)
            
            if target is not None:
                cv.circle(frame, target, 5, (0, 0, 255), -1)
                error_x = target[0] - frame_center_x
                error_y = frame_center_y - target[1]

                pan_step = pan_pid.update(error_x)
                tilt_step = tilt_pid.update(error_y)
                pan_angle += pan_step
                tilt_angle += tilt_step
                pan_angle = max(0.0, min(180.0, pan_angle))
                tilt_angle = max(0.0, min(180.0, tilt_angle))
                print(f"Pan: {pan_angle} | Tilt: {tilt_angle}")

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
    main()
