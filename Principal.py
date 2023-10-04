import os
from flask import Flask, render_template,send_from_directory

app = Flask(__name__)

@app.route('/')
def raiz():
    return render_template("/raiz.html")

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory('uploads', filename)

@app.route("/iniciaSesion")
def Sesion():
    return render_template("/iniciaSesion.html")


if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port="8090") 
