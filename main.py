import cv2 as cv

from vision import ColorTracker
from control import PIDController
from hardware import PanTilt
from buzzer import Buzzer


def main():
    tracker = ColorTracker()
    hardware = PanTilt()
    buzzer = Buzzer()

    pan_pid = PIDController(0.05, 0, 0)
    tilt_pid = PIDController(0.03, 0, 0)

    DEADBAND = 5

    if not hardware.motor_power_enabled():
        print("Motor power OFF. Cannot start tracking.")
        hardware.close()
        buzzer.close()
        return

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Failed to open camera.")
        hardware.close()
        buzzer.close()
        return

    _, dummy_frame = cap.read()

    if dummy_frame is None:
        print("Failed to read camera frame.")
        cap.release()
        hardware.close()
        buzzer.close()
        return

    height, width, _ = dummy_frame.shape

    frame_center_x = width // 2
    frame_center_y = height // 2

    pan_position = hardware.PAN_CENTER
    tilt_position = hardware.TILT_CENTER

    hardware.center()

    print("Motor power ON.")
    print("Playing startup melody...")

    buzzer.startup()

    print("Tracking started.")
    print("Press Ctrl+C to stop.")

    # None = no target state established yet
    # True = target currently visible
    # False = target was previously visible but is now lost
    target_found = None

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to read frame.")
                continue

            target = tracker.find_target(frame)

            if target is not None:

                if target_found is not True:
                    print("Target FOUND.")
                    buzzer.found()

                target_found = True

                error_x = frame_center_x - target[0]
                error_y = frame_center_y - target[1]

                if abs(error_x) < DEADBAND:
                    error_x = 0

                if abs(error_y) < DEADBAND:
                    error_y = 0

                pan_step = pan_pid.update(error_x)
                tilt_step = tilt_pid.update(error_y)

                pan_position += pan_step
                tilt_position += tilt_step

                pan_position = max(
                    hardware.PAN_MIN,
                    min(hardware.PAN_MAX, pan_position)
                )

                tilt_position = max(
                    hardware.TILT_MIN,
                    min(hardware.TILT_MAX, tilt_position)
                )

                hardware.set_pan(pan_position)
                hardware.set_tilt(tilt_position)

                print(
                    f"Target: {target} | "
                    f"Error: ({error_x}, {error_y}) | "
                    f"Pan: {pan_position:.2f} | "
                    f"Tilt: {tilt_position:.2f}"
                )

            else:

                if target_found is True:
                    print("Target LOST.")
                    buzzer.lost()

                target_found = False

    except KeyboardInterrupt:
        print("\nStopping tracking...")

    finally:
        cap.release()
        hardware.close()
        buzzer.close()
        print("Hardware interfaces closed.")


if __name__ == "__main__":
    main()
