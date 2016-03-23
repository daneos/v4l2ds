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
					  access=AttrWriteType.READ, fget="get_frame",
					  doc="Frame captured from camera")

	fps = attribute(label="Frames per second", dtype=int, format="%d", unit="fps",
					access=AttrWriteType.READ_WRITE, fget="get_fps", fset="set_fps",
					doc="Camera frame rate")

	width = attribute(label="Image width", dtype=int, format="%d", unit="px",
					  access=AttrWriteType.READ_WRITE, fget="get_width", fset="set_width",
					  doc="Frame width")

	height = attribute(label="Image height", dtype=int, format="%d", unit="px",
					   access=AttrWriteType.READ_WRITE, fget="get_height", fset="set_height",
					   doc="Frame height")

	def init_device(self):
		Device.init_device(self)
		self.cap = cv2.VideoCapture(self.cam_id)

	def get_frame(self):
		print "reading from cam: %s" % time.time()
		enc = EncodedAttribute()
		r, img = self.cap.read()
		print img
		enc.encode_rgb24(img)
		self.frame.set_value(enc)

	def get_fps(self):
		self.fps.set_value(self.cap.get(cv2.cv.CV_CAP_PROP_FPS))

	def set_fps(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_FPS, v)

	def get_width(self):
		self.width.set_value(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))

	def set_width(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, v)

	def get_height(self):
		self.height.set_value(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

	def set_height(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, v)

if __name__ == "__main__":
	server_run((v4l2Device,))