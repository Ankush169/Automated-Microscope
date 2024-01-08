import serial
import time
import cv2 
from time import sleep
from datetime import datetime
import picamera
from picamera import PiCamera
camera=PiCamera()
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
ser.reset_input_buffer()

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

def autofocus(camera, ser):
    var = []
    
    for i in range(21):
        image = np.empty((240 * 320 * 3), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((240, 320, 3))
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "/home/pi/Pictures/10x/image{0}({1}).jpg".format(i, variance(image))
        camera.capture(filename)
        
        var.append(variance(image))
        ser.write("zcclk,50".encode("utf-8"))
        sleep(2)
    
    var = np.array(var)
    l = np.argmax(var)
    sleep(2)
    a = "zclk,{}".format(1000 - l * 50)
    ser.write(a.encode("utf-8"))
    
    camera.resolution = (1920, 1080)
    sleep(8)
    
    #timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "/home/pi/Pictures/10x/auto/focusedImage1.jpg"
    camera.capture(filename)
    sleep(2)
    #camera.close()

def finefocus(camera, ser):
    var = []
    time.sleep(3)
    for i in range(11):
        camera.resolution=(320,240)
        image = np.empty((240 * 320 * 3), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((240, 320, 3))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "/home/pi/Pictures/10x/image{0}({1}).jpg".format(i, variance(image))
        camera.capture(filename)
        
        var.append(variance(image))
        ser.write("zcclk,20".encode("utf-8"))
        sleep(2)
    
    var = np.array(var)
    l = np.argmax(var)
    sleep(2)
    a = "zclk,{}".format(200 - l * 20)
    ser.write(a.encode("utf-8"))
    camera.resolution = (1920, 1080)
    sleep(8)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "/home/pi/Pictures/10x/auto/focusedImage_{}.jpg".format(timestamp)
    camera.capture(filename)
    sleep(2)
    #ser.write("zclk,100".encode("utf-8"))
if __name__ == '__main__':
	z=[]
	var=[]
	l=0
	sleep(2)
	camera.resolution=(320,240)
	camera.start_preview()
	camera.framerate=24
	ser.write("ncclk,350".encode("utf-8"))
	autofocus(camera, ser)
	time.sleep(5)
	
	for i in range (10):
		camera.resolution=(320,240)
		camera.start_preview()
		camera.framerate=24
		ser.write("xclk,13".encode("utf-8"))
		time.sleep(2)
		ser.write("zclk,100".encode("utf-8"))
		time.sleep(1)
		finefocus(camera, ser)
		time.sleep(5)  
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

	
