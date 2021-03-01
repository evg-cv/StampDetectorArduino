import serial
import time

from settings import ARDUINO_PORT, BAUD_RATE


class ArduinoCom:

    def __init__(self):

        self.ard = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=5)
        self.ard_res = "detect"
        self.receive_ret = True
        time.sleep(2)

    def send_command_arduino(self, coordinates):

        coordinates += "\n"
        self.ard.write(coordinates.encode("utf-8"))

        return

    def receive_command_arduino(self):

        while True:
            if not self.receive_ret:
                break
            response = self.ard.read(self.ard.inWaiting())
            decode_res = response.decode().replace("\r\n", "")
            if decode_res != "":
                self.ard_res = decode_res
                print(f"[INFO] Arduino Command: {self.ard_res}")
            time.sleep(0.1)

        return

    def close_port(self):

        if self.ard.isOpen():
            self.ard.close()


if __name__ == '__main__':

    ard_com = ArduinoCom()

    for i in range(3):
        ard_com.send_command_arduino(coordinates="2,3")
