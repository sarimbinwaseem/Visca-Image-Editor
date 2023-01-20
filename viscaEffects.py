from PIL import ImageFilter, ImageEnhance
from rsimageconvertor.convertor import Convertor

class ViscaEffects:
	def brightness(obj):
		intensityValue = obj[0]
		image = obj[1]
		bright = ImageEnhance.Brightness(image)
		intensity = float(intensityValue / 100) # 0.0 -> 1 -> 2
		# print(intensity)
		image = bright.enhance(intensity)
		return image

	def contrast(self):
		pass

	def blur(self):
		pass

	def enhance(self, image):
		image = image.filter(ImageFilter.DETAIL)
		return image

	def reduceSize(self, image):
		convertor = Convertor()
		image = convertor.compressOne(image, 2000)
		return image
