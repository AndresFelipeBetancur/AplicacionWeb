import datetime
import hashlib
import os

class Usuarios:
    def __init__(self,app,conDB,cursor):
        self.app = app
        self.conDB = conDB
        self.cursor = cursor
    
    def registrar(self,usuario):
        cifrada=hashlib.sha256(usuario[2].encode("utf-8")).hexdigest()
        ahora = datetime.now()
        fname,fext = os.path.splitext(usuario[3].filename)
        nombreFoto = "E" + ahora.strftime("%Y%m%d%H%M%S") + fext
        usuario[3].save("uploads/" + nombreFoto)
        sql=f"INSERT INTO usuarios (correo,nombreUsuario,contraseña,fotoUsuario) VALUES ('{usuario[0]}','{usuario[1]}','{cifrada}','{nombreFoto}')"
        self.cursor.execute(sql)
        self.conDB.commit()
        
    def buscar(self,id):
        sql = f"SELECT nombre FROM usuarios WHERE idusuario='{id}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado