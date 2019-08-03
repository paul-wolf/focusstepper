from adafruit_motor import stepper
from adafruit_motorkit import MotorKit


def move(step_increment=100, direction=stepper.FORWARD, style=stepper.SINGLE):
    kit = MotorKit()
    kit.stepper1.release()
    for i in range(step_increment):
        kit.stepper1.onestep(direction=direction, style=style)
