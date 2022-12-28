import requests

payload = {"username": "Saif", "pass": "optp"}

try:
	r = requests.post("http://127.0.0.1:5656/auth", data = payload)
except:
	print("Network error")

else:
	print(r.text)