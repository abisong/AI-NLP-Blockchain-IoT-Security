import random
import time

class IoTSimulator:
    def __init__(self):
        self.temperature = 20.0
        self.humidity = 50.0

    def get_sensor_data(self):
        self.temperature += random.uniform(-0.5, 0.5)
        self.humidity += random.uniform(-1, 1)
        self.humidity = max(0, min(100, self.humidity))
        return {
            'temperature': round(self.temperature, 1),
            'humidity': round(self.humidity, 1),
            'timestamp': int(time.time())
        }
