from lookups import PKMString
from structure import PersonalTable
import os

class Util():
	STRINGS = PKMString()
	PT = PersonalTable(bytearray(open(os.path.dirname(__file__) + '/../resources/bytes/personal_swsh','rb').read()))
	GenderSymbol = ['♂','♀','-']

	@staticmethod
	def translate(lang):
		Util.STRINGS = PKMString(lang)

	@staticmethod
	def convertImage(filename):
		import colorsys
		import numpy
		from PIL import Image
		image = Image.open(filename).convert('RGBA')
		h = image.height
		w = image.width
		pixels = numpy.array(image)
		hsv_array = numpy.empty(shape=(h, w, 5), dtype=float)
		for row in range(h):
			for column in range(w):
				rgb = pixels[row, column]
				hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
				hsv_array[row, column, 0] = hsv[0]
				hsv_array[row, column, 1] = hsv[1]
				hsv_array[row, column, 2] = hsv[2]
				hsv_array[row, column, 3] = rgb[3]
		return hsv_array

	@staticmethod
	def generatePallete(hsv_array, size = 32):
		# Crop the image
		import numpy
		h , w , d = hsv_array.shape
		if h > size:
			top = (h - size) // 2
			bottom = h - size - top
			if hsv_array[:top,:,3].any() or hsv_array[-bottom:,:,3].any():
				print("Image is too large")
			hsv_array = hsv_array[top:-bottom, : , :]
			h = size

		if w > size:
			left = (w - size) // 2
			right = w - size - left
			if hsv_array[:,:left,3].any() or hsv_array[:,-right:,3].any():
				print("Image is too large")
			hsv_array = hsv_array[:,left:-right, :]
			w = size

		# Find all colors
		Colorlist = numpy.empty((0,3),int)
		for r in range(h):
			if not hsv_array[r,:,3].any():
				continue
			for c in range(w):
				hsv = hsv_array[r,c]
				if hsv[3] == 0:
					continue
				HVB = Util.convert2HVB(hsv)
				idx = Util.findinlist(HVB,Colorlist)
				if idx < 0:
					Colorlist = numpy.append(Colorlist,[HVB], axis = 0)
					hsv_array[r,c,4] = len(Colorlist) - 1
				else:
					hsv_array[r,c,4] = idx
		return Colorlist, hsv_array

	@staticmethod
	def convert2HVB(hsv):
		import math
		H = min(29,math.floor(hsv[0] * 30))
		V = min(14,math.floor(hsv[1] * 15))
		B = min(14,math.floor(hsv[2] * 15))
		return [H,V,B]

	@staticmethod
	def findinlist(element,nplist):
		import numpy
		for ii in range(len(nplist)):
			if numpy.array_equal(nplist[ii],element):
				return ii
		return -1