from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

def encoder_callback(data):
    print("called callback")
    print(data)


class DifferentialDrive():
    def __init__(self, board, pins_mapping):
        self.board = board
        self.pins_mapping = pins_mapping
        self.setup()

    def setup(self):
        """Setup pins"""
        print("Setup pins")
        values = {
            "L_CTRL_1": Constants.OUTPUT,
            "L_CTRL_2": Constants.OUTPUT,
            "PWM_L": Constants.PWM,
            "R_CTRL_1": Constants.OUTPUT,
            "R_CTRL_2": Constants.OUTPUT,
            "PWM_R": Constants.PWM
        }
        
        for pin, mode in values.items():
            self.board.set_pin_mode(self.pins_mapping[pin], mode)

        self.board.set_pin_mode(
                self.pins_mapping["L_ENCODER"],
                board.INPUT,
                board.DIGITAL,
                encoder_callback
        )
        self.board.set_pin_mode(
                self.pins_mapping["R_ENCODER"],
                board.INPUT,
                board.DIGITAL,
                encoder_callback
        )
#        self.board.encoder_config(
#                self.pins_mapping["L_ENCODER"],
#                self.pins_mapping["R_ENCODER"],
#                cb=encoder_callback,
#                cb_type=Constants.CB_TYPE_DIRECT
#        )
        self.stop()

    def stop(self):
        print("Stop")
        digital_values = {
            "L_CTRL_1": 1,
            "L_CTRL_2": 0,
            "R_CTRL_1": 1,
            "R_CTRL_2": 0,
        }
        analog_values = {
            "PWM_L": 0,
            "PWM_R": 0
        }

        for k, v in digital_values.items():
            self.board.digital_write(self.pins_mapping[k], v)
        for k, v in analog_values.items():
            self.board.analog_write(self.pins_mapping[k], v)
    def forward(self, speed):
        print("Soumia go forward!")
        digital_values = {
            "L_CTRL_1": 1,
            "L_CTRL_2": 0,
            "R_CTRL_1": 1,
            "R_CTRL_2": 0,
        }
        analog_values = {
            "PWM_L": speed,
            "PWM_R": speed
        }

        for k, v in digital_values.items():
            self.board.digital_write(self.pins_mapping[k], v)
        for k, v in analog_values.items():
            self.board.analog_write(self.pins_mapping[k], v)
    def backward(self, speed):
        print("Soumia go backward!")
        digital_values = {
            "L_CTRL_1": 0,
            "L_CTRL_2": 1,
            "R_CTRL_1": 0,
            "R_CTRL_2": 1,
        }
        analog_values = {
            "PWM_L": speed,
            "PWM_R": speed
        }

        for k, v in digital_values.items():
            self.board.digital_write(self.pins_mapping[k], v)
        for k, v in analog_values.items():
            self.board.analog_write(self.pins_mapping[k], v)
    def left(self, speed):
        print("Soumia go left!")
        digital_values = {
            "L_CTRL_1": 1,
            "L_CTRL_2": 0,
            "R_CTRL_1": 1,
            "R_CTRL_2": 0,
        }
        analog_values = {
            "PWM_L": int(speed/2),
            "PWM_R": speed
        }

        for k, v in digital_values.items():
            self.board.digital_write(self.pins_mapping[k], v)
        for k, v in analog_values.items():
            self.board.analog_write(self.pins_mapping[k], v)
    def right(self, speed):
        print("Soumia go right!")
        digital_values = {
            "L_CTRL_1": 1,
            "L_CTRL_2": 0,
            "R_CTRL_1": 1,
            "R_CTRL_2": 0,
        }
        analog_values = {
            "PWM_L": speed,
            "PWM_R": int(speed/2)
        }

        for k, v in digital_values.items():
            self.board.digital_write(self.pins_mapping[k], v)
        for k, v in analog_values.items():
            self.board.analog_write(self.pins_mapping[k], v)      

if __name__ == "__main__":
    # RedBot motor pins from RedBot.h
    pins_mapping = {}
    pins_mapping["L_CTRL_1"] = 5
    pins_mapping["L_CTRL_2"] = 4
    pins_mapping["PWM_L"] = 9
    pins_mapping["L_ENCODER"] = 2

    pins_mapping["R_CTRL_1"] = 6
    pins_mapping["R_CTRL_2"] = 7
    pins_mapping["PWM_R"] = 10
    pins_mapping["R_ENCODER"] = 3

    board = PyMata3()
    default_speed = 244
    dd = DifferentialDrive(board, pins_mapping)
    while True:
        dd.forward(default_speed)
        board.sleep(2.0)

        dd.backward(default_speed)
        board.sleep(2.0)

        dd.left(default_speed)
        board.sleep(2.0)

        dd.right(default_speed)
        board.sleep(2.0)
        
        dd.stop()
        board.sleep(5.0)

    dd.stop()
