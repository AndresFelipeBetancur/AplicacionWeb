from datetime import datetime
import hashlib
import os

class Usuarios:
    
    def __init__(self,app,conDB,cursor):
        self.app = app
        self.conDB = conDB
        self.cursor = cursor
    
    def foto(self, correo):
        sql = f"SELECT fotoUsuario FROM usuarios WHERE correo='{correo}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        if resultado:
            return resultado[0][0]  
        
    
    def registrar(self,usuario):
        cifrada=hashlib.sha256(usuario[2].encode("utf-8")).hexdigest()
        ahora = datetime.now()
        fname,fext = os.path.splitext(usuario[3].filename)
        nombreFoto = "E" + ahora.strftime("%Y%m%d%H%M%S") + fext
        usuario[3].save("uploads/" + nombreFoto)
        sql=f"INSERT INTO usuarios (correo,nombreUsuario,contraseña,fotoUsuario) VALUES ('{usuario[0]}','{usuario[1]}','{cifrada}','{nombreFoto}')"
        self.cursor.execute(sql)
        self.conDB.commit()
        
    def buscar(self,correo):
        sql = f"SELECT nombreUsuario FROM usuarios WHERE correo='{correo}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    def loguear(self,correo,contra):
        cifrada = hashlib.sha256(contra.encode("utf-8")).hexdigest()
        sql=f"SELECT nombreUsuario,fotoUsuario FROM usuarios WHERE correo='{correo}' AND contraseña='{cifrada}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado