import os
from flask import Flask, redirect, render_template, request,send_from_directory,session
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

CARPETAUP = os.path.join('uploads')
app.config['CARPETAUP'] = CARPETAUP


@app.route('/')
def raiz():
    if session.get('loginOk'):
        return render_template("/raiz.html",usuario=Sesion.get(""))
    else:
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

@app.route('/loguin')
def login():
    return render_template("/loguin.html")

@app.route('/loguear',methods=['POST'])
def loguear():
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    resultado = misUsuarios.loguear(correo,contraseña)
    if len(resultado)>0:
        session['loginOk'] = True
        session['nombreUsuario'] = resultado[0][0]
        session['foto'] = resultado[0][1]
        return render_template("/raiz.html",nom=resultado[0][0],fot=resultado[0][1])
    else:
        return render_template("/login.html",msg="Credenciales incorrectas",msg2=resultado)
    
  



if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port="8090") 
