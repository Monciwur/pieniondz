from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def mainPage():
    if request.method == "GET":
        return render_template("mainPage.html")
    if request.method == "POST":
        product = request.form[u"produkt"]
        zlotyAndGrosze = int((float(request.form[u"cenazl"]) * 100) + float(request.form[u"cenagr"]))
        konChkBox = bool(request.form.getlist("konChkBox"))
        matChkBox = bool(request.form.getlist("matChkBox"))
        szyChkBox = bool(request.form.getlist("szyChkBox"))
        return redirect(url_for("mainPage"))

if __name__ == '__main__':
    app.run()
