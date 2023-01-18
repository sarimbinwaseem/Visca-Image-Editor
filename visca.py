from PyQt6 import QtWidgets, uic, QtCore, QtGui
import sys, requests, os
# from time import sleep
# import cv2
from PIL import Image
from helpers import Calc
from viscaEffects import ViscaEffects
from save_thread_result import ThreadWithResult
from rsimageconvertor.convertor import Convertor


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
		
		self.intensityValue = 1
		self.changeFlag = False

		self.actionOpen.triggered.connect(self.openSourceImage)
		self.actionSave.triggered.connect(self.saveResultImage)
		self.actionReduce_Size.triggered.connect(self.reduceSize)
		self.enhanceBtn.clicked.connect(self.enhance)
		self.brightnessBtn.clicked.connect(self.brightness)
		self.intensitySlider.valueChanged.connect(self.intensity)

	def intensity(self):
		self.intensityValue = self.intensitySlider.value()
		self.intensityLabel.setText(str(self.intensityValue))
		print(self.intensityValue)

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
			bytesPerLine, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
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

		temp = ThreadWithResult(target = ViscaEffects.brightness, 
			args = (self, self.imgTemp,))
		temp.start()
		temp.join()
		self.sourceImageResized = temp.result
		self.mainImage.setPixmap(self.pixmapFromPILImage(self.sourceImageResized))
		self.changeFlag = True

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
		temp = ThreadWithResult(target = ViscaEffects.reduceSize, 
			args = (self, self.source_filename,))
		temp.start()
		temp.join()
		self.source_image_data = temp.result


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Visca()
	window.show()
	app.exec()