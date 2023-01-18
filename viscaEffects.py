from PIL import ImageFilter, ImageEnhance
from rsimageconvertor.convertor import Convertor

class ViscaEffects:
	def brightness(self, image):
		bright = ImageEnhance.Brightness(image)
		intensity = float(self.intensityValue / 100)
		print(intensity)
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
