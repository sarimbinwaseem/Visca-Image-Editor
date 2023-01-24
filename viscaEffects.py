from PIL import ImageFilter, ImageEnhance
# from rsimageconvertor.convertor import Convertor

class ViscaEffects:
	def brightness(obj):
		intensityValue = obj[0]
		image = obj[1]
		bright = ImageEnhance.Brightness(image)
		intensity = float(intensityValue / 100) # 0.0 -> 1.0 -> 2.0
		# print(intensity)
		image = bright.enhance(intensity)
		return image

	def contrast(self):
		pass

	def blur(self):
		pass

	@staticmethod
	def enhance(image):
		eimage = image.filter(ImageFilter.DETAIL)
		return eimage

	# def reduceSize(self, image):
	# 	convertor = Convertor()
	# 	image = convertor.compressOne(image, 2000)
	# 	return image
