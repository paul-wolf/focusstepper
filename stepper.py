from adafruit_motor import stepper
from adafruit_motorkit import MotorKit


def move(step_size=100, direction=stepper.FORWARD, style=stepper.SINGLE):
    print("move(step_size={}, style={})".format(int(step_size), style))
    kit = MotorKit()
    kit.stepper1.release()
    for i in range(step_size):
        kit.stepper1.onestep(direction=direction, style=style)
