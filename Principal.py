import os
from flask import Flask, redirect, render_template, request,send_from_directory
import mysql.connector
from usuarios import Usuarios

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="aplicacionWeb"
)

miCursor = conexion.cursor()
app = Flask(__name__)
misUsuarios = Usuarios(app,conexion,miCursor)

@app.route('/')
def raiz():
    return render_template("/raiz.html")

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory('uploads', filename)

@app.route("/registro")
def Sesion():
    return render_template("/registro.html")

@app.route("/registrarse", methods = ['POST'])
def registrarse():
    
    correo = request.form['correo']
    nombre = request.form['nombreUsuario']
    contraseña = request.form['contraseña']
    foto = request.files['fotoUsuario']
    usuario = [correo,nombre,contraseña,foto]
    
    if len(misUsuarios.buscar(usuario[0]))>0:
        return render_template("/registro.html",msg="correo de usuario no disponible")
    else:
        misUsuarios.registrar(usuario)
        return redirect("/")
    




if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port="8090") 
