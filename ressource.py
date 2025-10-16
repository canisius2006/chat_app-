import os,sys

def chemin_fichier(path:str) -> str:
    """Cette fonction nous aide à connaître les vrais chemins d'accès d'un fichier"""
    try:
        chemin = sys._MEIPASS
    except:
        chemin = os.path.abspath('.')
    return os.path.join(chemin,path)
#Si tu comprends cet script , c'est que tu es devenu un grand garçon
