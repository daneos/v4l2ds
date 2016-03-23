from PyTango import AttrWriteType, AttrDataFormat, EncodedAttribute, DevEncoded
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command, device_property
from PyTango.server import server_run
from numpy import ndarray

import cv2
import time

class v4l2Device(Device):
	__metaclass__ = DeviceMeta

	cam_id = device_property(dtype=int)

	frame = attribute(label="Image frame", dtype=DevEncoded, format="RawImage",
					  access=AttrWriteType.READ,
					  fget="get_frame",
					  doc="Frame captured from camera")

	def init_device(self):
		Device.init_device(self)
		self.cap = cv2.VideoCapture(self.cam_id)
		self.cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)

	def get_frame(self):
		print "reading from cam: %s" % time.time()
		enc = EncodedAttribute()
		r, img = self.cap.read()
		# width = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
		# height = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
		enc.encode_rgb24(img)
		self.frame.set_value(enc)

if __name__ == "__main__":
	server_run((v4l2Device,))