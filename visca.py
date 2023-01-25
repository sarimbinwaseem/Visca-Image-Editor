from PyQt6 import QtWidgets, uic, QtCore, QtGui
import sys, os
# from time import sleep
# import cv2
from PIL import Image
from helpers import Calc
from viscaEffects import ViscaEffects
from save_thread_result import ThreadWithResult
# from rsimageconvertor.convertor import Convertor
from multiprocessing import Pool
from time import perf_counter

# class ResizeDialog(QtWidgets.QDialog):
#     def __init__(self, parent = None):
#         super().__init__(parent)

#         self.setWindowTitle("HELLO!")

#         QBtn = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel

#         self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)

#         self.layout = QtWidgets.QVBoxLayout()
#         message = QtWidgets.QLabel("Something happened, is that OK?")
#         self.layout.addWidget(message)
#         self.layout.addWidget(self.buttonBox)
#         self.setLayout(self.layout)

class ImageWidget(QtWidgets.QLabel):
	'''Display image holder'''
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setScaledContents(True)

class Visca(QtWidgets.QMainWindow):
	'''Main Visca Image Editor'''
	def __init__(self):
		super(Visca, self).__init__()
		ViscaEffects.__init__(self)

		uic.loadUi(os.path.join("UI", "main.ui"), self)
		self.setWindowTitle("Visca Image Editor")
		self.mainImage = ImageWidget()
		self.imageDisplayer.addWidget(self.mainImage)

		# Intensity of effect
		self.intensityValue = 100
		# Defines if image has been effected.
		self.changeFlag = False

		# Variables to store values for saving original image.
		self.enhanceValue = 0
		self.brightnessValue = 100
		self.blurValue = 0

		# Change it to True to save with slicing and multiprocessing
		# CAUTION: Will result in artifacted image.
		self.saveMultiThreaded = False

		# Connecting buttons to methods.
		self.actionOpen.triggered.connect(self.openSourceImage)
		self.actionSave.triggered.connect(self.saveResultImage)
		# self.actionReduce_Size.triggered.connect(self.reduceSize)

		self.brightnessSlider.valueChanged.connect(self.mainBrightness)
		self.enhanceButton.clicked.connect(self.mainEnhance)
		self.blurSlider.valueChanged.connect(self.mainBlur)

	def openSourceImage(self):
		'''Opening source image.'''
		self.sourceFilename = QtWidgets.QFileDialog.getOpenFileName(self,
			f'Open Image', '.', "Image Files (*.jpeg *.jpg *.png)")[0]
		# self.sourceImageData = cv2.imread(self.sourceFilename)
		self.sourceImageData = Image.open(self.sourceFilename)
		self.sourceSize = self.sourceImageData.size
		# Resizing source image to fit into display.
		self.sourceImageResized = self.resizeImage(self.sourceImageData)
		# Making Qt compatible image to display.
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		# self.mainImage.adjustSize()
		# self.imageDisplayer.adjustSize()
			# pass

	def pixmapFromPILImage(self, srcImgResized):
		'''Converting PIL image to Qt Image'''
		width, height = srcImgResized.size
		print(f"Width: {width}, Height: {height}")
		bytesPerLine = 3 * width
		# qImg = QtGui.QImage(srcImgResized.data, width, height,
		qImg = QtGui.QImage(srcImgResized.tobytes("raw", "RGB"), width, height,
			bytesPerLine, QtGui.QImage.Format.Format_RGB888)
		return QtGui.QPixmap(qImg)

	def resizeImage(self, imageData):
		'''Resizing image to fit into display.'''
		displayerSize = self.imageDisplayer.contentsRect()
		calcResize = Calc(displayerSize)
		sourceHeight = imageData.size[1]
		sourceWidth = imageData.size[0]
		# Calculating appropriate dimensions so image won't warp
		# (Cannot implement due to Qt layout limitaions)
		newSize = calcResize.getNewDimensions(sourceWidth, sourceHeight)
		# imageResized = cv2.resize(imageData, newSize, None, None, None, cv2.INTER_AREA)
		imageResized = imageData.resize(newSize)
		return imageResized

	def saveResultImage(self):
		'''Saving Source image.'''
		try:
			ext = os.path.basename(self.sourceFilename).split('.')[-1]
			if self.saveMultiThreaded:
				print("Slicing Image...")
				pieceThread = ThreadWithResult(target = Calc.sliceImage,
				args = (self.sourceImageData, 6, 6))
				pieceThread.start()
				pieceThread.join()

				pieces = pieceThread.result

			print("Applying Effects...")
			if self.brightnessValue != 100:
				print("Brightness...")
				if self.saveMultiThreaded:
					newpieces = [[self.brightnessValue, piece] for piece in pieces]
					with Pool(processes = 4) as pool:
						m = pool.map_async(ViscaEffects.brightness, newpieces)
						pieces = m.get()
				else:
					temp = ThreadWithResult(target = ViscaEffects.brightness,
						args = ([self.brightnessValue, self.sourceImageData],))
					temp.start()
					temp.join()
					self.sourceImageData = temp.result


				# self.sourceImageData = ViscaEffects.brightness([self.brightnessValue,
				# 	self.sourceImageData])


			if self.blurValue != 0:
				print("Blur...")
				print(self.blurValue)
				if self.saveMultiThreaded:
					newpieces = [[self.blurValue, piece] for piece in pieces]
					with Pool(processes = 4) as pool:
						m = pool.map_async(ViscaEffects.blur, newpieces)
						pieces = m.get()
				else:
					temp = ThreadWithResult(target = ViscaEffects.blur,
						args = ([self.blurValue, self.sourceImageData],))
					temp.start()
					temp.join()
					self.sourceImageData = temp.result

				# self.sourceImageData = ViscaEffects.blur([self.blurValue,
				# 	self.sourceImageData])

			if self.enhanceValue != 0:
				print("Enhance...")
				if self.saveMultiThreaded:
					for _ in range(self.enhanceIntensity):
						with Pool(processes = 4) as pool:
							m = pool.map_async(ViscaEffects.enhance, pieces)
							pieces = m.get()
				else:
					temp = ThreadWithResult(target = ViscaEffects.enhance,
						args = (self.sourceImageData,))
					temp.start()
					temp.join()
					self.sourceImageData = temp.result

				# self.sourceImageData = ViscaEffects.enhance([self.enhanceValue,
				# 	self.sourceImageData])

			# size = self.sourceImageData.size
			if self.saveMultiThreaded:
				print([p.size for p in pieces])
				print("Rebuilding..")
				self.sourceImageData = Calc.rebuildImage(self.sourceSize, pieces)
			print("Saving...")
			
			self.sourceImageData.save(self.sourceFilename.replace(f".{ext}",
			f"out.{ext}"))
			self.sourceImageData.show()
			print("Saved..")
		except Exception as e:
			print(e)

	def mainBrightness(self):
		'''Brightness Effect Call'''
		if self.changeFlag is False:
			self.imgTemp = self.sourceImageResized
		else:
			pass

		# Setting intensity value to slider's value
		self.intensityValue = self.brightnessSlider.value()
		self.brightnessValue = self.intensityValue
		self.intensityLabel.setText(str(self.intensityValue))
		start = perf_counter()

		# Making pieces of image
		# print("Making Pieces..")
		pieceThread = ThreadWithResult(target = Calc.sliceImage,
			args = (self.imgTemp, 6, 6))
		pieceThread.start()
		pieceThread.join()

		pieces = pieceThread.result

		# Making new list with intensity value for each piece.
		newpieces = [[self.intensityValue, piece] for piece in pieces]
		# print(pieces)

		# Applying effect to each piece with 4 multiprocessing processes.
		effectedPieces = []
		with Pool(processes = 4) as pool:
			m = pool.map_async(ViscaEffects.brightness, newpieces)
			# Getting the result back
			effectedPieces.extend(m.get())

		print(len(effectedPieces))
		size = self.imgTemp.size
		# Rebuilding Image from pieces.
		self.sourceImageResized = Calc.rebuildImage(size, effectedPieces)

		# temp = ThreadWithResult(target = ViscaEffects.brightness, 
		# 	args = ([self.intensityValue, self.imgTemp],))
		# temp.start()
		# temp.join()
		# self.sourceImageResized = temp.result

		# Displaying the effected image.
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		self.changeFlag = True
		print("Time taken:", perf_counter() - start)

	def mainBlur(self):
		'''Blur Effect Call'''
		if self.changeFlag is False:
			self.imgTemp = self.sourceImageResized
		else:
			pass

		self.intensityValue = self.blurSlider.value()
		self.blurValue = self.intensityValue
		self.intensityLabel.setText(str(self.intensityValue))
		start = perf_counter()
		# Making pieces of image
		print("Making Pieces..")
		pieceThread = ThreadWithResult(target = Calc.sliceImage,
			args = (self.imgTemp, 6, 6))
		pieceThread.start()
		pieceThread.join()

		pieces = pieceThread.result
		newpieces = [[self.intensityValue, piece] for piece in pieces]
		# print(pieces)
		print("Applying Effect...")
		effectedPieces = []
		with Pool(processes = 4) as pool:
			m = pool.map_async(ViscaEffects.blur, newpieces)
			effectedPieces.extend(m.get())

		print(len(effectedPieces))

		# # print("Merging Picture...")
		size = self.sourceImageResized.size

		# Rebuilding Image.
		self.sourceImageResized = Calc.rebuildImage(size, effectedPieces)
	
			# temp = ThreadWithResult(target = ViscaEffects.enhance, 
			# 	args = ([self.intensityValue, self.sourceImageResized],))
			# temp.start()
			# temp.join()
			# self.sourceImageResized = temp.result
		# Displaying the effected image.
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		self.changeFlag = True
		print("Blur took:", perf_counter() - start)

	def mainEnhance(self):
		'''Enhance Effect Call'''
		start = perf_counter()
		# Making pieces of image
		print("Making Pieces..")
		pieceThread = ThreadWithResult(target = Calc.sliceImage,
			args = (self.sourceImageResized, 6, 6))
		pieceThread.start()
		pieceThread.join()

		pieces = pieceThread.result
		# print(pieces)
		print("Applying Effect...")
		effectedPieces = []
		with Pool(processes = 4) as pool:
			m = pool.map_async(ViscaEffects.enhance, pieces)
			effectedPieces.extend(m.get())

		print(len(effectedPieces))

		print("Merging Picture...")
		size = self.sourceImageResized.size

		# Rebuilding Image.
		self.sourceImageResized = Calc.rebuildImage(size, effectedPieces)
	
			# temp = ThreadWithResult(target = ViscaEffects.enhance, 
			# 	args = ([self.intensityValue, self.sourceImageResized],))
			# temp.start()
			# temp.join()
			# self.sourceImageResized = temp.result
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		self.changeFlag = True
		self.enhanceValue += 1
		print("Enhance took:", perf_counter() - start)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Visca()
	window.show()
	app.exec()