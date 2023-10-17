from datetime import datetime
import hashlib
import os

class Videos:
    
    def __init__(self,app,conDB,cursor):
        self.app = app
        self.conDB = conDB
        self.cursor = cursor
    
    def buscar(self):
        sql = "SELECT nombreUsuario,video,nombreVideo,portada FROM videos"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    def subir(self,archivo):
        correoUsuario = archivo[0]
        nombreUsuario = archivo[1]
        nombre = archivo[2]
        #video
        ahora = datetime.now()
        fname,fext = os.path.splitext(archivo[3].filename)
        nombreVideo = "V" + ahora.strftime("%Y%m%d%H%M%S") + fext
        archivo[3].save("uploads/" + nombreVideo)
        #Guardar la portada
        ahora = datetime.now()
        fname,fext = os.path.splitext(archivo[4].filename)
        nombrePortada = "E" + ahora.strftime("%Y%m%d%H%M%S") + fext
        archivo[4].save("uploads/" + nombrePortada)
        sql=f"INSERT INTO videos (correoUsuario,nombreUsuario,nombreVideo,portada,video)\
            VALUES ('{correoUsuario}','{nombreUsuario}','{nombre}','{nombrePortada}','{nombreVideo}')"
        self.cursor.execute(sql)
        self.conDB.commit()
        
    def encontrar(self,nombre):
        sql=f"SELECT nombreUsuario,video,nombreVideo,portada FROM videos\
        WHERE nombreVideo LIKE '%{nombre}%'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado