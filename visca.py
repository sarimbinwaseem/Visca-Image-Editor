from PyQt6 import QtWidgets, uic, QtCore, QtGui
import sys, requests, os
# from time import sleep
# import cv2
from PIL import Image
from helpers import Calc
from viscaEffects import ViscaEffects
from save_thread_result import ThreadWithResult
# from rsimageconvertor.convertor import Convertor
from multiprocessing import Pool
from time import perf_counter

class CustomDialog(QtWidgets.QDialog):
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

		self.actionOpen.triggered.connect(self.openSourceImage)
		self.actionSave.triggered.connect(self.saveResultImage)
		# self.actionReduce_Size.triggered.connect(self.reduceSize)

		self.brightnessSlider.valueChanged.connect(self.brightness)
		self.enhanceSlider.valueChanged.connect(self.enhance)
		# self.intensitySlider.valueChanged.connect(self.intensity)
		# self.intensitySlider.valueChanged.connect(self.intensity)

	# def intensity(self):
	# 	self.intensityValue = self.intensitySlider.value()
	# 	self.intensityLabel.setText(str(self.intensityValue))
	# 	print(self.intensityValue)

	def openSourceImage(self):
		self.source_filename = QtWidgets.QFileDialog.getOpenFileName(self,
			f'Open Image', '.', "Image Files (*.jpeg *.jpg *.png)")[0]
		# self.source_image_data = cv2.imread(self.source_filename)
		self.source_image_data = Image.open(self.source_filename)
		self.sourceImageResized = self.resize_image(self.source_image_data)
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

	def resize_image(self, imageData):
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
			ext = os.path.basename(self.source_filename).split('.')[-1]
			self.source_image_data.save(self.source_filename.replace(f".{ext}",
			f"out.{ext}"))
			print("Saved..")
		except Exception as e:
			print(e)

	def brightness(self):
		if self.changeFlag is False:
			self.imgTemp = self.sourceImageResized
		else:
			pass

		self.intensityValue = self.brightnessSlider.value()
		self.intensityLabel.setText(str(self.intensityValue))
		start = perf_counter()
		# Making pieces of image
		# print("Making Pieces..")
		# pieceThread = ThreadWithResult(target = Calc.sliceImage,
		# 	args = (self.imgTemp, 6, 6))
		# pieceThread.start()
		# pieceThread.join()

		# pieces = pieceThread.result

		# newpieces = [[self.intensityValue, piece] for piece in pieces]
		# # print(pieces)
		# effectedPieces = []
		# with Pool(processes = 4) as pool:
		# 	m = pool.map_async(ViscaEffects.brightness, newpieces)
		# 	effectedPieces.extend(m.get())

		# print(len(effectedPieces))
		# size = self.imgTemp.size
		# self.sourceImageResized = Image.new("RGB", size)
		# x = 0
		# xOffset = self.imgTemp.width // 6
		# y = 0
		# yOffset = self.imgTemp.height // 6
		# yy = 0
		# for i in range(6):
		# 	# print("I:", i)
		# 	for j in range(6):
		# 		# print("J:", j)
		# 		self.sourceImageResized.paste(effectedPieces[yy + j],
		# 			(x, y))
		# 		x += xOffset
		# 	yy += j + 1
		# 	x = 0
		# 	y += yOffset

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

	def blur(self):
		from scipy import misc,ndimage
    
		face = misc.face()  
		blurred_face = ndimage.gaussian_filter(face, sigma=3)  
		very_blurred = ndimage.gaussian_filter(face, sigma=5)
   
	#Results  
		plt.imshow()

	def enhance(self):

		# temp = ThreadWithResult(target = ViscaEffects.enhance, 
		# 	args = (self, self.sourceImageResized,))
		# temp.start()
		# temp.join()
		# self.sourceImageResized = temp.result
		# self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))

		# temp = ThreadWithResult(target = ViscaEffects.enhance, 
		# 	args = (self, self.source_image_data,))
		# temp.start()
		# temp.join()

		# self.source_image_data = temp.result

		# def reduceSize(self):
		#	temp = ThreadWithResult(target = ViscaEffects.reduceSize, 
		# 		args = (self, self.source_filename,))
		# 	temp.start()
		# 	temp.join()
		# 	self.source_image_data = temp.result
		if self.changeFlag is False:
			self.imgTemp = self.sourceImageResized
		
		self.intensityValue = self.enhanceSlider.value()
		self.intensityLabel.setText(str(self.intensityValue))
		start = perf_counter()
		# Making pieces of image
		print("Making Pieces..")
		pieceThread = ThreadWithResult(target = Calc.sliceImage,
			args = (self.imgTemp, 6, 6))
		pieceThread.start()
		pieceThread.join()

		pieces = pieceThread.result

		# newpieces = [[self.intensityValue, piece] for piece in pieces]
		# print(pieces)
		effectedPieces = []
		with Pool(processes = 4) as pool:
			m = pool.map_async(ViscaEffects.enhance, pieces)
			effectedPieces.extend(m.get())

		print(len(effectedPieces))
		size = self.imgTemp.size
		self.sourceImageResized = Image.new("RGB", size)
		x = 0
		xOffset = self.imgTemp.width // 6
		y = 0
		yOffset = self.imgTemp.height // 6
		yy = 0
		for i in range(6):
			# print("I:", i)
			for j in range(6):
				# print("J:", j)
				self.sourceImageResized.paste(effectedPieces[yy + j],
					(x, y))
				x += xOffset
			yy += j + 1
			x = 0
			y += yOffset
	
			# temp = ThreadWithResult(target = ViscaEffects.enhance, 
			# 	args = ([self.intensityValue, self.imgTemp],))
			# temp.start()
			# temp.join()
			# self.sourceImageResized = temp.result
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		self.changeFlag = True
		print("Time taken:", perf_counter() - start)

<<<<<<< HEAD
	def contrast(self):
		pass

	def blur(self):
		pass

	def enhance(self):

		temp = ThreadWithResult(target = ViscaEffects.enhance, 
			args = (self, self.sourceImageResized,))
		temp.start()
		temp.join()
		self.sourceImageResized = temp.result
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))

		temp = ThreadWithResult(target = ViscaEffects.enhance, 
			args = (self, self.source_image_data,))
		temp.start()
		temp.join()

		self.source_image_data = temp.result

	def reduceSize(self):
		dlg = CustomDialog(self)
		dlg.exec()
		# temp = ThreadWithResult(target = ViscaEffects.reduceSize, 
		# 	args = (self, self.source_filename,))
		# temp.start()
		# temp.join()
		# self.source_image_data = temp.result


=======
>>>>>>> 353ccd8a69c094782954626f216f6170b4a43a4d
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Visca()
	window.show()
	app.exec()