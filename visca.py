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

class ResizeDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class ImageWidget(QtWidgets.QLabel):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setScaledContents(True)
	# def hasHeightForWidth(self):
	# 	return self.pixmap() is not None

	# def heightForWidth(self, w):
	# 	if self.pixmap():
	# 		try:
	# 			return int(w * (self.pixmap().height() / self.pixmap().width()))
	# 		except ZeroDivisionError:
	# 			return 0

class Visca(QtWidgets.QMainWindow):
	'''Main Visca Image Editor'''
	def __init__(self):
		super(Visca, self).__init__()
		ViscaEffects.__init__(self)

		uic.loadUi(os.path.join("UI", "main.ui"), self)
		self.setWindowTitle("Visca Image Editor")
		self.mainImage = ImageWidget()
		self.imageDisplayer.addWidget(self.mainImage)

		self.intensityValue = 100
		self.changeFlag = False

		self.enhanceValue = 0
		self.brightnessValue = 100
		self.blurValue = 0

		self.saveMultiThreaded = False

		self.actionOpen.triggered.connect(self.openSourceImage)
		self.actionSave.triggered.connect(self.saveResultImage)
		# self.actionReduce_Size.triggered.connect(self.reduceSize)

		self.brightnessSlider.valueChanged.connect(self.mainBrightness)
		self.enhanceButton.clicked.connect(self.mainEnhance)
		self.blurSlider.valueChanged.connect(self.mainBlur)
		# self.intensitySlider.valueChanged.connect(self.intensity)

	# def intensity(self):
	# 	self.intensityValue = self.intensitySlider.value()
	# 	self.intensityLabel.setText(str(self.intensityValue))
	# 	print(self.intensityValue)

	def openSourceImage(self):
		self.sourceFilename = QtWidgets.QFileDialog.getOpenFileName(self,
			f'Open Image', '.', "Image Files (*.jpeg *.jpg *.png)")[0]
		# self.sourceImageData = cv2.imread(self.sourceFilename)
		self.sourceImageData = Image.open(self.sourceFilename)
		self.sourceSize = self.sourceImageData.size
		self.sourceImageResized = self.resizeImage(self.sourceImageData)
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		# self.mainImage.adjustSize()
		# self.imageDisplayer.adjustSize()
			# pass

	def pixmapFromPILImage(self, srcImgResized):

		width, height = srcImgResized.size
		print(f"Width: {width}, Height: {height}")
		bytesPerLine = 3 * width
		# qImg = QtGui.QImage(srcImgResized.data, width, height,
		qImg = QtGui.QImage(srcImgResized.tobytes("raw", "RGB"), width, height,
			bytesPerLine, QtGui.QImage.Format.Format_RGB888)
		return QtGui.QPixmap(qImg)

	def resizeImage(self, imageData):
		displayerSize = self.imageDisplayer.contentsRect()
		calcResize = Calc(displayerSize)
		sourceHeight = imageData.size[1]
		sourceWidth = imageData.size[0]
		newSize = calcResize.getNewDimensions(sourceWidth, sourceHeight)
		# imageResized = cv2.resize(imageData, newSize, None, None, None, cv2.INTER_AREA)
		imageResized = imageData.resize(newSize)
		return imageResized

	def saveResultImage(self):
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
		if self.changeFlag is False:
			self.imgTemp = self.sourceImageResized
		else:
			pass

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

		newpieces = [[self.intensityValue, piece] for piece in pieces]
		# # print(pieces)
		effectedPieces = []
		with Pool(processes = 4) as pool:
			m = pool.map_async(ViscaEffects.brightness, newpieces)
			effectedPieces.extend(m.get())

		print(len(effectedPieces))
		size = self.imgTemp.size
		self.sourceImageResized = Calc.rebuildImage(size, effectedPieces)

		temp = ThreadWithResult(target = ViscaEffects.brightness, 
			args = ([self.intensityValue, self.imgTemp],))
		temp.start()
		temp.join()
		self.sourceImageResized = temp.result
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		self.changeFlag = True
		print("Time taken:", perf_counter() - start)

	def contrast(self):
		pass

	def mainBlur(self):
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
		# print("Applying Effect...")
		effectedPieces = []
		with Pool(processes = 4) as pool:
			m = pool.map_async(ViscaEffects.blur, newpieces)
			effectedPieces.extend(m.get())

		print(len(effectedPieces))

		# # print("Merging Picture...")
		size = self.sourceImageResized.size

		self.sourceImageResized = Calc.rebuildImage(size, effectedPieces)
	
			# temp = ThreadWithResult(target = ViscaEffects.enhance, 
			# 	args = ([self.intensityValue, self.sourceImageResized],))
			# temp.start()
			# temp.join()
			# self.sourceImageResized = temp.result
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		self.changeFlag = True
		print("Blur took:", perf_counter() - start)

	def mainEnhance(self):

		start = perf_counter()
		# Making pieces of image
		print("Making Pieces..")
		pieceThread = ThreadWithResult(target = Calc.sliceImage,
			args = (self.sourceImageResized, 6, 6))
		pieceThread.start()
		pieceThread.join()

		pieces = pieceThread.result
		# print(pieces)
		# print("Applying Effect...")
		effectedPieces = []
		with Pool(processes = 4) as pool:
			m = pool.map_async(ViscaEffects.enhance, pieces)
			effectedPieces.extend(m.get())

		print(len(effectedPieces))

		# # print("Merging Picture...")
		size = self.sourceImageResized.size

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