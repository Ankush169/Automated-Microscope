import serial
import time
import cv2 
from time import sleep
import picamera
from autofocus import camera
#camera=PiCamera()
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
from autofocus import variance,auto
def movex(distance):
	if __name__== "__main__" :
		camera.start_preview()
		ser.reset_input_buffer()
		command = "xcclk,{}".format(distance)
		ser.write(command.encode("utf-8"))
		print("hello")
print("step1")
movex(100)
auto()


		


		

		
