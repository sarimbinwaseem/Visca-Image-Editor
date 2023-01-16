from PIL import ImageFilter

class ViscaEffects:
	def brightness(self):
		pass

	def contrast(self):
		pass

	def blur(self):
		pass

	def enhance(self, image):
		image = image.filter(ImageFilter.DETAIL)
		return image
