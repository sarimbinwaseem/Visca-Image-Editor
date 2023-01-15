class Calc:
	def __init__(self, imageSize):
		self.displayWidth = imageSize.width()
		self.displayHeight = imageSize.height()

		print(f"Display Dimension: {self.displayWidth}, {self.displayHeight}")

	def getNewDimensions(self, sourceWidth, sourceHeight):
		if sourceWidth >= self.displayWidth:
			newSourceWidth = sourceWidth - (sourceWidth - self.displayWidth)
			newSourceHeight = self.adjHeight(sourceWidth, sourceHeight, newSourceWidth)
			
			if newSourceHeight > self.displayHeight:
				newSourceHeight = newSourceHeight - (newSourceHeight - self.displayHeight)
				newSourceWidth = self.adjWidth(sourceWidth, sourceHeight, newSourceHeight)

		elif sourceHeight >= self.displayHeight:
			newSourceHeight = sourceHeight - (sourceHeight - self.displayHeight)
			newSourceWidth = self.adjWidth(sourceWidth, sourceHeight, newSourceHeight)

			if newSourceWidth > self.displayWidth:
				newSourceWidth = newSourceWidth - (newSourceWidth - self.displayWidth)
				newSourceWidth = self.adjWidth(sourceWidth, sourceHeight, newSourceWidth)
		else:
			newSourceWidth = sourceWidth
			newSourceHeight = sourceHeight
		print(int(newSourceWidth), int(newSourceHeight))
		return (int(newSourceWidth), int(newSourceHeight))

	def adjHeight(self, sourceWidth, sourceHeight, width):
		return (sourceHeight * width) / sourceWidth

	def adjWidth(self, sourceWidth, sourceHeight, height):
		return (height * sourceWidth) / sourceHeight


# r = Calc()
# print(r.adjHeight(1920, 1080, 1280))
# print(r.adjWidth(1920, 1080, 720))
