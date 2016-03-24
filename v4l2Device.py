from PyTango import AttrWriteType, EncodedAttribute, DevEncoded, DispLevel, IMAGE
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command, device_property
from PyTango.server import server_run
from numpy import ndarray

import cv2
import time

class v4l2Device(Device):
	__metaclass__ = DeviceMeta


	### Device properties -----------------------------------------------------

	cam_id = device_property(dtype=int, default_value=0)


	### API methods -----------------------------------------------------------

	def init_device(self):
		Device.init_device(self)
		self.cap = cv2.VideoCapture(self.cam_id)
		self.r = False


	### Attributes ------------------------------------------------------------

	# Attribute: frame --------------------------------------------------------

	frame = attribute(label="Image frame", dtype=DevEncoded, format="RawImage",
					  access=AttrWriteType.READ, fget="get_frame",
					  doc="Frame captured from camera")

	def get_frame(self):
		print "reading from cam: %s" % time.time()
		enc = EncodedAttribute()
		self.r, img = self.cap.read()
		print img
		enc.encode_rgb24(img)
		self.frame.set_value(enc)
		#return enc

	# Attribute: fps ----------------------------------------------------------

	# fps = attribute(label="Frames per second", dtype=int, unit="fps",
	# 				access=AttrWriteType.READ_WRITE, fget="get_fps", fset="set_fps",
	# 				doc="Camera frame rate")

	# def get_fps(self):
	# 	return self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
	# def set_fps(self, v):
	# 	self.cap.set(cv2.cv.CV_CAP_PROP_FPS, v)

	# Attribute: width --------------------------------------------------------

	width = attribute(label="Image width", dtype=int, format="%4d", unit="px",
					  access=AttrWriteType.READ_WRITE, fget="get_width", fset="set_width",
					  doc="Frame width")

	def get_width(self):
		return self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
	def set_width(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, v)

	# Attribute: height -------------------------------------------------------

	height = attribute(label="Image height", dtype=int, format="%4d", unit="px",
					   access=AttrWriteType.READ_WRITE, fget="get_height", fset="set_height",
					   doc="Frame height")

	def get_height(self):
		return self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
	def set_height(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, v)

	# Attribute: active -------------------------------------------------------

	active = attribute(label="Capture active", dtype=bool,
					   access=AttrWriteType.READ, fget="get_active",
					   doc="If capture process is active")

	def get_active(self):
		return self.cap.isOpened()

	# Attribute: lastr --------------------------------------------------------

	lastr = attribute(label="Last frame result", dtype=bool,
					   access=AttrWriteType.READ, fget="get_lastr",
					   doc="If last frame was captured correctly")

	def get_lastr(self):
		return self.r

	# Attribute: codec --------------------------------------------------------

	# codec = attribute(label="Codec", dtype=str,
	# 				    access=AttrWriteType.READ, fget="get_codec",
	# 				    doc="Codec code")

	# def get_codec(self):
	# 	return self.cap.get(cv2.cv.CV_CAP_PROP_FOURCC)

	# Attribute: mode ---------------------------------------------------------

	# mode = attribute(label="Capture mode", dtype=str,
	# 				   access=AttrWriteType.READ, fget="get_mode",
	# 				   doc="Backend capture mode")

	# def get_mode(self):
	# 	return self.cap.get(cv2.cv.CV_CAP_PROP_MODE)

	# Attribute: brightness ---------------------------------------------------

	brightness = attribute(label="Brightness", dtype=int, format="%3d", unit="%",
						   min_value=0, max_value=100,
						   access=AttrWriteType.READ_WRITE, fget="get_brightness", fset="set_brightness",
						   display_level=DispLevel.EXPERT,
						   doc="Camera brightness")

	def get_brightness(self):
		return int(round(self.cap.get(cv2.cv.CV_CAP_PROP_BRIGHTNESS)*100))
	def set_brightness(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, v/100.0)

	# Attribute: contrast -----------------------------------------------------

	contrast = attribute(label="Contrast", dtype=int, format="%3d", unit="%",
						 min_value=0, max_value=100,
						 access=AttrWriteType.READ_WRITE, fget="get_contrast", fset="set_contrast",
						 display_level=DispLevel.EXPERT,
						 doc="Camera contrast")

	def get_contrast(self):
		return int(round(self.cap.get(cv2.cv.CV_CAP_PROP_CONTRAST)*100))
	def set_contrast(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_CONTRAST, v/100.0)

	# Attribute: saturation ---------------------------------------------------

	saturation = attribute(label="Saturation", dtype=int, format="%3d", unit="%",
						   min_value=0, max_value=100,
						   access=AttrWriteType.READ_WRITE, fget="get_saturation", fset="set_saturation",
						   display_level=DispLevel.EXPERT,
						   doc="Camera saturation")

	def get_saturation(self):
		return int(round(self.cap.get(cv2.cv.CV_CAP_PROP_SATURATION)*100))
	def set_saturation(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_SATURATION, v/100.0)

	# Attribute: hue ----------------------------------------------------------

	hue = attribute(label="Hue", dtype=int, format="%3d", unit="%",
					min_value=0, max_value=100,
					access=AttrWriteType.READ_WRITE, fget="get_hue", fset="set_hue",
					display_level=DispLevel.EXPERT,
					doc="Camera hue")

	def get_hue(self):
		return int(round(self.cap.get(cv2.cv.CV_CAP_PROP_HUE)*100))
	def set_hue(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_HUE, v/100.0)

	# Attribute: gain ---------------------------------------------------------

	gain = attribute(label="Gain", dtype=int, format="%3d", unit="%",
					 min_value=0, max_value=100,
					 access=AttrWriteType.READ_WRITE, fget="get_gain", fset="set_gain",
					 display_level=DispLevel.EXPERT,
					 doc="Camera gain")

	def get_gain(self):
		return int(round(self.cap.get(cv2.cv.CV_CAP_PROP_GAIN)*100))
	def set_gain(self, v):
		self.cap.set(cv2.cv.CV_CAP_PROP_GAIN, v/100.0)

	# Attribute: exposure -----------------------------------------------------

	# exposure = attribute(label="Exposure", dtype=float,
	# 					 access=AttrWriteType.READ_WRITE, fget="get_exposure", fset="set_exposure",
	# 					 doc="Camera exposure")

	# def get_exposure(self):
	# 	return self.cap.get(cv2.cv.CV_CAP_PROP_EXPOSURE)
	# def set_exposure(self, v):
	# 	self.cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE, v)

	# Attribute: index --------------------------------------------------------

	# index = attribute(label="Frame index", dtype=int,
	# 				 access=AttrWriteType.READ, fget="get_index",
	# 				 doc="0-based frame count")

	# def get_index(self):
	# 	return self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)



if __name__ == "__main__":
	server_run((v4l2Device,))