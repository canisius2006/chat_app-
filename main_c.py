import customtkinter as ctk
import socket,time
from threading import Thread
import json, module_c#,logging 
from PIL import Image 
import ressource
#Définition des nots importantes


class accueil(ctk.CTkFrame):
    """Cette classe va me permettre de faire l'accueil pour pouvoir récuperer les informations comme le nom et l'adresse"""
    def __init__(self,master,path):
        super().__init__(master)
        
        self.path = path
        self.configure(fg_color = 'white')
        #Ici, on place la frame contenant l'accueil 
        self.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
        #Ici, on définit la photo qu'on veut packer sur le frame 
        self.picture = ctk.CTkImage(Image.open(self.path),Image.open(self.path),size=(500,400))
        self.ready = True #Une variable qui va nous permettre d'arrêter le thread au bon moment 
        self.ready_2 = True 
        self.debut() #Ici, on fait commence notre animation du début 
        #Ici, on fait le thread pour pouvoir configurer le mode agrandissement 
        Thread(target = self.master.bind,args = ('<Configure>',self.resize),daemon = True ).start()
        self.master.bind('<Button-1>',self.rapide)
        self.compteur = 0
        self.demande()
        self.sign_up_1()
        self.sign_up_2() 
        self.login()
        #Ici, on défini le nom illusoire 
        self.illusoire = ressource.mot_hasard() 
        self.illusoire_1 = f"{self.illusoire}/././ok/././0"
        self.bienvenue()

    def demande(self):
        """Cette fonction va nous permettre de faire l'ouverture, c'est à dire demander l'ip"""
        self.frame_9 = ctk.CTkFrame(self,fg_color='white',corner_radius=10)
        self.entree_8 = ctk.CTkEntry(self.frame_9,placeholder_text="Entrer l'adresse ip",font=('Times',20),width = 400)
        self.bouton_13 = ctk.CTkButton(self.frame_9,text='Confirmer')
        self.entree_8.pack()
        self.bouton_13.pack()

    def ouverture(self):
        """Cette fonction va nous permettre de faire l'accueil pour  demander à la personne si il veut s'inscire ou se connecter """
        
        self.frame_2 = ctk.CTkFrame(self,fg_color='white',corner_radius=10)
        self.frame_plus_1 = ctk.CTkFrame(self.frame_2,fg_color='white',corner_radius=10,border_color='blue',border_width=2)
        self.label_3 = ctk.CTkLabel(self.frame_2,fg_color='blue',text="Bienvenue sur l'application NCZ Messagerie",text_color='white',corner_radius=10,font=('Times',30),wraplength=400)
        self.bouton_2 = ctk.CTkButton(self.frame_plus_1,text="S'inscrire ",text_color='white',font=('Times',30,'underline'),corner_radius=10,fg_color='blue',width=150)
        self.bouton_3 = ctk.CTkButton(self.frame_plus_1,text='Se connecter',fg_color='blue',font=('Times',30,'underline'),text_color='white',corner_radius=10,width = 150)
        #Ici, on packe les widgets 
        self.label_3.pack(side=ctk.TOP,anchor = 'center',fill = 'x')
        self.frame_plus_1.pack(expand = 1,anchor = 'center',ipadx = 5)
        self.bouton_2.pack(anchor = 'center')
        self.bouton_3.pack(anchor = 'center',pady = 5)
    
    def sign_up_1(self):
        """Cette fonction va nous permettre de faire l'inscription """
        self.frame_3 = ctk.CTkFrame(self,fg_color='white',corner_radius=10)
        self.frame_plus_2 = ctk.CTkFrame(self.frame_3,fg_color='white',corner_radius=10,border_color='blue',border_width=2)
        self.bouton_5 = ctk.CTkButton(self.frame_3, text='<-',fg_color='blue',text_color='black',font=('Times',20,'bold'),corner_radius=5)
        self.label_4 = ctk.CTkLabel(self.frame_3,text='Inscription',text_color='white',fg_color = 'blue',corner_radius=10,font=('Times',40,'italic'))
        self.entree_3 = ctk.CTkEntry(self.frame_plus_2,placeholder_text='Entrez votre pseudonyme ',corner_radius=15,font=('Times',20),text_color='black',width = 400)
        self.label_5 = ctk.CTkLabel(self.frame_plus_2,text='',fg_color='white',text_color='blue',font=('Times',20))
        self.bouton_4 = ctk.CTkButton(self.frame_plus_2,text='Confirmer',fg_color='blue',text_color='white',font=('Times',20,'underline'),corner_radius=10)
        #Maintenant on les packe
        self.bouton_5.pack(side = ctk.TOP,anchor = 'nw')
        self.label_4.pack(anchor = 'center',fill = 'x') 
        self.frame_plus_2.pack(expand = 1,anchor = 'center',ipadx = 5)
        self.entree_3.pack(anchor = 'center')
        self.label_5.pack(anchor = 'center')
        self.bouton_4.pack(anchor = 'center')
    
    def verification_du_nom(self,nom)->bool:
        """Cette fonction va nous permettre de vérifier si ce nom n'existe pas déjà dans la base de données, c'est-à-dire si quelqu'un n'a pas encore pris le nom"""
        self.liste_disponible = self.instance.liste_des_amis 
        liste = [] 
        for i, j in self.liste_disponible:
            if nom.lower().strip() == j.lower().strip():
                liste.append(nom)
            else:
                pass
        
        return bool(liste)

    def sign_up_2(self):
        """Cette fonction va nous permettre de faire la fonction pour la phase 2 de l'inscription """
        self.frame_4 = ctk.CTkFrame(self,fg_color='white',corner_radius=10)
        self.frame_plus_3 = ctk.CTkFrame(self.frame_4,fg_color='white',corner_radius=10,border_color='blue',border_width=2)
        self.frame_5 = ctk.CTkFrame(self.frame_plus_3,fg_color='white',corner_radius=10)
        self.bouton_6 = ctk.CTkButton(self.frame_4, text='<-',fg_color='blue',text_color='black',font=('Times',20,'bold'),corner_radius=5)
        self.label_7 = ctk.CTkLabel(self.frame_4,text='Inscription',text_color='white',fg_color = 'blue',corner_radius=10,font=('Times',40,'italic'))
        self.entree_5 = ctk.CTkEntry(self.frame_5,placeholder_text='Mot de passe ',corner_radius=15,font=('Times',20),text_color='black',show='*',width=400)
        self.label_11 = ctk.CTkLabel(self.frame_plus_3,text='',corner_radius=10,fg_color='white',text_color='blue',font=('Times',20,'italic'))
        self.frame_8 = ctk.CTkFrame(self.frame_plus_3,fg_color='white',corner_radius=10)
        self.entree_7 = ctk.CTkEntry(self.frame_8,placeholder_text='Entrer le Mot de passe encore une fois ',corner_radius=15,font=('Times',20),text_color='black',show='*',width=400)
        self.bouton_12 = ctk.CTkButton(self.frame_8, text='voir',fg_color='blue',text_color='black',font=('Times',20,'bold'),corner_radius=5,width = 25)
        self.bouton_7 = ctk.CTkButton(self.frame_5, text='voir',fg_color='blue',text_color='black',font=('Times',20,'bold'),corner_radius=5,width = 25)
        self.label_6 = ctk.CTkLabel(self.frame_plus_3,text='',corner_radius=10,fg_color='white',text_color='blue',font=('Times',20,'italic'))   
        self.bouton_8 = ctk.CTkButton(self.frame_plus_3, text='Confirmer',fg_color='blue',text_color='white',font=('Times',20,'bold'),corner_radius=10)
        #Ici, on packe les widgets 
        self.bouton_6.pack(side=ctk.TOP,anchor = 'nw')
        self.label_7.pack(anchor = 'center',fill='x')
        self.frame_plus_3.pack(expand = 1,anchor = 'center',ipadx = 5)
        self.frame_5.pack(anchor = 'center' )
        self.frame_8.pack(anchor = 'center' )
        self.entree_5.pack(side=ctk.LEFT)
        self.bouton_7.pack(side= ctk.RIGHT)
        self.label_11.pack(after=self.frame_5,anchor = 'center')
        self.entree_7.pack(side=ctk.LEFT)
        self.bouton_12.pack(side= ctk.RIGHT)
        self.label_6.pack(after=self.frame_8,anchor = 'center')
        self.bouton_8.pack(anchor = 'center')

    def connexion_nouveau(self):
        """Cette fonction va nous permettre de se connecter lorsqu'on est nouveau sur le site"""
        #D'abord, on va simuler une déconnexion brutale 
        self.instance.provoquer_rupture()
        self.text_de_connexion = f"{self.entree_3.get().strip()}/././{self.entree_7.get().strip()}/././1"

    def connexion_ancien(self):
        """Cette fonction va nous permettre de se connecter lorsqu'on est nouveau sur le site"""
        #Ici, on fournit juste le text de connexion 
        self.text_de_connexion = f"{self.entree_6.get().strip()}/././{self.entree_4.get().strip()}/././2"
    
    def verification_mot_de_passe(self,password_1,password_2):
        """Cette fonction va nous permettre de vérifier si les mots de passes sont correctes"""
        if password_1 == password_2:
            return True
        else:
            return False 

    def login(self):
        """Cette fonction va nous permettre de faire la partie login, c'est à dire la connexion proprement dite"""
        self.frame_6 = ctk.CTkFrame(self,corner_radius=10,fg_color = 'white')
        self.frame_plus_4 = ctk.CTkFrame(self.frame_6,fg_color='white',corner_radius=10,border_color='blue',border_width=2)
        self.bouton_9 = ctk.CTkButton(self.frame_6, text='<-',fg_color='blue',text_color='black',font=('Times',20,'bold'),corner_radius=5)
        self.label_8 = ctk.CTkLabel(self.frame_6,text='Connexion',text_color='white',fg_color = 'blue',corner_radius=10,font=('Times',40,'italic'))
        self.entree_6 = ctk.CTkEntry(self.frame_plus_4,placeholder_text='Entrez votre pseudonyme',font=('Times',20),corner_radius=10,width = 300)
        self.label_9 = ctk.CTkLabel(self.frame_plus_4,text='',font=('Times',20,'italic'),fg_color='white',text_color='blue',corner_radius=10,height=2)
        self.frame_7 = ctk.CTkFrame(self.frame_plus_4,corner_radius=10,fg_color='white')
        self.entree_4 = ctk.CTkEntry(self.frame_7,placeholder_text='Entrez votre mot de passe',font=('Times',20),show = '*',corner_radius=10,width = 250)
        
        self.bouton_10 = ctk.CTkButton(self.frame_7, text='voir',fg_color='blue',text_color='black',font=('Times',20,'bold'),corner_radius=5,width = 25)
        self.label_10 = ctk.CTkLabel(self.frame_plus_4,text='',corner_radius=10,fg_color='white',text_color='blue',font=('Times',20,'italic'),height=2)
        self.bouton_11 = ctk.CTkButton(self.frame_plus_4, text='Confirmer',fg_color='blue',text_color='white',font=('Times',20,'bold'),corner_radius=10)
        #Ici, on packe les widgets 
        self.bouton_9.pack(side = ctk.TOP, anchor = 'nw')
        self.label_8.pack(anchor = 'center',fill = 'x')
        self.frame_plus_4.pack(expand = 1,anchor = 'center',ipadx = 5)
        self.entree_6.pack(anchor = 'center')
        self.label_9.pack(anchor = 'center')
        self.frame_7.pack(anchor = 'center')
        self.entree_4.pack(side = ctk.LEFT)
        self.bouton_10.pack(side = ctk.RIGHT)
        self.label_10.pack(anchor = 'center')
        self.bouton_11.pack(anchor = 'center')

    def verification_existence(self):
        """Cette fonction va nous permettre de savoir si le nom existe et si la personne s'est déjà connecté """
        self.liste_disponible = self.instance.liste_des_amis 
        nom = self.entree_6.get()
        liste = [] 
        liste_1 = []
        try:
            if nom:
                if self.liste_disponible:
                    self.label_9.configure(text="")
                    for i, j in self.liste_disponible:
                        if nom.lower().strip() == j.lower().strip():
                            if i.lower().strip()=='actif':
                                self.label_9.configure(text="Vous êtes déjà connecté ailleurs")
                                liste_1.append(nom)
                                
                            elif i.lower().strip() == 'left':
                                self.label_9.configure(text=f"Mot de passe, {nom.capitalize()}")
                                liste.append(nom)
                            
                            
                        elif len(liste_1):
                            self.label_9.configure(text="Rien trouvé dans la base ") 
                else:
                    self.label_9.configure(text="Rien trouvé dans la base ")        
            else:
                self.label_9.configure(text="Aucun nom détecté")
        except TypeError:
            pass 

        return bool(liste)
    
    def verification_password(self):
        """Cette fonction va nous permettre de vérifier si le mot de passe est correcte"""
        password = self.entree_4.get()
        temps = time.time()

        if len(password) == 0:
            self.label_10.configure(text='Aucun mot de passe détectée')  
            return False
         
        elif 0<len(password)<4:
            self.label_10.configure(text='Caractères inférieurs à 5')  
            return False 
        
        elif len(password)>4:
            try:
                self.label_10.configure(text='')
                self.instance.provoquer_rupture()
                del self.instance 
                self.text_de_connexion = f"{self.entree_6.get()}/././{self.entree_4.get()}/././2"
                self.instance = module_c.reception(self.entree_8.get(),self.text_de_connexion)
                self.caught= True   
             
                while self.caught:
                    try:
                        if time.time() - temps >5:
                            self.label_10.configure(text='Réessayer encore')
                            break 
                        if self.instance.liste_des_amis[0] == True:
                            self.caught = False 
                            return True
                        
                        if self.instance.liste_des_amis[0] == False:
                            self.label_10.configure(text="Mot de passe erroné")
                            self.caught = False
                            return False 
                        
                        if self.instance.liste_des_amis[0] not in [True,False]:
                            self.label_10.configure(text='...')

                    except:
                        pass 
            except:
                pass
                
            
        
    
    def fonction_bouton_4(self):
        """Cette fonction va nous permettre de faire la fonction du bouton 4 """
        if self.entree_3.get():
            if '012345' in self.entree_3.get():
                self.label_5.configure(text="Pseudonyme invalide")
            elif not self.verification_du_nom(self.entree_3.get()):
                self.label_5.configure(text="")
                self.frame_4.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
                self.frame_4.lift()
            elif self.verification_du_nom(self.entree_3.get()):
                self.label_5.configure(text='Ce nom a déjà été pris')
        else:
            self.label_5.configure(text='Aucun nom détecté')
            

    def fonction_bouton_7(self):
        """Cette fonction va nous permettre de faire la fonction du bouton voir et cacher"""
        
    def fonction_bouton_5(self):
        """Cette fonction va nous permettre de faire la fonction du bouton retour qu'est le bouton 5"""
        
        self.frame_2.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
        self.frame_2.lift()
        
    def fonction_bouton_2(self):
        """Cette fonction va nous permettre de faire la fonction du bouton 2"""
        
        self.frame_3.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
        self.frame_3.lift()

    def fonction_bouton_3(self):
        """Cette fonction va nous permettre de faire la fonction du bouton3"""
        
        self.frame_6.place(relx=0,rely = 0,relheight = 1,relwidth = 1)
        self.frame_6.lift()

    def fonction_bouton_6(self):
        """Cette fonction va nous permettre de faire la fonction du bouton 6"""
        
        self.frame_3.place(relx = 0,rely = 0,relheight = 1,relwidth =1 )
        self.frame_3.lift()
    
    def fonction_password(self,bouton,entrer):
        """Cette fonction va nous permettre la fonction mot de passe"""
        if entrer.cget('show') == '*':
            bouton.configure(text='Cacher')
            entrer.configure(show = '')
            
        else:
            bouton.configure(text='voir')
            entrer.configure(show = '*')
            

    def fonction_bouton_9(self):
        """Cette fonction va nous permettre de faire la fonction du bouton 9"""  
        self.frame_2.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
        self.frame_2.lift()
    
    def fonction_bouton_13(self):
        """Cette fonction va nous permettre de faire la fonction du bouton13"""
        if self.entree_8.get():
            self.frame_2.place(relx = 0,rely=0,relheight = 1,relwidth = 1)
            self.frame_2.lift()
            #Ici, on va commencer notre connexion 
            self.instance = module_c.reception(self.entree_8.get(),self.illusoire_1)
            #-----------------------------------WARNING ----------------------------------
        else:
            pass 

    def attribution_des_fonctions(self):
        """Cette fonction va nous permettre d'attribuer les fonctions """
        
        self.bouton_2.configure(command = self.fonction_bouton_2)
        self.bouton_4.configure(command = self.fonction_bouton_4)
        self.bouton_3.configure(command = self.fonction_bouton_3)
        self.bouton_5.configure(command = self.fonction_bouton_5)
        self.bouton_6.configure(command = self.fonction_bouton_6)
        self.bouton_7.configure(command = lambda:self.fonction_password(self.bouton_7,self.entree_5))
        self.bouton_9.configure(command = self.fonction_bouton_9)
        self.bouton_10.configure(command = lambda:self.fonction_password(self.bouton_10,self.entree_4))  
        self.bouton_12.configure(command = lambda:self.fonction_password(self.bouton_12,self.entree_7))
        self.bouton_13.configure(command = self.fonction_bouton_13)

    def debut(self):
        """Cette fonction va nous permettre de faire une frame qui va apparaitre au début pour présenter l'app"""
        self.frame_1 = ctk.CTkFrame(self,fg_color='white',corner_radius=20)
        self.frame_1.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)

        self.label_1 = ctk.CTkLabel(self.frame_1,corner_radius=20,image=self.picture,text=None)
        #Ici, selfinfo parce qu'on a pas encore packer les widgets qui sont là
        self.label_1.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
        self.info = self.master.after(4000,self.fin)

   
    def rapide(self,event):
        """Cette fonction va nous permettre de vite accéder à l'espace login """  
        if self.ready_2:
            self.master.after_cancel(self.info)
            self.fin()
            self.ready_2 = False 
        else:
            pass 
        
    def fin(self):
        """Cette fonction va nous permettre de mettre fin à la page d'accueil, la photo qui vient quoi"""
        self.ready = False 
        self.label_1.place_forget()

        self.ouverture()
        #self.widgets() #Et maintenant on packe les widgets pour la suite 
        self.frame_9.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
        #Ici, on fait l'attribution des fonctions 
        self.attribution_des_fonctions()

    def resize(self,event):
        """Cette fonction va nous permettre de redimensionner la photo du personne """
        if self.ready:
            self.x = self.master.winfo_height()
            self.y = self.master.winfo_width()
            self.picture.configure(size=(self.y,self.x))
            
            self.label_1.configure(image=self.picture)
        else:
            pass 

    def bienvenue(self):
        """Cette fonction va nous permettre d'afficher quelque chose à l'écran le temps que tout se charge normalement """
        
        self.cadre = ctk.CTkFrame(self.master,fg_color='white',corner_radius=10)
        self.label = ctk.CTkLabel(self.cadre,corner_radius=10,fg_color='white',text_color='purple',font=('Times',40))
        self.label.pack(expand = 1,anchor = 'center')
        Thread(target=self.after,args=(1000,self.animation),daemon = 1).start()
    
    def animation(self):
        """C'est la fonction pour l'animation qu'on va faire"""
        liste = ['|','\\','-','/']
        self.label.configure(text=liste[self.compteur%4]+"\n Un instant...")
        self.compteur +=1
        self.after(1000,self.animation)

    



#On va calibrer le module loggin rapidement 
#logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filename=f"D:/Phoenix/projet/messagerie/client/info_{nom}.log")
#Ici, on fait la classe de l'accueil  et d'entrée des données utilisateur
class reception:
    """Cette classe va nous permettre de gérer la connexion avec le serveur"""
    def __init__(self,nom,adresse):
        self.verification = True
        self.nom = nom
        self.adresse = adresse
        #Ici, on établie la connexion en même temps
        self.connexion_client()
    def connexion_client(self):
        """Cette fonction va nous permettre de faire la connexion avec le serveur"""
        
        # Crée une socket TCP/IP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecte la socket au port où le serveur écoute
        self.server_address = (self.adresse, 12345)
        
        self.sock.connect(self.server_address)

    def envoyer_message(self,destinataire ='ordinateur', message =''):
        """Cette fonction va nous permettre d'envoyer un message """

        self.donnee = {'encodeur':self.nom,'destinataire':destinataire,'message':message}
        self.donnee_json = json.dumps(self.donnee,ensure_ascii=False).encode()
        self.taille = len(self.donnee_json)
        self.sock.sendall(f"{self.taille:08d}".encode())
        self.sock.sendall(self.donnee_json)
        

    def recevoir_message(self):
        """Cette fonction va nous permettre de recevoir un message"""
        #Ici, j'ai tout fait, mettre la valeur de self.message = None ne marche pas 
        while self.verification:
            try:
                self.taille = self.sock.recv(8*8).decode()
                #Ici, on met un bloc try pour pouvoir être plus productif
            
            
                self.taille = int(self.taille)
                self.msg = self.sock.recv(self.taille)
                self.msg_decoder = json.loads(self.msg.decode())

            except:
                pass
    def fonction(self):  #En fait , je l'ai nommer comme ça parce que c'est plus facile à écrire
        """Cette fonction va nous permettre d'accorder un thread à chaque connexion"""
        Thread(target = self.recevoir_message,daemon = True).start()



class fenetre(ctk.CTkFrame):
    """C'est la classe pour notre fenetre principal d'essai, je vais le faire de façon basique, juste pour pouvoir expérimenter ça"""
    def __init__(self,master,serveur,ami):
        super().__init__(master)
        self.serveur = serveur
        self.ami = ami
        self.compteur = 0 #Cette variable va nous permettre de compter le nombre de message non lu 

        self.auto = True # Cette variable pour savoir s'il faut autoriser le self message, c'est un comportement bizarre que j'ai abrégé
        self.si_placer = False # Cette variable va nous permettre de savoir si ça a été déjà placé , je parle de l'écran 
        #Ici, on place les widgets
        self.widgets()
        #Ici, on attribue au bouton ce qu'il va faire dans un attribut proche
        self.bouton_envoyer.configure(command=lambda : Thread(target = self.recuperer,daemon = True).start())

        #Ici, on définit nos fonctions bind
        self.les_bind()
        #Un autre créer , à cause de la fonction copier que nous avons fait
        self.master.bind('<Button-1>',self.fonction_copier_release)
        self.already_send = False 
        
    def sur_ecran(self):
        """Cette fonction va nous permettre de placer le widget sur l'écran """
        #Ici, on va packer la fenêtre sur l'écran afin d'utiliser lift de l'autre côté 
        if not self.si_placer :
            self.place(relx = 0.5,rely = 0,relheight = 1,relwidth = 0.5)
            self.si_placer = True 
        else:
            pass 
    def les_bind(self):
        """Cette fonction va nous permettre de ne pas trop déborder l'initialisation de la classe"""
        
        self.entree.bind('<Return>',self.on_enter)
        self.entree.bind('<Shift-Return>',self.modification_entree)
        self.bouton_envoyer.bind('<Return>',self.recuperer_event)
    def afficher_message_envoyer(self,message):
        """Cette fonction va nous permettre d'afficher le message sur l'écran"""
        
        #Ici, on va faire un hack qu'on avait vu auparavant pour pouvoir permettre de copier le message à l'intérieur 
        ok =  ctk.CTkLabel(self.frame_canva,text=message,wraplength=250,fg_color='blue',text_color='white',corner_radius=10,font=('Segoe UI Emoji',20))
        ok.pack(side='top',anchor = 'ne',pady = 1)
        ok.bind('<Button-3>',lambda e :self.fonction_copier_enter(e,ok))
        
        
    def widgets(self):
        """C'est la fonction de créaction des widgets dont nous aurons besoin pour la suite"""
        self.frame_command = ctk.CTkFrame(self,fg_color='ivory')    
        #La frame qui va porter les élements des messages, autrement les élement envoyer
        self.frame_canva = ctk.CTkScrollableFrame(self,fg_color='white',corner_radius=10,scrollbar_button_color='white',border_width=2,border_color="blue")
        self.frame_canva.place(relx=0,rely=0.05,relheight=0.80,relwidth=1)
        #Ici, on crée une frame qui va nous permettre de placer les autres éléments input
        self.entree = ctk.CTkTextbox(self.frame_command,font=('Segoe UI Emoji',20),corner_radius=10,wrap='word',border_color='black',border_width=2)
        self.bouton_envoyer = ctk.CTkButton(self.frame_command,text='-->',corner_radius=10,font=('Segoe UI Emoji',25),fg_color='blue')
        self.frame_command.place(relx = 0,rely = 0.85,relheight = 0.15,relwidth = 1)
        self.entree.place(relx = 0,rely = 0,relheight = 1,relwidth = 0.8)
        self.bouton_envoyer.place(relx = 0.8,rely = 0.25,relheight = 0.75,relwidth = 0.2)
        #Ceci est un autre widget plus particulier, il va nous permettre de copier des informations sur les labels de message 
        self.popup = ctk.CTkFrame(self,fg_color='white',corner_radius=15,border_color='grey',border_width=3)
        self.popup_bouton_1 = ctk.CTkButton(self.popup,text='Copier',corner_radius=10,font=('Helvetica',15))
        self.popup_bouton_2 = ctk.CTkButton(self.popup,text='Supprimer',corner_radius=10,font=('Helvetica',15))
        self.popup_bouton_1.pack()
        self.popup_bouton_2.pack()
    def recuperer(self):
        """Cette fonction va nous permettre de recuperer ce que la personne a écrit et de l'envoyer"""
        message = self.entree.get("1.0",'end - 1c')
        if message :
            self.entree.delete("1.0",ctk.END)
            self.serveur.envoyer_message(self.ami,message)
            self.afficher_message_envoyer(message)
            del message
            #Ici, je vais déplacer la scale vers le bas
            self.frame_canva.update_idletasks()
            self.frame_canva._parent_canvas.yview_moveto(1.0)
            #Ici, on va définir notre variable sur true pour pouvoir déplacer le bouton en haut 
            self.already_send = True 
        else:
            pass
    def recuperer_event(self,event):
        """Cette fonction va nous permettre de faire la fonction envoyer message version evenement, donc pour le bouton lorsque le bouton a le focus """
        self.recuperer()

    def on_enter(self,event):
        """Cette fonction va nous permettre d'envoyer les messages avec la touche entrer"""
        self.recuperer()
        return 'break'
    
    def modification_entree(self,event):
        """Cette fonction va nous permettre de définir alt+entree comme entree même"""
        self.entree.insert('insert','\n')
        return 'break'
    #-------------------------------------------------------------------------------
    def fonction_du_bouton_1(self,label):
        """Cette fonction va nous permettre de dire ce que fera notre bouton popup"""
        texte = label.cget('text')
        self.master.clipboard_clear()
        self.master.clipboard_append(texte)
        

    def fonction_du_bouton_2(self,label:ctk.CTkLabel):
        """Cette fonction va nous permettre de supprimer un message"""
        if label.cget('fg_color') != 'white':
            label.configure(text='Vous avez supprimer ce message pour vous seul',font=('Helvetica',10,'italic'),text_color='black',fg_color='white')
            self.popup_bouton_1.configure(state='Disabled')
            #Un autre créer , à cause de la fonction copier que nous avons fait
            self.master.bind('<Button-1>',self.fonction_copier_release)
        else:
            label.pack_forget()
             
        
    def fonction_copier_enter(self,event,label:ctk.CTkLabel):
        """Cette fonction va nous permettre de copier le message dans les labels"""
        base = label.pack_info()
        self.popup.pack(after=label,side=base['side'],anchor=base['anchor'])
        self.popup_bouton_1.configure(command=lambda:self.fonction_du_bouton_1(label),state='Normal')
        self.popup_bouton_2.configure(command=lambda:self.fonction_du_bouton_2(label),state='Normal')
        #Un autre créer , à cause de la fonction copier que nous avons fait
        self.master.bind('<Button-1>',self.fonction_copier_release)

    def fonction_copier_release(self,event):
        """Cette fonction correspond au leave et on fera un bind sur la fenêtre entière pour ça"""
        try: # Un bloc try ici pour éviter les malentendus 
            self.popup.pack_forget()
        except:
            pass 
    #--------------------------------------------------------------------------------
    def afficher_message_recu(self,message_recu):
        """Cette fonction va nous permettre d'afficher les messages reçus sur l'écran"""
        if self.auto: #Cette variable nous permet de pouvoir enlever l'option écrire à soi même 
            ok = ctk.CTkLabel(self.frame_canva,text=message_recu,wraplength=250,corner_radius=10,font=('Segoe UI Emoji',20),fg_color="#B7C2DF",text_color='black')
            ok.pack(side=ctk.TOP,anchor='nw')
            ok.bind('<Button-3>',lambda e :self.fonction_copier_enter(e,ok))
            #Ici, je vais déplacer la scale vers le bas
            self.frame_canva.update_idletasks()
            self.frame_canva._parent_canvas.yview_moveto(1.0)
            self.compteur += 1 # Ici, on compte le nombre de message reçu 
        else:
            pass 
        



photo = ressource.chemin_fichier('D:/Phoenix/projet/messagerie/client/image.png')



#Ici, on définit la créaction de notre app
class app(ctk.CTk):
    """C'est la classe de notre application tkinter côté messagerie"""
    def __init__(self):
        super().__init__()
        self.geometry('500x400')
        self.title('NCZ Mail Client ')
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        #Ici, on créer un dictionnaire pour chaque connexion pour pouvoir vite se réperer afin d'attribuer les messages aux bonnes personnes
        self.base_de_fenetre = {} 
        self.fenetre_actuelle = None 
        self.liste_des_leurres = []
        self.liste_brouillon_recherche = []  #En fait, c'est des variables qui peuvent me permettre d'aller loin dans ma fonction recherche 
        self.me = None
        self.con = [] #C'est une liste qui va me permettre d'exécuter cette fonction conne des boutons
        self.inscription()
        #Ici, un thread pour pouvoir faire quelque chose 
        Thread(target = self.after,args = (500,self.monter_en_haut),daemon = True).start()
       
        #Le fameux mainloop
        self.mainloop()

    def inscription(self):
        """Cette fonction va nous permettre de faire l'inscription"""
        self.begin = accueil(self,photo) #Ici, on crée l'instance d'accueil 
        self.begin.bouton_8.configure(command=lambda:Thread(target=self.fonction_bouton_8,daemon=True).start())
        self.begin.bouton_11.configure(command=lambda:Thread(target=self.fonction_du_bouton_11,daemon=True).start())
    
    
    def initialisation(self):
        """Cette fonction va nous permettre d'initialiser les classes et fonctions essentielles pour toutes les classes et fonctions"""
        self.name_1 = self.begin.text_de_connexion
        self.name = self.name_1.split('/././')[0]
        self.ip = self.begin.entree_8.get().strip()
         
        #Première instance 
        self.instance = reception(self.name,self.ip) #On met en paramètre ce que la personne mettra
        #Deuxième instance 
        self.deuxieme_instance = module_c.reception(self.ip,self.name_1)
        
        #Ici, on place les widgets sur l'écran d'accueil  
        self.widgets()
        #Ici, on initie la réception de message pour celui ci
        Thread(target = self.instance.fonction,daemon = True).start()
        #Ici, je créer un thread pour pouvoir créer les threads spécifiques
        Thread(target=self.after,args=(10,self.creation_fenetre_specifique),daemon = True).start()
        #Ici, je créer un thread pour attribution des messages 
        Thread(target=self.after,args=(10,self.attribution_des_messages),daemon=True).start()
        #Je créer un thread pour l'autentification qui est l'envoie de message 

        i = Thread(target = self.authentifiation)
        i.start()
        i.join()
        self.rechercher.bind('<Button-1>',self.recherche_entrer)
        self.rechercher.bind('<Return>',self.recherche_entrer)
        self.bouton_unpack.configure(command=self.recherche_sortir)

    def initialisation_2(self):
        """Cette fonction va nous permettre de faire l'initialisation pour le niveau connecté """
        self.name_1 = self.begin.text_de_connexion
        self.name = self.name_1.split('/././')[0]
        self.ip = self.begin.entree_8.get()
        #Première instance 
        self.instance = reception(self.name,self.ip) #On met en paramètre ce que la personne mettra
        #Ici, on place les widgets sur l'écran d'accueil  
        self.widgets()
        #Ici, on initie la réception de message pour celui ci
        Thread(target = self.instance.fonction,daemon = True).start()
        #Ici, je créer un thread pour pouvoir créer les threads spécifiques
        Thread(target=self.after,args=(10,self.creation_fenetre_specifique),daemon = True).start()
        #Ici, je créer un thread pour attribution des messages 
        Thread(target=self.after,args=(10,self.attribution_des_messages),daemon=True).start()
        #Je créer un thread pour l'autentification qui est l'envoie de message 
        i = Thread(target = self.authentifiation)
        i.start()
        i.join()
        self.rechercher.bind('<Button-1>',self.recherche_entrer)
        self.rechercher.bind('<Return>',self.recherche_entrer)
        self.bouton_unpack.configure(command=self.recherche_sortir)
        self.me = True #Cette variable va nous permettre de savoir qu'on n'a pas utiliser initialisation 1

    def authentifiation(self):
        #Juste après la conexion avec le socket, on va envoyer notre message de bienvenue 
        self.instance.envoyer_message(destinataire='ordinateur',message='connexion réussi')  #L'important, c'est qu'il envoie un message 
    
            

    def widgets(self):
        """"Ici, on a les widgets qu'on va placer sur la fenêtre principale """
        self.frame_all = ctk.CTkFrame(self,fg_color='white')
        #self.frame_all.place(relx=0,rely = 0,relheight = 1,relwidth = 1)
        self.frame_inutile = ctk.CTkFrame(self.frame_all,corner_radius=15,fg_color='white')
        self.rechercher = ctk.CTkEntry(self.frame_inutile,placeholder_text='Recherche',corner_radius=10,font=('Helvetica',20))
        self.rechercher.pack(fill='x')
        self.frame_inutile.place(relx = 0,rely=0,relheight = 0.1,relwidth = 0.5) #Lui , c'est pour me permettre de rechercher les gens
        
        #Self.boite 1 sera la boite qui prendra en compte la recherche de personne 
        self.boite_1 = ctk.CTkScrollableFrame(self.frame_all,fg_color='white')
        self.boite_1.place(relx = 0,rely = 0.1,relheight = 1,relwidth = 0.5)
        self.entete = ctk.CTkLabel(self.boite_1,text="Liste de vos conctacts ",wraplength=200,text_color='blue',font=('Helvetica',14),fg_color="#ABB2BF",corner_radius=10)
        self.entete.pack(fill='x')
        #Dans cet deuxième frame que je vais créer, ce sera possible d'afficher un message de bienvenue au client 
        self.boite_2 = ctk.CTkFrame(self.frame_all,corner_radius=15,fg_color='white')
        self.boite_2.place(relx = 0.5,rely = 0,relheight = 1,relwidth = 0.5)
        self.opening = ctk.CTkLabel(self.boite_2,text="Bienvenue dans l'app de messagerie NCZ \n Commencez par discuter avec vos proches 😍😍",font=('Times',25,'bold'),text_color='blue',wraplength=250)
        self.opening.place(relx=0,rely = 0.2,relheight=0.5,relwidth = 1)
        
        #Ici, les widgets pour la recherche 
        self.frame_de_recherche = ctk.CTkScrollableFrame(self.frame_all,corner_radius=20,fg_color='white',border_color='blue',border_width=2)
        self.label_info = ctk.CTkLabel(self.frame_de_recherche,text='',corner_radius=10,fg_color='white',text_color='black',font=('Times',20,'bold'),wraplength=200)
        self.label_contact = ctk.CTkLabel(self.frame_de_recherche,text='Liste des contacts disponibles',corner_radius=10,fg_color='blue',text_color='white',font=('Times',15,'bold'),wraplength=200)
        self.bouton_unpack = ctk.CTkButton(self.frame_de_recherche,text='X',fg_color='blue',text_color='black',font=('Times',20,'bold'),width=2)
        self.bouton_unpack.pack(side=ctk.TOP,anchor='ne')
        self.label_info.pack(fill = 'x')


    def meilleur_choix(self,boite):
        """Cette fonction va nous permettre de faire le bon choix entre packer ou lifter"""
        boite.sur_ecran()
        boite.lift()
   
    def obtenir_nom(self,nouko:str):
        """C'est une fonction qui va nous permettre d'obtenir les noms d'utilisateurs adéquats dans certains cas de fonctions"""  
        if nouko.lower() == self.name.lower():
            return self.name.capitalize() + '(Vous)'
        elif nouko == 'messagerie01234':
            return 'Messagerie NCZ '
        else:
            return nouko.capitalize() 
        
    def vrai_liste_des_amis(self):
        """Cette fonction va nous aider à choisir la vraie liste des amis à cause de connexion ancien """
        if self.me == True :
            return self.begin.instance.liste_des_amis
        elif self.me == False:
            return self.deuxieme_instance.liste_des_amis
        else:
            pass

    #Le principe consiste à ne pas packer les boutons des frames de messagerie, mais à packet d'autre leurres à la place dans la frame de recherche pour la recherche

    def creation_fenetre_specifique(self):
        """Cette fonction va nous permettre de créer une fenêtre pour chaque connexion"""
        self.liste_amis = self.vrai_liste_des_amis()

        #logging.info(str(self.liste_amis)) 
        for element in self.liste_amis:
            self.verificateur = list(self.base_de_fenetre.keys())

            if element[1] in self.verificateur and element[0]=='actif'  : #C'est l'élement 1 que j'ajoute à mon dictionnaire 
                if element[1].lower() == self.name.lower() or element[1]=='messagerie01234' :
                    pass
                elif element[1].lower() != self.name.lower() or element[1]!='messagerie01234':
                    ajout = self.base_de_fenetre.get(element[1]) #Ici, on recueille les élements dont nous avons besoin 
                    ajout[2].configure(text=self.obtenir_nom(element[1]) +'(En ligne)')
                
            
            elif element[1].lower() == self.name.lower() and element[0]=='actif':
                
                a = fenetre(self,self.instance,element[1])
                b = ctk.CTkButton(self.boite_1,font=('Helvetica',14),text_color='blue',fg_color='white',border_color='blue',hover_color="#B5C4D4",border_width=2,text=f'{element[1].capitalize()} (Vous )')
                b.pack(fill='x') 
                f = ctk.CTkButton(self.frame_de_recherche,text=self.obtenir_nom(element[1]),text_color='blue',fg_color='white',corner_radius=10,border_color='blue',border_width=1)
                #Ici, on créer un label pour pouvoir afficher le nom de la messagerie en haut 
                c = ctk.CTkLabel(a,text='Vous ',font=('Helvetica',20),corner_radius=10,fg_color='blue',text_color='white')
                c.pack(fill = 'x')
                #Ajout à la base de fenêtre 
                self.base_de_fenetre[element[1]] = (a,b,c) #x parce que c'est une variable temporaire  
                a.auto = False # Il ne peut plus s'écrire à lui-même 
                #Configuration de la fonction du bouton 
                d = element[1]
                b.configure(command = lambda d = d ,b = b :self.fonction_bouton(d,b))
                self.liste_des_leurres.append(f) #Ici, on l'ajoute à la liste des leurres 
                f.configure(command=lambda b= b,d=d : (b.pack(fill='x'),self.recherche_sortir(),self.fonction_bouton(d,b)))
                self.authentifiation() #C'est pour augmenter les chances d'exécution de cette fonction 
                self.begin.cadre.place_forget()
                self.frame_all.place(relx=0,rely = 0,relheight = 1,relwidth = 1)

            elif element[1] == 'messagerie01234' and element != self.name and element[0]=="actif":
                a = fenetre(self,self.instance,element[1])
                #Ici, on créer un label pour pouvoir afficher le nom de la messagerie en haut 
                c = ctk.CTkLabel(a,text="Messagerie NCZ",font=('Helvetica',20),corner_radius=10,fg_color='blue',text_color='white')
                c.pack(fill = 'x')
                b =ctk.CTkButton(self.boite_1,font=('Helvetica',14),text_color='blue',fg_color='white',border_color='blue',hover_color="#B5C4D4",border_width=2,text="Messagerie NCZ") 
                # b.pack(fill='x') Il ne faut pas les packer tout de suite 
                f = ctk.CTkButton(self.frame_de_recherche,text=self.obtenir_nom(element[1]),text_color='blue',fg_color='white',corner_radius=10,border_color='blue',border_width=1)
                
                #Ajout à la base de fenêtre 
                self.base_de_fenetre[element[1]] = (a,b,c)#x parce que c'est une variable temporaire 
                a.entree.place_forget()
                a.bouton_envoyer.place_forget()
                ctk.CTkLabel(a.frame_command,text='Vous ne pouvez pas repondre à cette discussion',wraplength=200,text_color='blue',fg_color='white',font=('Helvetica',20)).place(relx=0,rely=0,relheight=1,relwidth=1)
                #Configuration de la fonction du bouton 
                d = element[1]
                b.configure(command = lambda d = d ,b = b :self.fonction_bouton(d,b))
                self.liste_des_leurres.append(f) #Ici, on l'ajoute à la liste des leurres 
                f.configure(command=lambda b= b,d=d : (b.pack(fill='x'),self.recherche_sortir(),self.fonction_bouton(d,b)))
                self.authentifiation() #C'est pour augmenter les chances d'exécution de cette fonction 

            elif element[0] == 'left' and element[1]!='messagerie01234' and element[1].lower()!=self.name.lower() :
                supprimer = self.base_de_fenetre.get(element[1]) #Ici, on recueille les élements dont nous avons besoin 
                if  supprimer:
                    supprimer[2].configure(text=element[1] +' (Déconnecté)')
                else:
                    a = fenetre(self,self.instance,element[1])
                    #Ici, on créer un label pour pouvoir afficher le nom de la messagerie en haut 
                    c = ctk.CTkLabel(a,text=element[1].capitalize()+'(Déconnecté)',font=('Helvetica',20),corner_radius=10,fg_color='blue',text_color='white')
                    c.pack(fill = 'x')
                    b = ctk.CTkButton(self.boite_1,font=('Helvetica',14),text_color='blue',fg_color='white',border_color='blue',hover_color="#B5C4D4",border_width=2,text=element[1].capitalize())
                    # b.pack(fill='x') Il ne faut pas les packer tout de suite 
                    f = ctk.CTkButton(self.frame_de_recherche,text=self.obtenir_nom(element[1]),text_color='blue',fg_color='white',corner_radius=10,border_color='blue',border_width=1)
                    
                    #Ajout à la base de fenêtre 
                    self.base_de_fenetre[element[1]] = (a,b,c) #x parce que c'est une variable temporaire 
                    #Configuration de la fonction du bouton 
                    d = element[1]
                    b.configure(command = lambda d = d ,b = b :self.fonction_bouton(d,b))
                    self.liste_des_leurres.append(f) #Ici, on l'ajoute à la liste des leurres 
                    f.configure(command=lambda b= b,d=d : (b.pack(fill='x'),self.recherche_sortir(),self.fonction_bouton(d,b)))
    
            elif element[1] not in self.verificateur and element[1].lower()!=self.name.lower():
                a = fenetre(self,self.instance,element[1])
                #Ici, on créer un label pour pouvoir afficher le nom de la messagerie en haut 
                c = ctk.CTkLabel(a,text=element[1].capitalize()+'(En Ligne )',font=('Helvetica',20),corner_radius=10,fg_color='blue',text_color='white')
                c.pack(fill = 'x')
                b = ctk.CTkButton(self.boite_1,font=('Helvetica',14),text_color='blue',fg_color='white',border_color='blue',hover_color="#B5C4D4",border_width=2,text=element[1].capitalize())
                # b.pack(fill='x') Il ne faut pas les packer tout de suite 
                f = ctk.CTkButton(self.frame_de_recherche,text=self.obtenir_nom(element[1]),text_color='blue',fg_color='white',corner_radius=10,border_color='blue',border_width=1)
                
                #Ajout à la base de fenêtre 
                self.base_de_fenetre[element[1]] = (a,b,c) #x parce que c'est une variable temporaire 
                #Configuration de la fonction du bouton 
                
                d = element[1]
                b.configure(command = lambda d = d ,b = b :self.fonction_bouton(d,b))
                self.liste_des_leurres.append(f) #Ici, on l'ajoute à la liste des leurres 
                f.configure(command=lambda b= b,d=d : (b.pack(fill='x'),self.recherche_sortir(),self.fonction_bouton(d,b)))

        self.after(10,self.creation_fenetre_specifique)
            
    def attribution_des_messages(self):
        """Cette fonction va nous permettre d'envoyer des messages à chaque fenêtre cible"""
        try:
            if self.instance.msg_decoder:
                destinataire = self.instance.msg_decoder['encodeur']
                la_fenetre = self.base_de_fenetre[destinataire][0] #Ici, on va l'afficher dans l'élément 0 de notre dictionnaire qui est la frame 
                #Ici, après la réception du message, on va déplacer le bouton en haut 
                self.base_de_fenetre[destinataire][1].pack_forget()
                self.base_de_fenetre[destinataire][1].pack(after=self.entete,fill='x')
                la_fenetre.afficher_message_recu(self.instance.msg_decoder['message']) #Et ici, on envoie le message
                self.instance.msg_decoder = None
                #Ici, notre fonction spéciale 
                self.coloration_message(destinataire) #Pour packer la fenêtre 
        except:
            pass
        finally:
            self.after(10,self.attribution_des_messages)

    def coloration_message(self,nom):
        """Cette fonction va me permettre de colorier le nom du bouton au cas où un message viendrait  """
        fen = self.base_de_fenetre.get(nom)[0]
        if self.fenetre_actuelle == nom:
           fen.compteur = 0  #Ici, on remet le compteur à zéro 
        else:     
            self.base_de_fenetre.get(nom)[1].configure(text=f'{self.obtenir_nom(nom )} ({fen.compteur})',text_color = 'red')
            
    def monter_en_haut(self):
        """Cette fonction va nous permettre de faire monter le bouton en haut au cas où on envoie un message"""
        liste = list(self.base_de_fenetre.values()) # Ici, on parcoure la liste des frames pour voir ce qui est prêt à venir en haut 
        for element in liste:
            if element[0].already_send:
                element[1].pack_forget()
                element[1].pack(after = self.entete,fill = 'x')
                element[0].already_send = False 
            else:
                pass 
        self.after(500,self.monter_en_haut)

    def fonction_bouton(self,actuelle,b:ctk.CTkButton ):
        """Cette fonction va nous permettre de modifier la couleur du bouton de chaque chat si c'est la frame actuelle qui est mappé et surtout la fonction du bouton """
        self.fenetre_actuelle = actuelle # C'est pour pouvoir savoir quelle fenêtre est packé 
        liste_des_boutons = [j for i,j,k in list(self.base_de_fenetre.values()) if j!= b]
        self.meilleur_choix(self.base_de_fenetre[actuelle][0])

        b.configure(text_color = 'white',fg_color = 'blue',hover_color="#599FE9",text=self.obtenir_nom(actuelle) ) ; self.base_de_fenetre[actuelle][0].compteur = 0 

        for i in liste_des_boutons:
            i.configure(text_color = 'blue',fg_color = 'white',hover_color="#B5C4D4")
        liste_des_boutons.clear()

    def recherche_1(self):
        """Cette fonction va nous permettre de rechercher une frame de discussion"""
        self.frame_de_recherche.place(relx=0,rely=0.12,relheight = 0.8,relwidth = 0.48)
        get = self.rechercher.get()

        for i in self.liste_des_leurres:
            
            if get :
                if get in i.cget('text').lower():
                    self.liste_brouillon_recherche.append(i)
                    self.label_info.configure(text='Résultat trouvé ')
                    self.label_contact.pack_forget()
                    i.pack(fill = 'x')
                    

                elif len(self.liste_brouillon_recherche) == 0:
                    self.label_info.configure(text='Aucun résultat trouvé ')
                    self.label_contact.pack_forget()
                    try:
                        i.pack_forget() # Donc ici on le supprime et on s'assure qu'il ne soit plus présent sur l'interface
                        self.liste_brouillon_recherche.remove(i) 
                    except:
                        pass 
                elif get not in i.cget('text').lower():
                    self.label_contact.pack_forget()
                    try:
                        i.pack_forget() # Donc ici on le supprime et on s'assure qu'il ne soit plus présent sur l'interface 
                        self.liste_brouillon_recherche.remove(i)
                        
                    except:
                        pass 
            else:
                self.label_contact.pack(fill = 'x',after = self.label_info)
                i.pack(fill='x')
                self.label_info.configure(text='Aucun entrée détectée ')
                
        self.marqueur_0 = self.after(500,self.recherche_1)
    
    def recherche_entrer(self,event):
        """Cette fonction va nous permettre binder la fonction recherche le widget de recherche """
        self.marqueur = self.after(500,self.recherche_1)

    def recherche_sortir(self):
        """Cette fonction va nous permettre de faire la sortie de la recherche """
        self.frame_de_recherche.place_forget()
        self.rechercher.delete(0,ctk.END)
        self.after_cancel(self.marqueur)
        self.after_cancel(self.marqueur_0)
        for i in self.liste_des_leurres:
            i.pack_forget()

    def fonction_bouton_8(self):
        """Cette fonction nous permet de faire la fonction du bouton 8"""
        if len(self.begin.entree_5.get()) ==0:
            self.begin.label_11.configure(text="Aucune entrée détectée")

        elif 0<len(self.begin.entree_5.get())<4:
            self.begin.label_11.configure(text="Caractère inférieurs à 5")

        elif len(self.begin.entree_5.get()) >4 :
            self.begin.label_11.configure(text='')

            if len(self.begin.entree_7.get()) == 0:
                self.begin.label_6.configure(text="Aucune entrée détectée")

            elif 0<len(self.begin.entree_7.get())<4:
                self.begin.label_6.configure(text="Caractère inférieurs à 5")

            elif len(self.begin.entree_7.get()) >4 :
                self.begin.label_6.configure(text='')
                if self.begin.verification_mot_de_passe(self.begin.entree_5.get(),self.begin.entree_7.get()):
                    self.begin.label_11.configure(text='')
                    self.begin.label_6.configure(text='')
                    self.begin.connexion_nouveau()
                    self.begin.place_forget()
                    self.begin.cadre.place(relx = 0,rely = 0,relheight=1,relwidth = 1)
                    
                    self.me = False
                    self.initialisation()

                else:
                    self.begin.label_11.configure(text="")
                    self.begin.label_6.configure(text="Mots de passe différents")


        

    def fonction_du_bouton_11(self):
        """Cette fonction va nous permettre de définir la fonction du bouton 11"""
        if self.begin.verification_existence():
            if self.begin.verification_password():
                self.begin.connexion_ancien()
                self.begin.place_forget()
                self.begin.cadre.place(relx = 0,rely = 0,relheight=1,relwidth = 1)
                
                self.me = True 
                self.initialisation_2()
            else:
                pass
        else:
            pass 

#Ici, on a l'exécution de notre app
app()
