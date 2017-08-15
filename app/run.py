from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from enum import Enum
import uuid
import myDataBase
import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
app.secret_key = str(uuid.uuid4())
dataBase = myDataBase.DataBase()

class Inhabitants(Enum):
  konrad = 0
  mateusz = 1
  szymon = 2

matrix = [[]]
matrix = [[0 for i in range(len(Inhabitants))] for i in range(len(Inhabitants))]

class Payment():
    def __init__(self):
        buyerName = ""
        product = ""
        price = 0
        participant = [2]
        date = 0

class User():
	def __init__(self, username):
		self.username = username

	def is_active(self):
		return True

	def is_anonymous(self):
		return self.is_anonymous

	def is_authenticated(self):
		return True

	def get_id(self):
		return self.username

@login_manager.user_loader
def load_user(username):
	return User(username)

def showMatrix(matrix):
  for i in range(len(Inhabitants)):
    for y in range(len(Inhabitants)):
      print(matrix[i][y], end='  ')
    print("\n")

@app.route("/")
def redirectToMain():
    return redirect(url_for("mainPage"))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", user1 = "Konrad", user2 = "Mateusz", user3 = "Szymon")

    if request.method == "POST":
        user = User(request.form.getlist("user"))
        login_user(user)
        return redirect(url_for("mainPage"))

@app.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


def printSpaces(howMany):
    result = ""
    for i in range(0, howMany):
        result += "&nbsp;"
    return result

def makeNiceHistory(dataBase):
    result = "Kupujący" + printSpaces(16) + "Produkt" + printSpaces(16) + "Cena" + printSpaces(30) +  "Data: <br>"
    for i in range(0, len(dataBase)):
        buyer = dataBase[i][0]
        product = str(dataBase[i][1])
        price = str(dataBase[i][2])
        date = str(dataBase[i][6])

        if dataBase[i][3] == 1:
            test1 = "K"
        if dataBase[i][4] == 1:
            test2 = "M"
        if dataBase[i][5] == 1:
            test3 = "S"
        result += (buyer + printSpaces(31 - len(buyer)*2) +
            product + printSpaces(31 - len(product)*2) +
            price[:-2] + "," + price[-2:] + "zł" +
            printSpaces(31 - len(price)*2) +
            date + printSpaces(31 - len(date))  + test1 + test2 +test3 + "<br>")
        print(dataBase[i])
        print(i)

    return result

'''
def makeNiceHistory(dataBase):
    result = ""
    for i in range(0, len(dataBase)):
        buyer = dataBase[i][0]
        product = str(dataBase[i][1])
        price = str(dataBase[i][2])
        date = str(dataBase[i][6])

        if dataBase[i][3] == 1:
            test1 = "K"
        if dataBase[i][4] == 1:
            test2 = "M"
        if dataBase[i][5] == 1:
            test3 = "S"

        result += (buyer + ": " + product + " " + price[:-2] + "," + price[-2:] + "zł" + test1 + test2 + test3 + date  +"<br>")
        print(dataBase[i])
        print(i)

    return result
'''

@app.route("/pieniondz", methods=["GET", "POST"])
@login_required
def mainPage():
    if request.method == "GET":
        return render_template("mainPage.html", history = makeNiceHistory(dataBase.showHistory()))

    if request.method == "POST":
        payment = Payment()
        product = request.form[u"produkt"]
        price = int((float(request.form[u"cenazl"]) * 100) + float(request.form[u"cenagr"]))
        konChkBox = bool(request.form.getlist("konChkBox"))
        matChkBox = bool(request.form.getlist("matChkBox"))
        szyChkBox = bool(request.form.getlist("szyChkBox"))
        time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        dataBase.createProduct(current_user.username[0], product, price, konChkBox, matChkBox, szyChkBox, time.strftime("%d %m %Y %H:%M:%S"))
        return redirect(url_for("mainPage"))

if __name__ == '__main__':
    app.run(host="192.168.1.103",port="5000")
