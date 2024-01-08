import serial
import time
import cv2 
from time import sleep
import picamera
from picamera import PiCamera
camera=PiCamera()
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
def movexclock(distance):

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "xclk,{}".format(distance)
		ser.write(command.encode("utf-8"))
		

def movexanticlock(distance):

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "xcclk,{}".format(distance)
		ser.write(command.encode("utf-8"))			
		
		
def movey(steps):
	if __name__== "__main__" :
		camera.start_preview()
		command="ycclk,{}".format(steps)
		ser.write(command.encode("utf-8"))
		sleep(1)		
		
		
		
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

	
	
def auto():	
	
	if __name__ == '__main__':
		z=[]
		var=[]
		l=0
		camera.start_preview()
		
		
		#ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
		#ser.reset_input_buffer()
		
		ser.reset_input_buffer()
		#ser.write("ncclk,150".encode("utf-8"))
		sleep(2)
		
		
		camera.resolution=(320,240)
		camera.framerate=24
		
		
		

		
		#ser=serial.Serial('/dev/ttyUSB1',9600,timeout=1)
		#ser.reset_input_buffer()
		ser.write("zcclk,12000".encode("utf-8"))
		sleep(30);
		for i in range(21):
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			camera.capture("/home/pi/Downloads/10x/New/image{0}({1}).jpg".format(i,variance(image)))
			sleep(1)
			var.append(variance(image))
			ser.write("zcclk,50".encode("utf-8"))
			sleep(1)
		
		var=np.array(var) 
		l=np.argmax(var)
		sleep(2)
		a="zclk,{}".format(1050-l*50)
		ser.write(a.encode("utf-8"))
		camera.resolution=(1920,1088)
		sleep((1050-l*50)/400+2)
		camera.capture("/home/pi/Downloads/10x autoscan/test3/focusedimage.jpg")
		sleep(2)
		#ser.write("init".encode("utf-8"))
		
		

		print(var)

def auto2(i,j):
	z=[]
	var=[]
	l=0
	if __name__=="__main__":
		camera.start_preview()
		camera.resolution=(320,240)
		camera.framerate=24
		ser.reset_input_buffer()
		ser.write("zclk,500".encode("utf-8"))
		sleep(2)
		for i in range(21):
				
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			sleep(1)

			var.append(variance(image))
			ser.write("zcclk,50".encode("utf-8"))
			sleep(1)
		
		var=np.array(var) 
		l=np.argmax(var)
		sleep(2)
		a="zclk,{}".format(1000-l*50)
		ser.write(a.encode("utf-8"))
		camera.resolution=(1920,1088)
		sleep((1050-l*50)/400+2)
		camera.capture("/home/pi/Downloads/10x autoscan/test3/imagerow{0},{1}.jpg".format(i,j))
		sleep(1)
		
		

		print(var)

def auto3(i):
	z=[]
	var=[]
	l=0
	if __name__=="__main__":
		camera.start_preview()
		camera.resolution=(320,240)
		camera.framerate=24
		ser.reset_input_buffer()
		ser.write("zclk,500".encode("utf-8"))
		sleep(2)
		for i in range(21):
				
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			sleep(1)

			var.append(variance(image))
			ser.write("zcclk,50".encode("utf-8"))
			sleep(1)
		
		var=np.array(var) 
		l=np.argmax(var)
		sleep(2)
		a="zclk,{}".format(1000-l*50)
		ser.write(a.encode("utf-8"))
		camera.resolution=(1920,1088)
		sleep((1050-l*50)/400+2)
		camera.capture("/home/pi/Downloads/10x autoscan/test2/imagerow{0},{1}.jpg".format(i,0))
		sleep(1)
		
		

		print(var)
	

def scan():
	if __name__=="__main__":
		s=0
		m=0
		for i in range(11):
			for j in range(20):
				if(i%2==0):
					movexclock(15)
				else:
					movexanticlock(15)
				
								
				sleep(2)
				camera.resolution=(1920,1088)
				image=np.empty((1088*1920*3),dtype=np.uint8)
				camera.capture(image,'bgr')
				sleep(1)
				image=image.reshape((1088,1920,3))
				if (abs(variance(image)-m)>= 2) and m>0 and m>variance(image):
					k=variance(image)
					ser.write("zclk,50".encode("utf-8"))
					sleep(1)
					camera.capture(image,'bgr')
				
					image=image.reshape((1088,1920,3))
					sleep(1)
					if variance(image) <k:
						while variance(image)<m :
							ser.write("zcclk,50".encode("utf-8"))
							sleep(1)
							camera.capture(image,'bgr')
				
							image=image.reshape((1088,1920,3))	
							print(variance(image),m)
					else:
						while variance(image)<m :
							ser.write("zclk,50".encode("utf-8"))
							sleep(1)
							camera.capture(image,'bgr')
							image=image.reshape((1088,1920,3))
					m=variance(image)
						
				else:
					m=variance(image)
					
					camera.capture("/home/pi/Downloads/10x autoscan/test3/imagerow{0},{1}.jpg".format(i,j))
				
				sleep(1)
				
			
			
			movey(20)
			
			sleep(1)	
			
		ser.write("zclk,13000".encode("utf-8"))
	
scan()
		
		

		
			

			

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

	
