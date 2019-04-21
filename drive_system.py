from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import numpy as np

class DifferentialDrive():
    def __init__(self, board, pins_mapping):
        self.PULSE_PEREVOLUTION = 16

        self.TS = 0.001 # 1ms sampling interval

        self.L_K_P = 1 # @TODO this needs to be tuned.
        self.L_K_D = 1 # @TODO this needs to be tuned.
        self.L_K_I = 1 # @TODO this needs to be tuned.

        self.R_K_P = 1 # @TODO this needs to be tuned.
        self.R_K_D = 1 # @TODO this needs to be tuned.
        self.R_K_I = 1 # @TODO this needs to be tuned.


        # Encoder pulses count
        self.total_left_ticks = 0
        self.total_right_ticks = 0
        
        # Wheels speed at any instant
        self.v_l = 0
        self.v_r = 0

        self.board = board
        self.pins_mapping = pins_mapping
        self.setup()

    def _encoder_callback(self, data):
        if data[0] == self.pins_mapping["L_ENCODER"]:
            self.total_left_ticks += 1
        if data[0] == self.pins_mapping["R_ENCODER"]:
            self.total_right_ticks += 1
        print(self.total_left_ticks)
 
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
                Constants.INPUT,
                callback=self._encoder_callback,
                cb_type=Constants.CB_TYPE_DIRECT
        )
         self.board.set_pin_mode(
                self.pins_mapping["R_ENCODER"],
                Constants.INPUT,
                callback=self._encoder_callback,
                cb_type=Constants.CB_TYPE_DIRECT
        )
        
        self.stop()

    def get_mesured_speed(self):
        denom = self.PULSE_PEREVOLUTION * self.TS
        mv_l = self.total_left_ticks / denom
        mv_r = self.total_right_ticks / denom
        return (mv_l, mv_r)

    def transfer_function(self, Il, Ir):
        if len(Il) != len(Ir):
            raise ValueError("Left input size should be equal to right input size %d != %d" % (len(Il), len(Ir)))

        Ol = np.array()
        Or = np.array()
        
        for i in range(len(Il)):
            self.total_left_ticks = 0
            self.total_right_ticks = 0

            analog_values = {
                "PWM_L": Il[i],
                "PWM_R": Ir[i]
            }
            for k, v in analog_values.items():
                self.board.analog_write(self.pins_mapping[k], v)

            self.board.sleep(self.TS)
            mv_l, mv_r = self.get_mesured_speed()
            Ol.append(mv_l)
            Or.append(mv_r)

        return (Ol, Or)
        
#    def execute(self, direction, v_l, v_r, t):
#        output = []
#        if direction == 1: 
#            self.set_forward()
#        else:
#            self.set_backrward()
#
#        intervals = int(t/self.TS)
#
#        self.total_left_ticks = 0
#        self.total_right_ticks = 0
#
#        base_pwm = 0
#        i_l_term = 0
#        i_r_term = 0
#        old_e_l, old_e_r = (v_l - mv_l, v_r - mv_r)
#        for i in range(intervals):
#            board.sleep(TS)
#            mv_l, mv_r = self.get_mesured_speed()
#            output.append((mv_l, mv_r))
#            e_l, e_r = (v_l - mv_l, v_r - mv_r)
#            # Compute proportional term:
#            p_l_term = self.L_K_P * e_l
#            p_r_term = self.R_K_P * e_r
#
#            # Compute integral term:
#            i_l_term += self.L_K_I * e_l
#            i_r_term += self.R_K_I * e_r
#
#            # Compute derivative term:
#            d_l_term = self.L_K_D * (e_l - old_e_l) / self.TS
#            d_r_term = self.R_K_D * (e_r - old_e_r) / self.TS
#
#            i_l_term, i_r_term = self._integral_term_limiter(i_l_term, i_r_term)
#
#            u_l = base_pwm + p_l_term + i_l_term + d_l_term
#            u_r = base_pwm + p_r_term + i_r_term + d_r_term
#
#            analog_values = {
#                "PWM_L": int(u_l),
#                "PWM_R": int(u_r)
#            }
#            for k, v in analog_values.items():
#                self.board.analog_write(self.pins_mapping[k], v)
#        return output   

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

    def set_forward(self):
        print("Soumia go forward!")
        digital_values = {
            "L_CTRL_1": 1,
            "L_CTRL_2": 0,
            "R_CTRL_1": 1,
            "R_CTRL_2": 0,
        }
        for k, v in digital_values.items():
            self.board.digital_write(self.pins_mapping[k], v)
    def set_backward(self):
        print("Soumia go backward!")
        digital_values = {
            "L_CTRL_1": 0,
            "L_CTRL_2": 1,
            "R_CTRL_1": 0,
            "R_CTRL_2": 1,
        }
        for k, v in digital_values.items():
            self.board.digital_write(self.pins_mapping[k], v)

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
    default_speed = 100
    dd = DifferentialDrive(board, pins_mapping)
    Il = np.concatenate([np.zeros(10), np.ones(990)* default_speed])
    Ir = np.concatenate([np.zeros(10), np.ones(990)* default_speed])

    Ol, Or = dd.transfer_function(self, Il, Ir)
    from matplotlib import pyplot as plt
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.plot(Il)
    ax1.plot(Ol)
    ax1.set_title('System response')
    ax2.plot(Il)
    ax2.plot(Ol)

    plt.savefig('system_response.pdf')

    dd.stop()
