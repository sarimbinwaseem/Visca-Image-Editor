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

	@staticmethod
	def sliceImage(im, xPieces, yPieces):
		pieces = []
		imgwidth, imgheight = im.size
		height = imgheight // yPieces
		width = imgwidth // xPieces
		for i in range(0, yPieces):
			for j in range(0, xPieces):
				box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
				cropped = im.crop(box)
				try:
				# cropped.save(filename + "-" + str(i) + "-" + str(j) + file_extension)
					pieces.append(cropped)
				except:
					print("Cannot append to pieces list..")
		return pieces


# r = Calc()
# print(r.adjHeight(1920, 1080, 1280))
# print(r.adjWidth(1920, 1080, 720))
