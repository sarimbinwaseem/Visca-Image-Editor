from run import db, User

username = input("Enter Username: ")
password = input("Input Password:" )

db.session.add(User(username = username, password = password))
db.session.commit()
