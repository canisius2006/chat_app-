import os,sys,random

def chemin_fichier(path:str) -> str:
    """Cette fonction nous aide à connaître les vrais chemins d'accès d'un fichier"""
    try:
        chemin = sys._MEIPASS
    except:
        chemin = os.path.abspath('.')
    return os.path.join(chemin,path)
#Si tu comprends cet script , c'est que tu es devenu un grand garçon

def mot_hasard():
    """C'est une fonction qui va nous permettre de générer un nom au hasard """
    mot = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    x = ''.join(random.sample(list(mot),k = 8)) + '012345'
    return x
