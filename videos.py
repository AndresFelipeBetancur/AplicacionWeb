from datetime import datetime,date
import hashlib
import os


class Videos:
    
    def __init__(self,app,conDB,cursor):
        self.app = app
        self.conDB = conDB
        self.cursor = cursor
        
    def buscar(self):
        sql = "SELECT nombreUsuario,video,nombreVideo,portada,FotoUSuario,fechaSubida FROM videos"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    def buscarC(self):
        sql = "SELECT nombreUsuario,video,nombreVideo,portada,FotoUSuario,fechaSubida FROM videos LIMIT 5"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    
    def subir(self,archivo):
        # Obtén la fecha actual
        fecha_actual = date.today()
        # Extrae el año, mes y día de la fecha actual
        year = fecha_actual.year
        month = fecha_actual.month
        day = fecha_actual.day
        
        # Formatea la fecha en el formato 'AAAA-MM-DD'
        fecha_formateada = fecha_actual.strftime('%Y-%m-%d')
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
        
        #Tambien se guardara la foto del usuario que subio el video
        """ahora = datetime.now()
        ruta_archivo = os.path.join('uploads/', archivo[5])
        fname,fext = os.path.splitext(ruta_archivo.filename)
        nombreFoto = "U" + ahora.strftime("%Y%m%d%H%M%S") + fext
        ruta_archivo.save('uploads', archivo[5])"""
        sql=f"INSERT INTO videos (correoUsuario,nombreUsuario,nombreVideo,portada,video,FotoUsuario,fechaSubida)\
            VALUES ('{correoUsuario}','{nombreUsuario}','{nombre}','{nombrePortada}','{nombreVideo}','{archivo[5]}','{fecha_formateada}')"
        self.cursor.execute(sql)
        self.conDB.commit()
        
    def encontrar(self,nombre):
        sql=f"SELECT nombreUsuario,video,nombreVideo,portada FROM videos\
        WHERE nombreVideo LIKE '%{nombre}%'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado