
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def raiz():
    return render_template("/raiz.html")

@app.route("/iniciaSesion")
def Sesion():
    return render_template("/iniciaSesion.html")


if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port="8090") 
