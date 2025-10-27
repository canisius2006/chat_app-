#-------- Ici, on va faire une seconde connexion pour pouvoir gérer la connexion , savoir ce qui sont connectés et la liste des personnes disponible sur le serveur -----#

#------- En fait, ici, je ne peux pas garantir beaucoup de choses à l'instant, je n'ai pas révisiter le code parce que ça ressemble à un code que je connaissais déjà ----- #

#Ici, on importe les modules dont nous aurons besoin pour la suite
import socket as st
from threading import Thread
import select  #time va nous permettre de programmer quand envoyer cette liste aux client
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

        #Pour le moment , je vais faire le préalable
        #Un bon dictionnaire pour les mots de passe 
        self.base_de_mot_de_passe = {}
        #Une variable pour savoir quand il faut envoyer la liste des personnes connectés 
        self.momentanement = True 
        #Une autre base de connexion pour les nouvelles connexions
        self.base_de_connexion = {}
        self.liste_2 = []
        self.agree = None #Pour dire d'accord
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
        
                self.recevoir_message(self.connexion)
                self.connard = [i for i,j in self.liste_connexion] #Connard parce que j'avais oublié de faire une vérification importante avant 
                #Avant de continuer ici, je vais d'abord checker un truc, je vais voir si l'instance existe d'abord avant de l'accepter

                if self.connexion in self.connard :  #En fait, c'est ligne est possible parce que je l'ai déjà définit auparavant avec l'opérateur egalité de la classe
                    pass 
                else: #Ici, ça veut dire que c'est pas dedans
                    self.liste_connexion.append((self.connexion,self.information)) #C'est lui qui va nous permettre de vérifier la présence de la connexion
                    
                   # print(len(self.liste_connexion)) #En phase d'observation 

                    #Ici, on va faire quelque chose pour pouvoir voir ce qui ce sont connectés
                    # with open('info.txt','+a') as f:
                    #     f.write(f'{str(self.info)}\t {str(self.information)} \n')  
    def recevoir_message(self,connexionner):
        """Cette fonction va nous permettre de recevoir les indentifiants"""
        while True:
            try:
                self.recu = self.connexion.recv(1024).decode() #Ici, il y aura une petite modification, c'est à dire qu'on pourra avoir un message maintenant 
                #Sachant que self.recu est  un str divisé par un symbole particulier, on va jouer sur ça 
                self.recu_1 = self.recu.split('/././') 

                if self.recu_1:
                    self.base_de_connexion[self.recu_1[0]] = connexionner
                    if self.recu_1[2].strip() == '0': #Connexion pour analyser le terrain d'abord 
                        self.information = self.recu_1[0] #L'option 1 contient le nom de la personne 
                        
                        #print('cool')
                    elif self.recu_1[2].strip() == '1': #L'option 1 correspond a signin , c'est à dire qu'on essaie de s'inscrire :
                        
                        self.information = self.recu_1[0]
                        self.base_de_mot_de_passe[self.information] = self.recu_1[1]
                        
                       # print('done')

                    elif self.recu_1[2].strip() == '2': #Ici, c'est en cas de connexion 
                        self.information == self.recu_1[0] 
                        self.check(self.recu_1[0],self.recu_1[1])
                        
                    
                    break
                    # pour la vérification , on fait ça print(self.message) 
            except:
                pass
    
    def confirmer(self):
        """Cette fonction va nous permettre d'envoyer un message lorsque le mot de passe est correcte """
        a = '[True]'.encode()
         
        b = len(a)
        self.base_de_connexion[self.sedo].sendall(f"{b:08d}".encode())
        self.base_de_connexion[self.sedo].sendall(a)
        
        #print('Envoye')

    def infirmer(self):
        """Cette fonction va nous permettre d'envoyer un message lorsque le mot de passe est incorrect"""
        a = '[False]'.encode()
         
        b = len(a)
        self.base_de_connexion[self.sedo].sendall(f"{b:08d}".encode())
        self.base_de_connexion[self.sedo].sendall(a)
         
       # print('Envoye')

    def check(self,nom,password):
        """Cette fonction va nous permettre de vérifier si le mot de passe est correct """
        
        self.sedo = nom #sedo en langue fon veut dire envoyer
       # print("commencé")
        if self.base_de_mot_de_passe.get(nom) == password:
            self.agree = True #Cette variable va nous permettre d'envoyer le message
            
        else:
            self.agree = False 


    def envoyer_liste(self):
        """Cette fonction va nous permettre d'envoyer la liste de ceux qui sont disponibles sur le réseau"""
        while self.momentanement:
           
            try:  
                if self.agree == None:
                    self.message = str(list(self.liste_2)).encode() #Donc on envoie que la liste des noms avec actif devant chaque nom
                    #liste de set au cas où la personne se reconnecte après être déconnecté 
                    self.taille = len(self.message)

                    for element,identifiant in self.liste_connexion:
                        element.sendall(f"{self.taille:08d}".encode())
                        element.sendall(self.message)
                    self.message = None

                if self.agree == True:
                    for i in range(5):
                        self.confirmer()
                    
                    self.agree = None
                    #print("Je t'asssure ")

                if self.agree == False:
                    for i in range(5):
                        self.infirmer()
                        self.agree = None 

                
            except ConnectionResetError or BrokenPipeError:
     
                self.liste_connexion.remove((element,identifiant))

            except ValueError:
                pass
                
            except IndexError:
                pass #Cet erreur au cas la méthode pop ne marche pas 
                                     
