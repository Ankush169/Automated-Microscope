import numpy as np
from time import sleep
from datetime import datetime

def autofocus(camera, ser):
    var = []
    for i in range(21):
        image = np.empty((240 * 320 * 3), dtype=np.uint8)
        camera.capture(image, 'bgr', use_video_port=True)
        image = image.reshape((240, 320, 3))
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "/home/pi/Pictures/10x/image{0}({1}).jpg".format(i, variance(image))
        camera.capture(filename, use_video_port=True)
        
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
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "/home/pi/Downloads/10x/focusedImage_{}.jpg".format(timestamp)
    camera.capture(filename)
    
    sleep(2)

# Example usage
camera = ...  # Initialize your camera object
ser = ...  # Initialize your serial object

autofocus(camera, ser)
