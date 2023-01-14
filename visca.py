from PyQt6 import QtWidgets, uic, QtCore, QtGui
import sys, requests, os
# from time import sleep


class Visca(QtWidgets.QMainWindow):
	'''Main Visca Image Editor'''
	def __init__(self):
		super(Visca, self).__init__()
		uic.loadUi(os.path.join("UI", "main.ui"), self)
		self.setWindowTitle("Visca Image Editor")


# if __name__ == "__main__":
# 	app = QtWidgets.QApplication(sys.argv)
# 	window = Visca()
# 	window.show()
# 	app.exec()