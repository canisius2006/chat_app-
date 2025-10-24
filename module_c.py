#------- Ici, on fait le module nécéssaire pour gérer la connexion et savoir ce qui se passe , la liste des connexions disponibles et des personnes disponibles -------#

#Ici, je ne peux pas vous garantir la propreté du code, c'est un copie collée de l'ancien code que j'ai construit

import socket ,ast,struct
from threading import Thread


class reception:
    """Cette classe va nous permettre de gérer la connexion avec le serveur"""
    def __init__(self,adresse,nom):
        self.verification = True
        self.adresse = adresse
        self.nom = nom
        #Ici, il faut que je définisse la liste des amis avant , sinon je risque une erreur
        self.liste_des_amis = []
        #Les bonnes choses commencent ici 
        self.connexion_client() 
        Thread(target=self.recevoir_message,daemon=True).start()

    def connexion_client(self):
        """Cette fonction va nous permettre de faire la connexion avec le serveur"""
        
        # Crée une socket TCP/IP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecte la socket au port où le serveur écoute
        self.server_address = (self.adresse, 12346)
        
        self.sock.connect(self.server_address)

        #Ici, on va envoyer le nom de la personne connecté 
        self.envoyer_identification()

    def envoyer_identification(self):
        """Cette fonction va nous permettre d'envoyer notre nom , nos identification en quelque sorte """
        self.message = str(self.nom)
        self.sock.sendall(self.message.encode())
        self.message = None
        
    def envoyer_message(self,message):
        """Cette fonction va nous permettre d'envoyer des messages"""
        self.message = str(message)
        self.sock.sendall(self.message.encode())
        self.message = None

    def recevoir_message(self):
        """Cette fonction va nous permettre de recevoir un message"""
        #Ici, j'ai tout fait, mettre la valeur de self.message = None ne marche pas 
        while self.verification:
            try:
                self.taille = self.sock.recv(8*8).decode()
                #Ici, on met un bloc try pour pouvoir être plus productif
            
                self.taille = int(self.taille)
                self.msg = ast.literal_eval(self.sock.recv(self.taille).decode())
                self.liste_des_amis = list(self.msg )

            except:
                pass
            # finally:
            #     with open('D:/Phoenix/projet/messagerie/client/texte.txt','+a') as f: 
            #         f.write(str(self.liste_des_amis )+str('\n'))
    def provoquer_rupture(self):
        """Cette fonction va nous permettre de provoquer une déconnexion brutale"""
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack('ii',1,0))
        self.sock.close()

