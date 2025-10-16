#-------- Ici, on va faire une seconde connexion pour pouvoir gérer la connexion , savoir ce qui sont connectés et la liste des personnes disponible sur le serveur -----#

#------- En fait, ici, je ne peux pas garantir beaucoup de choses à l'instant, je n'ai pas révisiter le code parce que ça ressemble à un code que je connaissais déjà ----- #

#Ici, on importe les modules dont nous aurons besoin pour la suite
import socket as st
from threading import Thread
import select,time  #time va nous permettre de programmer quand envoyer cette liste aux client
import logging # C'est pour pouvoir faire le log de mon application 

#logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filename=f"D:/Phoenix/projet/messagerie/client/info.log")

#Ici, on fait l'initialisation de la première fenêtre

class connexion:
    """Cette classe va nous permettre de gérer la connexion de la fenêtre"""
    def __init__(self):
        self.hote,self.port = '',12346 # Ici, on écoute sur le port +1 de l'ancien port 
        self.backlog = 5
        self.liste_connexion = [] #Ici, ça va renfermer la liste des connexions 
        self.encodement = [] #C'est la liste dans lequel les élements qui seront déconnecté seront 
        self.origine = time.time()
        #Pour le moment , je vais faire le préalable
        
        self.prealable()
        Thread(target=self.connexion_serveur,daemon=True).start() #Ici, nous avons le thread qui s'occupe de la connexion 
        Thread(target = self.envoyer_liste,daemon = True).start()
        
    def prealable(self):
        """Cette fonction va nous permettre de faire l'initiation de la connexion du serveur"""
        self.connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
        self.connexion_principale.bind((self.hote,self.port))
        self.connexion_principale.listen(self.backlog)

    def connexion_serveur(self):
        """Cette fonction va nous permettre de gérer la connexion du côté serveur"""
        while True:
            self.rlist,wlist,xlist = select.select([self.connexion_principale],[],[],0.05)
            for connect in self.rlist :
                self.connexion,self.info = connect.accept()
                 
                self.recevoir_message()
                #Avant de continuer ici, je vais d'abord checker un truc, je vais voir si l'instance existe d'abord avant de l'accepter
                if self.connexion in self.liste_connexion :  #En fait, c'est ligne est possible parce que je l'ai déjà définit auparavant avec l'opérateur egalité de la classe
                    del self.connexion
                else: #Ici, ça veut dire que c'est pas dedans
                    self.liste_connexion.append((self.connexion,self.information)) #C'est lui qui va nous permettre de vérifier la présence de la connexion
                   
                   # print(len(self.liste_connexion)) #En phase d'observation 

                    #Ici, on va faire quelque chose pour pouvoir voir ce qui ce sont connectés
                    # with open('info.txt','+a') as f:
                    #     f.write(f'{str(self.info)}\t {str(self.information)} \n')  
    def recevoir_message(self):
        """Cette fonction va nous permettre de recevoir les indentifiants"""
        while True:
            try:
                self.information = self.connexion.recv(1024).decode() 
                break
                # pour la vérification , on fait ça print(self.message)
            except:
                pass
    def en_ligne(self,liste1,liste2):
        """Cette fonction va nous permettre de modifier le statut de quelqu'un s'il est en ligne ou pas"""
        for j in liste1[:]:
            for i in liste2:
                if i[1] == j[1]:
                    i[0] = 'actif'
                    i[1] = j[1]
                    #Ici, on supprime l'élémement correspondant à J
                    liste1.remove(j)
                else:
                    pass 
        return liste1,liste2 
                    
    def envoyer_liste(self):
        """Cette fonction va nous permettre d'envoyer la liste de ceux qui sont disponibles sur le réseau"""
        while True:
            self.liste_2 = [['actif',j] for i,j in self.liste_connexion] #C'est la liste qu'on voudrait envoyer à travers le message 
            self.encodement,self.liste_2 = self.en_ligne(self.encodement,self.liste_2)
            #logging.info(str(self.encodement + self.liste_2))
            try:  
                self.message = str(list(self.encodement+self.liste_2)).encode() #Donc on envoie que la liste des noms avec actif devant chaque nom
                #liste de set au cas où la personne se reconnecte après être déconnecté 
                self.taille = len(self.message)

                for element,identifiant in self.liste_connexion:
                    element.sendall(f"{self.taille:08d}".encode())
                    element.sendall(self.message)
                self.message = None
                
            except ConnectionResetError or BrokenPipeError:
                
                self.liste_connexion.remove((element,identifiant))
                self.encodement.append(['left',identifiant]) #Donc on ajoute le statut de la personne là
                
                
            except IndexError:
                pass #Cet erreur au cas la méthode pop ne marche pas 
                                     
