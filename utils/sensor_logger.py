from sense_hat import SenseHat
import time
import os
from datetime import datetime

class SensorLogger:
    """
    Logs selected Sense HAT sensor data for educational
    and post-flight analysis purposes only.
    This data does NOT affect the ISS speed calculation ;)
    """

    def __init__(self, file_path: str):
        self.sense = SenseHat()
        self.file_path = file_path

        # Write CSV header once
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write(
                    "datetime,accel_x,accel_y,accel_z,"
                    "gyro_x,gyro_y,gyro_z,"
                    "temp,pressure,humidity\n"
                )

    def log_once(self):
        t = datetime.utcnow()  # current UTC time
        t_str = t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # ms precision

        accel = self.sense.get_accelerometer_raw()
        gyro = self.sense.get_gyroscope_raw()
        temp = self.sense.get_temperature()
        pressure = self.sense.get_pressure()
        humidity = self.sense.get_humidity()

        with open(self.file_path, "a") as f:
            f.write(
                f"{t_str},"
                f"{accel['x']:.4f},{accel['y']:.4f},{accel['z']:.4f},"
                f"{gyro['x']:.4f},{gyro['y']:.4f},{gyro['z']:.4f},"
                f"{temp:.2f},{pressure:.2f},{humidity:.2f}\n"
            )