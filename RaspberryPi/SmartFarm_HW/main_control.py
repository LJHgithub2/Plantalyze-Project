import RPi.GPIO as GPIO
import time

class GPIOController:
    def __init__(self, LED_PIN, WATER_PIN, MOTOR_PIN, LED_DURATION, WATER_DURATION, MOTOR_DURATION):
        self.pin_duration_map = {
            LED_PIN: LED_DURATION,
            WATER_PIN: WATER_DURATION,
            MOTOR_PIN: MOTOR_DURATION,
        }
        self.setup()

    def setup_module(self, pin_num):
        GPIO.setup(pin_num, GPIO.OUT)
        GPIO.output(pin_num, GPIO.HIGH)

    def control_module(self, pin_num, duration):        
        GPIO.output(pin_num, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(pin_num, GPIO.HIGH)

    def setup(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            for pin_num in self.pin_duration_map.keys():
                self.setup_module(pin_num)
            return True
        except:
            return False

    # Method to update durations
    def set_duration(self, led_duration=None, water_duration=None, motor_duration=None):
        if led_duration is not None:
            self.pin_duration_map[list(self.pin_duration_map.keys())[0]] = led_duration
        if water_duration is not None:
            self.pin_duration_map[list(self.pin_duration_map.keys())[1]] = water_duration
        if motor_duration is not None:
            self.pin_duration_map[list(self.pin_duration_map.keys())[2]] = motor_duration

    def activate_control(self, pin, duration=None):
        try:
            if not duration:
                duration = self.pin_duration_map[pin]
            self.control_module(pin, duration)
            return True
        except:
            return False

    def run_all(self):
        try:
            for pin_num in self.pin_duration_map.keys():
                self.activate_control(pin_num)
        except KeyboardInterrupt:
            print("\nProgram stopped by user")
