import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

class Car:
	def __init__(self, in1, in2, in3, in4, led):
		self.PIN_IN1 = in1
		self.PIN_IN2 = in2
		self.PIN_IN3 = in3
		self.PIN_IN4 = in4
		self.PIN_LED = led
		self.BoolLedToggle = False
		self.motorControl = Adafruit_PCA9685.PCA9685();
		self.motorControl.set_pwm_freq(50);
		self.FORWARD = [self.PIN_IN2, self.PIN_IN3]
		self.BACKWARD = [self.PIN_IN1, self.PIN_IN4]
	
	def __del__(self):
		GPIO.output(self.PIN_IN1, False);
		GPIO.output(self.PIN_IN2, False);
		GPIO.output(self.PIN_IN3, False);
		GPIO.output(self.PIN_IN4, False);
		GPIO.cleanup();
	def setup(self):
		GPIO.setmode(GPIO.BOARD); 			 # Set GBUS to BOARD (not BCM)
		GPIO.setup(self.PIN_IN1, GPIO.OUT);  # in1 to OUTPUT
		GPIO.setup(self.PIN_IN2, GPIO.OUT);  # in2 to OUTPUT
		GPIO.setup(self.PIN_IN3, GPIO.OUT);  # in3 to OUTPUT
		GPIO.setup(self.PIN_IN4, GPIO.OUT);  # in4 to OUTPUT
		GPIO.setup(self.PIN_LED, GPIO.OUT);  # LED to OUTPUT
		
	def SetAllFalse(self):
		GPIO.output(self.PIN_IN1, False);
		GPIO.output(self.PIN_IN2, False);
		GPIO.output(self.PIN_IN3, False);
		GPIO.output(self.PIN_IN4, False);
	
	def setFalse(self, MODE):
		GPIO.output(MODE[0], False);
		GPIO.output(MODE[1], False);
		
	
	def ToggleLed(self):
		self.BoolLedToggle = not self.BoolLedToggle
		GPIO.output(self.PIN_LED, self.BoolLedToggle);
	
	def forward(self):
#		GPIO.setup()
		GPIO.output(self.PIN_IN2, True);
		GPIO.output(self.PIN_IN3, True);
		GPIO.output(self.PIN_IN1, False);
		GPIO.output(self.PIN_IN4, False);
		time.sleep(0.001);
#		self.SetAllFalse();

	def backward(self):
#		GPIO.setup()
		GPIO.output(self.PIN_IN1, True);
		GPIO.output(self.PIN_IN4, True);
		GPIO.output(self.PIN_IN2, False);
		GPIO.output(self.PIN_IN3, False)
		time.sleep(0.001);
#		self.SetAllFalse();
	
	def Turn(self, servoN, position):
		self.motorControl.set_pwm(servoN, 0, position)
			

"""
PIN_IN1 -> 7  given control input 1 on L298N driver
PIN_IN2 -> 11 given To control input 2 on L298N driver
PIN_IN3 -> 13 given To control input 3 on L298N driver
PIN_IN4 -> 15 given To control input 4 on L298N driver
PIN_LED -> 19 given To control LED
"""
