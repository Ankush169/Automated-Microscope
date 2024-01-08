import serial
import time
import cv2 
from time import sleep
import picamera
from picamera import PiCamera
camera=PiCamera()
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
def movex(distance):

	if __name__== "__main__" :
		
		
		ser.reset_input_buffer()
		command = "xclk,{}".format(distance)
		ser.write(command.encode("utf-8"))
#40x -395; 10x- 350; 4x-200
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

	
	
if __name__ == '__main__':
	z=[]
	var=[]
	l=0
	
	
	#ser=serial.Serial('/dev/ttyUSB1',9600,timeout=1)
	#ser.reset_input_buffer()
	ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.reset_input_buffer()
	#ser.write("ncclk,150".encode("utf-8"))
	sleep(2)
	
	camera.start_preview()
	camera.resolution=(320,240)
	camera.framerate=24
	
	
	
	ser.write("ncclk,360".encode("utf-8"))
	

	#ser=serial.Serial('/dev/ttyUSB1',9600,timeout=1)
	#ser.reset_input_buffer()
	for i in range(21):
		image=np.empty((240*320*3),dtype=np.uint8)
		camera.capture(image,'bgr')
		image=image.reshape((240,320,3))
		camera.capture("/home/pi/Downloads/10x/image{0}({1}).jpg".format(i,variance(image)))

		var.append(variance(image))
		ser.write("zcclk,50".encode("utf-8"))
		sleep(3)
	var=np.array(var) 
	l=np.argmax(var)

	sleep(2)
	a="zclk,{}".format(1000-l*50)
	ser.write(a.encode("utf-8"))
	camera.resolution=(1920,1088)
	sleep(8)
	camera.capture("/home/pi/Downloads/10x/focusedImage.jpg")
	sleep(2)
	ser.write("nclk,365".encode("utf-8"))
	print(var)
	
	sleep(2)
		
		

		
			

			

#(z,var)=autofocus()
#spline=InterpolatedUnivariateSpline(z,var,k=4)
#cr_pts=spline.derivative().roots()
#cr_pts=np.append(cr_pts,(z[0],z[-1]))
#cr_vals=spline(cr_pts)
#bestz=cr_pts[np.argmax(cr_vals)]

#movefin(z,bestz)
#if __name__=="__main__": 
#	ser=serial.Serial('/dev/ttyUSB1',9600,timeout=1)
#	ser.reset_input_buffer()
#	q="ncclk,{}".format(bestz)
#	ser.write(q.encode("utf-8"))

	
