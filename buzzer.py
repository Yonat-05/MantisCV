import time
import lgpio


class Buzzer:
    def __init__(self):
        self.BUZZER = 18
        self.GPIO_CHIP = 4

        self.chip = lgpio.gpiochip_open(self.GPIO_CHIP)

        lgpio.gpio_claim_output(
            self.chip,
            self.BUZZER,
            0
        )

    def _tone(self, frequency, duration_ms):
        lgpio.tx_pwm(
            self.chip,
            self.BUZZER,
            frequency,
            50
        )

        time.sleep(duration_ms / 1000)

    def _no_tone(self):
        # 0% duty cycle = silent
        # Keep a valid PWM frequency.
        lgpio.tx_pwm(
            self.chip,
            self.BUZZER,
            1000,
            0
        )

    def startup(self):
        melody = [
            (392, 125),
            (370, 125),
            (330, 125),
            (330, 375),
            (370, 250),
            (294, 250),
            (330, 125),
            (220, 375),
        ]

        for frequency, duration in melody:
            self._tone(frequency, duration)
            self._no_tone()
            time.sleep(0.010)

        time.sleep(2)
        self._no_tone()

    def found(self):
        self._tone(660, 100)
        self._no_tone()
        time.sleep(0.03)

        self._tone(880, 150)
        self._no_tone()

    def lost(self):
        self._tone(440, 100)
        self._no_tone()
        time.sleep(0.03)

        self._tone(330, 150)
        self._no_tone()

    def close(self):
        self._no_tone()
        lgpio.gpiochip_close(self.chip)
