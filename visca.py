from PyQt6 import QtWidgets, uic, QtCore, QtGui
import sys, requests, os
# from time import sleep
import cv2
from PIL import Image
from helpers import Calc



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
		uic.loadUi(os.path.join("UI", "main.ui"), self)
		self.setWindowTitle("Visca Image Editor")
		self.mainImage = ImageWidget()
		self.imageDisplayer.addWidget(self.mainImage)
		self.actionOpen.triggered.connect(self.openSourceImage)
		self.actionSave.triggered.connect(self.saveResultImage)

	def openSourceImage(self):
		self.source_filename = QtWidgets.QFileDialog.getOpenFileName(self,
			f'Open Image', '.', "Image Files (*.jpeg *.jpg *.png)")[0]
		# self.source_image_data = cv2.imread(self.source_filename)
		self.source_image_data = Image.open(self.source_filename)
		source_image_resized = self.resize_image(self.source_image_data)
		self.mainImage.setPixmap(self.pixmap_from_cv_image(source_image_resized))
		# pass

	def pixmap_from_cv_image(self, cvImage):
		# height, width, _ = cvImage.shape
		width, height = cvImage.size
		print(f"Width: {width}, Height: {height}")
		bytesPerLine = 3 * width
		# qImg = QtGui.QImage(cvImage.data, width, height,
		qImg = QtGui.QImage(cvImage.tobytes("raw", "RGB"), width, height,
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
		pass

	# def choose_source_image(self):


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Visca()
	window.show()
	app.exec()