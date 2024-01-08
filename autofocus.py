import serial
import time
import cv2 
from time import sleep
import picamera
from picamera import PiCamera
camera=PiCamera()
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
#51 loops for 100 steps in coarse
def variance(image):
	bg=cv2.GaussianBlur(image,(11,11),0)
	v=cv2.Laplacian(bg,cv2.CV_64F).var()
	return v
def movefin(z,bestz):

	if __name__== "__main__" :
		ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
		ser.reset_input_buffer()
		a="ncclk,{}".format((z[-1]-bestz))
		ser.write(a.encode("utf-8"))
		image=np.empty((240*320*3),dtype=np.uint8)
		camera.capture(image,"bgr")
def autofocus():
	
	
	if __name__ == '__main__':
		z=[]
		var=[]
		l=0
		ser=serial.Serial('/dev/ttyUSB1',9600,timeout=1)
		ser.reset_input_buffer()
		ser1=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
		ser1.reset_input_buffer()
		ser1.write("esz".encode("utf-8"))
		ine=ser1.readline().decode('utf-8').rstrip()
		for i in range(5):
			camera.start_preview()
			camera.resolution=(320,240)
			camera.framerate=24
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			var.append(variance(image))
			z.append(l)
			l+=100
			ser.write("nclk,100".encode("utf-8"))
			ser1.write("esz".encode("utf-8"))
			line=ser.readline().decode('utf-8').rstrip()
			ine=ser1.readline().decode('utf-8').rstrip()
			print(line)
			print(ine)
			time.sleep(2)
	t=(z,var)
	return t

(z,var)=autofocus()
spline=InterpolatedUnivariateSpline(z,var,k=4)
cr_pts=spline.derivative().roots()
cr_pts=np.append(cr_pts,(z[0],z[-1]))
cr_vals=spline(cr_pts)
bestz=cr_pts[np.argmax(cr_vals)]

movefin(z,bestz)

	
