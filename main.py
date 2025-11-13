#Ici, on importe les modules dont nous aurons besoin pour la suite
import socket as st
from threading import Thread
import select,json,module#,traceback
import logging 
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filename=f"D:/Phoenix/projet/messagerie/client/info.log")
#Ici, je veux construire la classe responsable de la créaction de la vérification de la reception de message 
class special:
    """Ceci c'est notre classe spéciale"""
    def __init__(self,client): 
        self.client = client
        self.verification = True #C'est une variable qui va nous permettre de savoir quand est-ce qu'il faut faire la vérification pour
        #savoir quand est-ce qu'il faut faire mourir le thread associé

    def __eq__(self,other): #En fait, j'ai travaillée cette méthode native pour pouvoir faire de tels sorte que j'ai pas de soucis 
        #pour la suite de mon app, il faut qu'il sache faire la différence entre les différents clients qui se connecteront
        return self.client == other.client
    def __hash__(self):
        return hash(self.client) #Dans le but de rendre ça hashable
    
    def recevoir_message(self):  #Ici, j'ai mis out parce que j'ai bien envie de récuperer cette valeur là
        """Cette fonction va nous permettre de recevoir le message"""
        #Ici, j'ai tout fait, mettre la valeur de self.message = None ne marche pas 
        while self.verification:
            #Ici, on met un bloc try pour pouvoir être plus productif
            try:
                self.taille = self.client.recv(8*8).decode()
                self.taille = int(self.taille)
                self.msg = self.client.recv(self.taille)
                self.msg_decoder = {'news':json.loads(self.msg.decode())}

            except ConnectionResetError or BrokenPipeError:  # En cas de problème de déconnexion 
                self.verification = False 
            except AttributeError:
                pass
            except ValueError:
                pass 
    def arret(self):
        """Cette fonction va me permettre d'arrêter l'exécution l'envoie du message"""
        self.msg_decoder["news"] = 0
            
            
    
    def fonction(self):  #En fait , je l'ai nommer comme ça parce que c'est plus facile à écrire
        """Cette fonction va nous permettre d'accorder un thread à chaque connexion"""
        Thread(target = self.recevoir_message,daemon = True).start()


#Ici, on fait l'initialisation de la première fenêtre

class connexion:
    """Cette classe va nous permettre de gérer la connexion de la fenêtre"""
    def __init__(self):
        self.hote,self.port = '',12345
        self.backlog = 5
        self.liste_des_ecoutes = []  #C'est une liste qui va renfermer tous les connexions , les threads qui sont actifs
        self._liste_secondaire = []
        #Pour le moment , je vais faire le préalable
        
        self.prealable()
        Thread(target=self.connexion_serveur,daemon=True).start()
  
    def prealable(self):
        """Cette fonction va nous permettre de faire l'initiation de la connexion du serveur"""
        self.connexion_principale = st.socket(st.AF_INET, st.SOCK_STREAM)
        self.connexion_principale.bind((self.hote,self.port))
        self.connexion_principale.listen(self.backlog)

    def connexion_serveur(self):
        """Cette fonction va nous permettre de gérer la connexion du côté serveur"""
        while True:
            self.rlist,_,self.xlist = select.select([self.connexion_principale],[],[self.connexion_principale],0.05)
            for connect in self.rlist :
                self.connexion,self.info = connect.accept()
                instance = special(self.connexion)
                
                #Avant de continuer ici, je vais d'abord checker un truc, je vais voir si l'instance existe d'abord avant de l'accepter
                if instance in self._liste_secondaire :  #En fait, c'est ligne est possible parce que je l'ai déjà définit auparavant avec l'opérateur egalité de la classe
                    del instance
                else: #Ici, ça veut dire que c'est pas dedans
                    instance.fonction()
                    self.liste_des_ecoutes.append((instance,self.connexion))
                    self._liste_secondaire.append(instance) #C'est lui qui va nous permettre de vérifier la présence de la connexion
                    

class chacun:
    """Cette classe va nous permettre d'attribuer une écoute à chaque client afin d'envoyer les messages aux bonne personnes"""
    def __init__(self,mon_client,base_de_equivalence:dict):
        self.mon_client = mon_client    
        self.base_de_equivalence = base_de_equivalence
        self.feu_vert = True # C'est une variable qui va nous permettre d'arrêter cet thread là 
        Thread(target = self.envoyer_bonne_personne,daemon = True).start()

    def __eq__(self,other):
        return self.mon_client == other.client
    
    def envoyer_bonne_personne(self):
        """Cette fonction va nous permettre d'envoyer le message à la bonne personne"""
        while self.feu_vert:

            #Vérification si la personne s'est déconnecté 
            if self.mon_client[0].verification == False: 
        
                self.feu_vert = False 
                
            
            try:
                self.message_recu = self.mon_client[0].msg_decoder['news']
                
                #Ici, on va recevoir le message de salutation et pouvoir là enregistrer ça dans la base de données
                if self.message_recu:
                   # logging.info(str(self.message_recu)) #Un peu de log pour être rassuré 
                    if self.message_recu['destinataire'] == 'ordinateur':
                        self.base_de_equivalence[self.message_recu['encodeur']]=self.mon_client[1] 
                        self.moi = self.message_recu['encodeur']
                        
                    else: #Autrement, on l'envoie à la bonne personne
                        self.envoyer_message(self.base_de_equivalence.get(self.message_recu['destinataire']),self.message_recu)#Et ici, le travail est fait
                        self.mon_client[0].arret()  
                    
                else:
                    pass

            except AttributeError: #Ici, passe si self.message_recu a un problème 
                pass 
    def ajouter_a_la_liste(self,liste:list,classe):
        """C'est une fonction qui va nous permettre d'ajouter une nouvelle connexion à liste du module"""
        while True:
            try:
                nom = classe.moi
                if nom:
                    if liste.count(['actif',nom]) == 0:
                        liste.append(['actif',nom])
                        if ['left',nom] in liste:
                            liste.remove(['left',nom])
                        else:
                            pass 
                        break
                    else:
                        break
            except:
                pass 
            

    def supprimer_de_la_liste(self,liste,nom):
        """Cette fonction va me permettre de supprimer de la liste"""
        if ['actif',nom] in liste:
            liste.remove(['actif',nom])
        else:
            pass 
        liste.append(['left',nom])

    def envoyer_message(self,destinataire, message):
        """Cette fonction va nous permettre d'envoyer un message """
        self.message = message
        self.destinateur = destinataire
        if self.destinateur:
            self.donnee_json = json.dumps(self.message,ensure_ascii=False).encode()
            self.taille = len(self.donnee_json)
            self.destinateur.sendall(f"{self.taille:08d}".encode())
            self.destinateur.sendall(self.donnee_json)
            self.message = None #C'est vraiment important le nettoyage surtout dans mon cas
        else:
            pass 


class cerveau:
    """Cette classe va nous permettre de constituer notre serveur, pour le moment on a pas besoin de gui"""
    def __init__(self):
        self.instance_connexion = connexion() #Une fois la classe crée, il n'y a plus rien a specifier 
        #Ici, on va également initier la connexion dans le port suivant 
        self.instance_connexion_2 = module.connexion() 
        #Ici, on va créer une liste pour les elements qui seront des instances de chacu
        self.liste_des_chacuns = []
        #Ici, créaction de la base 
        self.base = {}
        self.dictio_important = {} #C'est un dictionnaire qui va me permettre de stocker les classes chacun crées
        # Ici, l'attribution des fonctions de notre base 
        Thread(target = self.attribution,daemon = True).start()


    def attribution(self):
        """Cette fonction va nous permettre d'attribuer à chaque connexion, une classe chacun"""

        while True:
            try:
                for element in self.instance_connexion.liste_des_ecoutes[:]: 
                    if element in self.liste_des_chacuns[:]:
                        
                        if self.dictio_important.get(element).feu_vert == True :
                            pass 
                        else:
                            
                            #Ici, on le supprime de la base 
                            y = self.base.pop(self.dictio_important.get(element).moi)
                            self.instance_connexion.liste_des_ecoutes.remove(element)
                            self.instance_connexion._liste_secondaire.remove(element[0])
                            #Ici, on l'éfface de la rlist 
                            self.instance_connexion.rlist = list(set(self.instance_connexion.rlist) - set(self.instance_connexion.xlist))
                            self.instance_connexion.xlist.clear()                            
                            x = self.dictio_important.pop(element)
                            #interagire avec l'autre module 
                           # x.supprimer_de_la_liste(self.instance_connexion_2.liste_2,x.moi)
                            #Libération des ressources de la mémoire 
                            self.liste_des_chacuns.remove(element)
                            
                            del element,x ,y  


                    else :
                        classe = chacun(element,self.base)
                        self.liste_des_chacuns.append(element)
                        self.dictio_important[element] = classe #J'ajoute dans le dictionnaire le truc 
                        Thread(target = classe.ajouter_a_la_liste,args = (self.instance_connexion_2.liste_2,classe),daemon = True).start()
                
                        
            except AttributeError:
                pass 

#Créaction de l'instance du serveur 
instance = cerveau()

print("serveur démarré")
while instance : 
    try:
        reponse = input("Entrer un nombre en 1 et ...: ") 
        if reponse == '1':
           print(len(instance.instance_connexion.liste_des_ecoutes),'\n')
           print(instance.instance_connexion.liste_des_ecoutes)
           print('\n')
           continue 
        elif reponse == '0':
            break
        elif reponse =='2':
            print(len(instance.base))
            print(f'\n {'-'*15} ')
            print(instance.base,'\n')
        elif reponse =='3':
            print(len(instance.dictio_important))
            print(f'\n {'-'*15} ')
            print(instance.dictio_important,'\n')
        elif reponse =='4':
            print("Ici, c'est pour le module ",len(instance.instance_connexion_2.liste_connexion))
            print(f'\n {'-'*15} ')
            print(instance.instance_connexion_2.liste_connexion,'\n')
        elif reponse =='5':
            print("Ici, c'est pour le module ",len(instance.instance_connexion_2.base_de_mot_de_passe))
            print(f'\n {'-'*15} ')
            print(instance.instance_connexion_2.base_de_mot_de_passe,'\n')
        elif reponse =='6':
            print("Ici, c'est pour le module ",len(instance.instance_connexion_2.base_de_connexion))
            print(f'\n {'-'*15} ')
            print(instance.instance_connexion_2.base_de_connexion,'\n')
        elif reponse =='7':
            print("Ici, c'est pour le module ",len(instance.instance_connexion_2.liste_2))
            print(f'\n {'-'*15} ')
            print(instance.instance_connexion_2.message,'\n')
        else:
            print('choix inexistant')
            continue
    except:
        break