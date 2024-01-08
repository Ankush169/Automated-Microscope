import serial  # this is imported for eastablishing the connection
import time
import cv2    # for calculating the variance
from time import sleep
import picamera   # to control the activities the camera like capturing 
from picamera import PiCamera
camera=PiCamera()
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)    # serial connection is established where /dev/ttyUSB0 is port and 9600 is serial no.
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
		
		

def movexanticlock(distance):  # defined for moving the platform in anticlockwise x direction (distance=no. of steps)
	global x

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "xcclk,{}".format(distance)
		ser.write(command.encode("utf-8"))	
		x=x-distance
		print('x:',x)		
		
		
def movey(steps):          # defined for moving the platform in anticlockwise y direction
	global y
	if __name__== "__main__" :
		camera.start_preview()
		command="ycclk,{}".format(steps)
		ser.write(command.encode("utf-8"))
		y=y+steps
		sleep(1)	
		print('y:',y)
		
		
def movezclock(distance):    # defined for moving the platform in clockwise x direction using the fine motor (distance=no. of steps)
	global z
	

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "zclk,{}".format(distance)
		ser.write(command.encode("utf-8"))
		z=z-distance	
		print('z:',z)
		
def movezanticlock(distance):    # defined for moving the platform in anticlockwise x direction using the fine motor (distance=no. of steps)
	global z

	if __name__== "__main__" :
		camera.start_preview()
		
		
		ser.reset_input_buffer()
		command = "zcclk,{}".format(distance)
		ser.write(command.encode("utf-8"))	
		z=z+distance			
		print('z:',z)	
		
		
		
#40x -395; 10x- 350; 4x-200
def variance(image):                  # variance is difined to calculate the variance of each image for autofocus the variance which have the highest variance will give the best focussed image
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
def init():            # for moving the platform from any position to initial position
	if __name__== "__main__" :
		ser.reset_input_buffer()
		ser.write("init".encode("utf-8"))
	
	
def auto():       # for focussing for the first time from  intial point 	
	
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
		movezanticlock(12000)   # 12000 steps is moved in anticlockwise direction for focussing 
		sleep(30);
		#x=0
		#y=0
		ze=[]
		for i in range(25):        # After moving 12000 steps the platform move to 1250 steps more by moving 50 steps each time and capturing the image and then calculating the variance
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			camera.capture("/home/pi/Downloads/10x/New/image{0}({1}).jpg".format(i,variance(image))) # image capturing
			sleep(1)
			var.append(variance(image))  # adding variance of new images in the empty list of var.
			#z.append(i)
			movezanticlock(50)  # moving 50 steps each time 
			#ser.write("zcclk,50".encode("utf-8"))
			#ze=ze+50
			ze.append((i+1)*50)
			sleep(1)
			
		var=np.array(var) # list of variance of all 25 images 
		l=np.argmax(var) # index of maximum variance in the var list
		sleep(2)
		movezclock((1290-l*50))  # moved the platform from 12000+1250 to best focussed point(12000+1250-l*50)  but we moved 1290 -l*50 because of backlash of motor
		sleep((1300-l*50)/400+2)
		camera.resolution=(320,240)
		camera.framerate=24
		image=np.empty((240*320*3),dtype=np.uint8)
		camera.capture(image,'bgr')
		image=image.reshape((240,320,3))
		m= variance(image)  # variance of captured image actually the variance of best focussed image is different than the captured image because of back lash platform is not moving at the right point(max variance point)
		print (m)
		#a="zclk,{}".format(1050-l*50)
		#ser.write(a.encode("utf-8"))
		camera.resolution=(1920,1088) 
		sleep((1250-l*50)/400+2)
		camera.capture("/home/pi/Downloads/10x autoscan/413/focusedimage.jpg")
		sleep(2)
		#ser.write("init".encode("utf-8"))
		
		

		print(var)
		print(ze)
		print(ze[l])
		print('max var:',max(var))

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
		zee=[]
		for i in range(21):
				
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			sleep(1)

			var.append(variance(image))
			ser.write("zcclk,50".encode("utf-8"))
			
			sleep(1)
			sleep(1)
		
		var=np.array(var) 
		l=np.argmax(var)
		sleep(2)
		a="zclk,{}".format(1000-l*50)
		ser.write(a.encode("utf-8"))
		
		camera.resolution=(1920,1088)
		sleep((1050-l*50)/400+2)
		#camera.contrast = 60
		#camera.meter_mode = 'average'
		#camera.awb_mode = 'auto'
		camera.capture("/home/pi/Downloads/10x autoscan/test3/imagerow{0},{1}.jpg".format(i,j))
		sleep(1)
		
		

		print(var)
		print(zee)
		

def auto3(i,j):  # for focussing during scanning after certain number of steps (as per requirement the number of images) 
	z=[]
	var=[]
	l=0
	if __name__=="__main__":
		camera.resolution=(320,240)
		camera.framerate=24
		movezclock(200) # after first each focus 200 steps moved in clock direction i.e. downward
		#ser.reset_input_buffer()
		#ser.write("zclk,200".encode("utf-8"))
		sleep(1)
		zee=[]
		for k in range(12):  #12 images is taken after a certain number of steps during scanning
			camera.start_preview()
			image=np.empty((240*320*3),dtype=np.uint8)
			camera.capture(image,'bgr')
			image=image.reshape((240,320,3))
			

			var.append(variance(image))
			movezanticlock(50) # during scanning 50 steps moved 
			#ser.write("zcclk,50".encode("utf-8"))
			zee.append((k+1)*50)
			sleep(1)
		
		sleep(1)
		var=np.array(var) #list of varince
		l=np.argmax(var)# index of max variance
		#a="zclk,{}".format(550-l*50)
		movezclock(610-l*50) # moved to best focussed image should be 600-l*50  but due to backlash it is 610-l*50
		sleep((550-l*50)/400+2) 
		camera.resolution=(320,240)
		camera.framerate=24
		image=np.empty((240*320*3),dtype=np.uint8)
		camera.capture(image,'bgr')
		image=image.reshape((240,320,3))
		n=variance(image) #variance of captured image 
		print(n)
		#ser.write(a.encode("utf-8"))
		camera.resolution=(1920,1088)
		
		#camera.contrast = 60
		#camera.meter_mode = 'average'
		#camera.awb_mode = 'auto'
		camera.capture("/home/pi/Downloads/10x autoscan/412/imagerow{0},{1}.jpg".format(i,j))
		sleep(1)
		
		

		print(var)
		print(zee)
		print(zee[l])
		print('max var:',max(var))
		


print("time")	
auto()
print("time")


sleep(1)
def scan(): # defined for scanning the slide 
	if __name__=="__main__":
		s=0
		m=0
		
		for i in range(7): # for y direction (1 times platform is moved in y direction after moving the platform 7 steps in x direction each time)
			for j in range(7): # for x direction (7 steps moved in x direction means 7 images it captures in x direction )
				var=[]
				if (j%4==0 and i>0):          #in each 4rth steps from second row images are focussed by auto3 function
					auto3(i,j)
				else:
					camera.resolution=(1920,1088)
					#camera.contrast = 60
					#camera.meter_mode = 'average'
					#camera.awb_mode = 'auto'
					camera.capture("/home/pi/Downloads/10x autoscan/412/imagerow{0},{1}.jpg".format(i,j)) 
				if(i%2==0):  # for moving the platform in x anticlock and clock direction
					movexclock(15) # in x direction each image covers 15 steps of platform so we move the platform by 15 steps for next image
				else:
					movexanticlock(15)
												
				sleep(2)
									
				sleep(1)
						
			
			movey(12) # each field of view covers in y direction covers 12 steps means we need to move 12 steps for taking next image in y direction
			
			sleep(1)	
		init()
		#ser.write("zclk,13000".encode("utf-8"))
	
scan()
print(x)
print(y)
print(z)
			

		
			

	
