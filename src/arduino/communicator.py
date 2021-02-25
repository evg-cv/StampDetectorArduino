import serial
import time

from settings import ARDUINO_PORT, BAUD_RATE


class ArduinoCom:

    def __init__(self):

        self.ard = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=5)
        self.ard_res = "detect"
        time.sleep(2)

    def communicate_arduino(self, coordinates):

        coordinates += "\n"
        self.ard.write(coordinates.encode("utf-8"))
        while True:
            response = self.ard.read(self.ard.inWaiting())
            if response:
                break
            time.sleep(0.1)
        self.ard_res = response.decode().replace("\r\n", "")
        print(f"[INFO] Arduino Command: {self.ard_res}")

        return

    def close_port(self):

        if self.ard.isOpen():
            self.ard.close()


if __name__ == '__main__':

    ard_com = ArduinoCom()

    for i in range(3):
        res = ard_com.communicate_arduino(coordinates="2,3")
        print(res)
