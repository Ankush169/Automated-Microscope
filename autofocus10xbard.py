import numpy as np
import time
import serial

def autofocus(camera, ser):
  """
  Performs autofocus on the camera.

  Args:
    camera: The camera object.
    ser: The serial object to communicate with the focus motor.

  Returns:
    The focused image.
  """

  var = []
  for i in range(21):
    image = np.empty((240*320*3), dtype=np.uint8)
    camera.capture(image, 'bgr', use_video_port=True)
    image = image.reshape((240, 320, 3))
    var.append(variance(image))
    ser.write("zcclk,50".encode("utf-8"))
    time.sleep(2)

  var = np.array(var)
  l = np.argmax(var)
  time.sleep(2)

  a = "zclk,{}".format(1000-l*50)
  ser.write(a.encode("utf-8"))

  camera.resolution = (1920, 1080)
  time.sleep(8)
  focused_image = camera.capture("/home/pi/Downloads/10x/focusedImage.jpg")
  return focused_image

if __name__ == "__main__":
  camera = cv2.VideoCapture(0)
  ser = serial.Serial("/dev/ttyUSB0", 9600)
  focused_image = autofocus(camera, ser)
  cv2.imshow("Focused Image", focused_image)
  cv2.waitKey(0)
