import serial # this is imported for eastablishing the connection
import time 
import cv2 # for calculating the variance
from time import sleep 
import picamera # to control the activities the camera like capturing 
from picamera import PiCamera
camera=PiCamera()
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1) # serial connection is established where /dev/ttyUSB0 is port and 9600 is serial no.
sleep(1)

# global x, y and z is for telling about the position of platform in terms of steps from the initial position
global x  
x=0
global y
y=0
global z
z=0
def movexclock(distance):  # defined for moving the platform in clockwise x direction (distance=no. of steps)
	global x
	

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "xclk,{}".format(distance)
		ser.write(command.encode("utf-8"))
		x=x+distance 
		print('x:',x)
		
		

def movexanticlock(distance): # defined for moving the platform in anticlockwise x direction (distance=no. of steps)
	global x

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "xcclk,{}".format(distance)
		ser.write(command.encode("utf-8"))	
		x=x-distance
		print('x:',x)		
		
		
def movey(steps):# defined for moving the platform in anticlockwise y direction
	global y
	if __name__== "__main__" :
		camera.start_preview()
		command="ycclk,{}".format(steps)
		ser.write(command.encode("utf-8"))
		y=y+steps
		sleep(1)	
		print('y:',y)
		
		
def movezclock(distance):# defined for moving the platform in clockwise x direction using the fine motor (distance=no. of steps)
	global z
	

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "zclk,{}".format(distance)
		ser.write(command.encode("utf-8"))
		z=z-distance	
		print('z:',z)
		
def movezanticlock(distance):  # defined for moving the platform in anticlockwise x direction using the fine motor (distance=no. of steps)
	global z

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "zcclk,{}".format(distance)
		ser.write(command.encode("utf-8"))	
		z=z+distance			
		print('z:',z)	
		
		
		
#40x -395; 10x- 350; 4x-200
def variance(image):  # variance is difined to calculate the variance of each image for autofocus the variance which have the highest variance will give the best focussed image
	g=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	threshold = cv2.adaptiveThreshold(g,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,blockSize=11,C=2)
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	enhd = clahe.apply(threshold)
	denoised = cv2.GaussianBlur(enhd,(3,3),0)
	background = cv2.medianBlur(denoised,21)
	subtracted = cv2.absdiff(denoised,background)
	
	#kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	#opened=cv2.morphologyEx(threshold,cv2.MORPH_OPEN,kernel,iterations=2)
	#bg=cv2.GaussianBlur(subtracted,(11,11),0)
	#pb=cv2.equalizeHist(bg)
	v=cv2.Laplacian(subtracted,cv2.CV_64F).var()
	print(v)
	return v
	
def movefin(z,bestz):

	if __name__== "__main__" :
		ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
		ser.reset_input_buffer()
		a="ncclk,{}".format((z[-1]-bestz))
		ser.write(a.encode("utf-8"))
		image=np.empty((240*320*3),dtype=np.uint8)
		camera.capture(image,"bgr")
def init():       # for moving the platform from any position to initial position
	if __name__== "__main__" :
		ser.reset_input_buffer()
		ser.write("init".encode("utf-8"))
	
	
def auto():	# for focussing for the first time from  intial point 
	
	if __name__ == '__main__':
		z=[]
		var=[]
		l=0
		camera.start_preview()
		
		#ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
		#ser.reset_input_buffer()
	
		ser.reset_input_buffer()
		#ser.write("ncclk,150".encode("utf-8"))
		sleep(1)
		
		
		camera.resolution=(320,240)
		camera.framerate=24
		
		#ser=serial.Serial('/dev/ttyUSB1',9600,timeout=1)
		#ser.reset_input_buffer()
		#ser.write("zcclk,12150".encode("utf-8"))
		movezanticlock(14300) # first platform is moved 
		sleep(30);
		#x=0
		#y=0
		ze=[]
		for i in range(21):
			image=np.empty((480*640*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((480,640,3))
			camera.capture("/home/pi/Downloads/40x/New/image{0}({1}).jpg".format(i,variance(image)))
			#sleep(1)
			var.append(variance(image))
			#z.append(i)
			movezanticlock(50)
			#ser.write("zcclk,50".encode("utf-8"))
			#ze=ze+50
			ze.append((i+1)*50)
			sleep(1)
			
		var=np.array(var) 
		l=np.argmax(var)
		sleep(2)
		movezclock(1050-(l*50))
		#a="zclk,{}".format(1050-l*50)
		#ser.write(a.encode("utf-8"))
		camera.resolution=(1920,1088)
		sleep((1050-l*50)/400+2)
		camera.capture("/home/pi/Downloads/40x autoscan/blood/focusedimage.jpg")
		sleep(2)
		#ser.write("init".encode("utf-8"))
		
		

		print(var)
		print(ze)
		print(ze[l])
		print('max var:',max(var))


def auto3(i,j):
	z=[]
	var=[]
	l=0
	if __name__=="__main__":
		camera.resolution=(320,240)
		camera.meter_mode = 'average'
		camera.awb_mode = 'auto'
		camera.framerate=24
		movezclock(100)
		#ser.reset_input_buffer()
		#ser.write("zclk,200".encode("utf-8"))
		sleep(1)
		for k in range(11):#11
			camera.start_preview()
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			#sleep(1)

			var.append(variance(image))
			movezanticlock(25)#20 30
			#ser.write("zcclk,50".encode("utf-8"))
			sleep(1)
		
		sleep(1)
		var=np.array(var) 
		l=np.argmax(var)
		a = 275-l*25#550-(l*50)#220
		movezclock(a)
		sleep((550-l*50)/400+2) #((330-l*50)/200+2)
		
		image=np.empty((240*320*3),dtype=np.uint8)
		camera.capture(image,'bgr')
		image=image.reshape((240,320,3))
		e=variance(image)
		print (e)
		# For validating whether the variance at the point is the same as measured before
		sleep(5)
		
		camera.resolution=(1920,1088)
		sleep((330-l*30)/200+2) #((330-l*50)/200+2)
		#camera.contrast = 60
		#camera.sharpness = 50
		#camera.meter_mode = 'average'
		#camera.awb_mode = 'auto'
		camera.capture("/home/pi/Downloads/40x autoscan/blood/imagerow{0},{1}.jpg".format(i,j))
		sleep(1)
		
		

		print(var)

print(time)

auto()
init()
print(time)

sleep(1)
def scan():
	if __name__=="__main__":
		s=0
		m=0
		for i in range(3):
			for j in range(3):
				var=[]
				
				if (j%2==0 and i>=0):
					auto3(i,j)
				else:
					camera.resolution=(1920,1088)
					camera.contrast = 60
		
					camera.awb_mode = 'auto'
		
					camera.meter_mode = 'average'
					camera.capture("/home/pi/Downloads/40x autoscan/blood/scan/imagerow{0},{1}.jpg".format(i,j))
		
				if(i%2==0):
					movexclock(14)#4
				else:	
					movexanticlock(14)#4
												
				sleep(2)
							
				sleep(1)
				
			movey(13)#3
			
			sleep(1)	
		init()
		#ser.write("zclk,13000".encode("utf-8"))
	
scan()
print(x)
print(y)
print(z)
			

		
			

			

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

	
