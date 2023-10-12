from datetime import datetime
import hashlib
import os

class Videos:
    
    def __init__(self,app,conDB,cursor):
        self.app = app
        self.conDB = conDB
        self.cursor = cursor
        
    def subir(self,)