import board
import busio
import lgpio

from adafruit_pca9685 import PCA9685


class PanTilt:
    def __init__(self):
        # -----------------------------
        # PCA9685 setup
        # -----------------------------

        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.pca = PCA9685(
            self.i2c,
            address=0x40,
            reference_clock_speed=27000000
        )

        self.pca.frequency = 50

        self.PAN = 0
        self.TILT = 2

        # Calibrated mechanical positions
        self.PAN_CENTER = 340
        self.TILT_CENTER = 350

        # Conservative mechanical limits
        self.PAN_MIN = 220
        self.PAN_MAX = 460
        self.TILT_MIN = 320
        self.TILT_MAX = 450

        # -----------------------------
        # Motor power status GPIO
        # -----------------------------

        self.gpio_chip = lgpio.gpiochip_open(4)
        self.MOTOR_POWER_PIN = 17

        lgpio.gpio_claim_input(
            self.gpio_chip,
            self.MOTOR_POWER_PIN
        )

    def _set_servo(self, channel, pulse):
        self.pca.channels[channel].duty_cycle = int(
            pulse * 65535 / 4096
        )

    def set_pan(self, pulse):
        pulse = max(self.PAN_MIN, min(self.PAN_MAX, pulse))
        self._set_servo(self.PAN, pulse)

    def set_tilt(self, pulse):
        pulse = max(self.TILT_MIN, min(self.TILT_MAX, pulse))
        self._set_servo(self.TILT, pulse)

    def center(self):
        self.set_pan(self.PAN_CENTER)
        self.set_tilt(self.TILT_CENTER)

    def motor_power_enabled(self):
        return lgpio.gpio_read(
            self.gpio_chip,
            self.MOTOR_POWER_PIN
        ) == 1

    def close(self):
        self.pca.deinit()
        lgpio.gpiochip_close(self.gpio_chip)
