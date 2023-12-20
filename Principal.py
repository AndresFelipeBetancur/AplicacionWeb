from datetime import timedelta
import os
from flask import Flask, redirect, render_template, request,send_from_directory,session
import mysql.connector
from usuarios import Usuarios
from random import randint
from videos import Videos


conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="aplicacionWeb"
)

miCursor = conexion.cursor()
app = Flask(__name__)
misUsuarios = Usuarios(app,conexion,miCursor)
misVideos = Videos(app,conexion,miCursor)

app.secret_key=str(randint(100000,999999)) 
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=40)

CARPETAUP = os.path.join('uploads')
app.config['CARPETAUP'] = CARPETAUP


@app.route('/')
def raiz():
    if session.get('loginOk'):
        correo = session.get('correo')
        nombre_usuario = session.get('nombreUsuario')
        foto_usuario = misUsuarios.foto(correo) 
        videos = misVideos.buscar()
        return render_template("/raiz.html", nombre=nombre_usuario, foto=foto_usuario, res=videos)
    else:
        videos = misVideos.buscar()
        return render_template("/raiz.html",res=videos)



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
    usuario = misUsuarios.loguear(correo,contraseña)
    if len(usuario)>0:
        session['loginOk'] = True
        session['nombreUsuario'] = usuario[0][0]
        session['correo'] = correo
        foto = misUsuarios.foto(correo)
        session['fotoUsuario'] = foto
        resultado = misVideos.buscar()
        return render_template("/raiz.html",bienvenida=f"¡Bienvenido {usuario[0][0]}!",fot=foto,res=resultado)
    else:
        return render_template("/login.html",msg="Credenciales incorrectas")

@app.route("/Regresar")
def Regresar():
    if session.get('loginOk'):
        nombre_usuario = session.get("nombreUsuario")
        correo = session.get("correo")
        foto_usuario = misUsuarios.foto(correo)  
        videos = misVideos.buscar()
        return render_template("/raiz.html", bienvenida=f"¡Bienvenido {nombre_usuario}!",fot=foto_usuario,res=videos)
    else:
        return redirect("/")

@app.route("/cerrarSesion")
def cierreSesion():
    session.clear()
    return redirect("/")

@app.route("/subirVideo")
def subirVideo():
    if session.get('loginOk'):
        correo = session.get("correo")
        foto_usuario = misUsuarios.foto(correo)  # Asume que misUsuarios tiene un método foto
        return render_template("/subirVideo.html", foto=foto_usuario)
    else:
        return redirect("/")

@app.route("/subir", methods = ['POST'])
def subir():
    correo = session.get("correo")
    nombre_usuario = session.get('nombreUsuario')
    foto_usuario = misUsuarios.foto(session.get("correo"))
    nombre = request.form["nombreVideo"]
    video = request.files["video"]
    portada = request.files["portada"]
    archivo = [correo,nombre_usuario,nombre,video,portada,foto_usuario]
    misVideos.subir(archivo)
    nombre_usuario = session.get('nombreUsuario')
    foto_usuario = misUsuarios.foto(correo) 
    return redirect("/",nombre=nombre_usuario, foto=foto_usuario)

@app.route('/ver_video/<video_id>/<nombre_video>')
def ver_video(video_id,nombre_video):
    return render_template('/verVideo.html', video_id=video_id,nombre_video=nombre_video)


@app.route("/buscar", methods = ['POST'])
def buscar():
    vdBuscar = request.form["buscar"]
    resultado = misVideos.encontrar(vdBuscar)
    return render_template("/Buscar.html",res=resultado)


if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port="8090") 
