from PyQt6 import QtWidgets, uic, QtCore, QtGui
import sys, threading, random, requests, subprocess, os
from time import sleep


class Ui(QtWidgets.QDialog):
	'''UI functions of Visca Image Editor'''
	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi(os.path.join("UI", "login.ui"), self)
		self.setWindowTitle("Visca Login")
		self.loginButton.clicked.connect(self.login)

	def login(self):
		'''Login logic'''
		payload = {"username": "Saif", "pass": "optp"}
		try:
			r = requests.post("http://127.0.0.1:5656/auth", data = payload)
		except:
			print("Network error")
		else:
			response = r.text

		if response == "alwd":
			# from visca import Box
    		# box = Box()
    		# box.show()
    		# self.hide()

    	elif response == "acnf":
    		self.notif.setText("Incorrect username or password.")
    	else:
    		self.notif.setText("Some error ocurred.")

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Ui()
	window.show()
	app.exec()