from datetime import timedelta
import os
from flask import Flask, redirect, render_template, request,send_from_directory,session,url_for
import mysql.connector
from usuarios import Usuarios
from random import randint
from videos import Videos
import smtplib
from email.message import EmailMessage

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

#CONFIGURACION PARA ENVIAR EMAILS
remitente = "tpscab2023@hotmail.com"
smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
smtp.starttls()
smtp.login(remitente, "CAB+12345+tps")

@app.route('/')
def raiz():
    if session.get('loginOk'):
        correo = session.get('correo')
        nombre_usuario = session.get('nombreUsuario')
        foto_usuario = misUsuarios.foto(correo) 
        videos = misVideos.buscar()
        return render_template("/raiz.html",correo=correo,nombre_usuario=nombre_usuario, foto=foto_usuario, res=videos)
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
        nombre_usuario = session['nombreUsuario']
        session['correo'] = correo
        foto = misUsuarios.foto(correo)
        session['fotoUsuario'] = foto
        resultado = misVideos.buscar()
        return render_template("/raiz.html",correo=correo,nombre_usuario=nombre_usuario,bienvenida=f"¡Bienvenido {usuario[0][0]}!",fot=foto,res=resultado)
    else:
        return render_template("/login.html",msg="Credenciales incorrectas")

@app.route("/Regresar")
def Regresar():
    if session.get('loginOk'):
        nombre_usuario = session.get("nombreUsuario")
        correo = session.get("correo")
        foto_usuario = misUsuarios.foto(correo)  
        videos = misVideos.buscar()
        return render_template("/raiz.html",correo,bienvenida=f"¡Bienvenido {nombre_usuario}!",fot=foto_usuario,res=videos)
    else:
        return redirect("/")

@app.route("/cerrarSesion")
def cierreSesion():
    session.clear()
    return redirect("/")

@app.route("/verPerfil/<nom_usuario>/<fotoU>")
def verPerfil(nom_usuario,fotoU):
    if session.get('loginOk'):
        correo = session['correo']
        if correo:
            print(correo)
        return render_template("/verPerfil.html",correoU=correo,nom=nom_usuario,foto=fotoU)
    else:
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
    videos = misVideos.buscarC(video_id)
    
    infoVideo = misVideos.infoVideo(video_id)
    video = {
        "id": video_id,
        "nombre": nombre_video,
        "usuario": infoVideo[0][0],
        "fotoU": infoVideo[0][1],
        "fechaSubida": infoVideo[0][2]    
    }
    
    return render_template('/verVideo.html',video=video,contenido=videos)


@app.route("/buscar", methods = ['POST'])
def buscar():
    vdBuscar = request.form["buscar"]
    resultado = misVideos.encontrar(vdBuscar)
    return render_template("/Buscar.html",res=resultado)

@app.route("/recuperaContrasena")
def recuperaContrasena():
    return render_template("recuperaContraseña.html")
    

@app.route("/consultarCorreo",methods=['POST'])
def consultarCorreo():
    correoU = request.form["campo"]
    resultado = misUsuarios.buscar(correoU)
    if len(resultado)<0:
        mensaje = "No se a encontrado una cuenta asociada al correo ingresado"
        return render_template("recuperaContraseña.html",msg=mensaje)
    else:
        #CONFIGURACION PARA ENVIAR EMAILS
        remitente = "tpscab2023@hotmail.com"
        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp.starttls()
        smtp.login(remitente, "CAB+12345+tps")
        codigo = str(randint(0, 99999)).zfill(5) #ZFILL SE USA PARA QUE EL CODIGO TENGA AL MENOS 5 DIGITOS
        #SE INICIA EL ENVIO DE LOS MENSAJES
        mensaje = "Hola,<br>Este es un mensaje de <b>prueba</b><br>\
            Enviado desde python.<br><br>Atentamente,<br>\
                CP9"
        email = EmailMessage()
        email["From"] = remitente
        email["To"] = correoU
        email["subject"] = f"Hola, Tu codigo de verificacion es: {codigo}"
        email.set_content(mensaje, subtype="html")
        #SE ENVIA EL HTML
        smtp.sendmail(remitente,correoU,email.as_string())
        return render_template("verificaCorreo.html",cod=codigo)

@app.route("/compruebaCorreo/<codigo>",methods=["POST"])
def compruebaCorreo(codigo):
    codigoU = request.form["campo"]
    if codigo == codigoU:
        return render_template("cambiaContraseña.html")
    else:
        mensaje = "EL codigo proporsionado es incorrecto"
        return render_template("verificaCorreo.html",msg=mensaje)

if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port="8090") 
