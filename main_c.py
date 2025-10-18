import customtkinter as ctk
import socket
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
        self.picture = ctk.CTkImage(Image.open(self.path),Image.open(self.path),size=(400,400))
        self.ready = True #Une variable qui va nous permettre d'arrêter le thread au bon moment 
        self.debut() #Ici, on fait commence notre animation du début 
        #Ici, on fait le thread pour pouvoir configurer le mode agrandissement 
        Thread(target = self.master.bind,args = ('<Configure>',self.resize),daemon = True ).start()
        self.master.bind('<Button-1>',self.rapide)
        #Ca là va nous permettre de binder l'entree 1
        self.entree_1.bind('<Return>',self.focus_2)
        self.entree_2.bind('<Button-1>',self.clear_entree_2)
    def debut(self):
        """Cette fonction va nous permettre de faire une frame qui va apparaitre au début pour présenter l'app"""
        self.frame_1 = ctk.CTkFrame(self,fg_color='white',corner_radius=20)
        self.frame_1.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)

        self.label_1 = ctk.CTkLabel(self.frame_1,corner_radius=20,image=self.picture,text=None)
        #Ici, on définit les widgets qui viendront pour empêcher certains erreurs de ne plus venir 
        self.label_2 = ctk.CTkLabel(self.frame_1,corner_radius=10,text="NCZ Messagerie",text_color='blue',font=('Helvetica',20,'bold'))
        self.entree_1 = ctk.CTkEntry(self.frame_1,placeholder_text='Entrer votre nom ',corner_radius=10,font=('Helvetica',20,'italic'),placeholder_text_color='black')
        
        self.entree_2 = ctk.CTkComboBox(self.frame_1,values=['localhost'],corner_radius=10,font=('Helvetica',20,'italic'),dropdown_font=('Helvetica',20,'italic'),dropdown_fg_color='white',dropdown_text_color='blue',)
        self.entree_2.set("Entrer l'adresse")
        
        self.bouton_1 = ctk.CTkButton(self.frame_1,text='Confirmer',corner_radius=10,font = ('Helvetica',20))
        self.label_1.place(relx = 0,rely = 0,relheight = 1,relwidth = 1)
        self.info = self.master.after(4000,self.fin)

    def clear_entree_2(self,event):
        """Cette fonction va nous permettre d'enlever le texte d'entrer de la combobox"""
        if self.entree_2.get() == "Entrer l'adresse":
            self.entree_2.set('')
        else:
            pass 
    def rapide(self,event):
        """Cette fonction va nous permettre de vite accéder à l'espace login """  
        self.master.after_cancel(self.info)
        self.fin()
        
    def fin(self):
        """Cette fonction va nous permettre de mettre fin à la page d'accueil, la photo qui vient quoi"""
        self.ready = False 
        self.label_1.place_forget()
        
        self.widgets() #Et maintenant on packe les widgets pour la suite 

    def resize(self,event):
        """Cette fonction va nous permettre de redimensionner la photo du personne """
        if self.ready:
            self.x = self.master.winfo_height()
            self.y = self.master.winfo_width()
            self.picture.configure(size=(self.y,self.x))
            
            self.label_1.configure(image=self.picture)
        else:
            pass 

    def widgets(self):
        """L'ensemble des widgets qu'on va définir et packer""" 
        self.label_2.place(relx=0.1,rely = 0.3,relheight = 0.15,relwidth = 0.8)
        self.entree_1.place(relx = 0.2,rely = 0.5,relwidth = 0.6,relheight = 0.1)
        self.entree_2.place(relx = 0.2,rely = 0.6,relwidth = 0.6,relheight = 0.1)
        self.bouton_1.place(relx = 0.3,rely = 0.7,relwidth = 0.4,relheight = 0.1)
    
    def focus_2(self,event):
        """Cette fonction va nous permettre de mettre le focus sur l'entree 2"""
        self.entree_2.focus()
        if self.entree_2.get() == "Entrer l'adresse":
            self.entree_2.set('')
        else:
            pass
    
    



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
        self.geometry('400x400')
        self.title('NCZ Mail Client ')
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')
        #Ici, on créer un dictionnaire pour chaque connexion pour pouvoir vite se réperer afin d'attribuer les messages aux bonnes personnes
        self.base_de_fenetre = {} 
        self.fenetre_actuelle = None 
        self.liste_des_leurres = []
        self.liste_brouillon_recherche = []  #En fait, c'est des variables qui peuvent me permettre d'aller loin dans ma fonction recherche 
        self.con = [] #C'est une liste qui va me permettre d'exécuter cette fonction conne des boutons
        self.inscription()
        #Ici, un thread pour pouvoir faire quelque chose 
        Thread(target = self.after,args = (500,self.monter_en_haut),daemon = True).start()
       
        #Le fameux mainloop
        self.mainloop()

    def inscription(self):
        """Cette fonction va nous permettre de faire l'inscription"""
        self.begin = accueil(self,photo) #Ici, on crée l'instance d'accueil 
        self.begin.bouton_1.configure(command=lambda:Thread(target=self.fonction_bouton_accueil,daemon=True).start())
        self.begin.entree_2.bind('<Return>',self.valider) #Ici on définit la fonction valider 
    
    def fonction_bouton_accueil(self):
        """Cette fonction va nous permettre de définir les fonctions du bouton accueil"""
        if self.begin.entree_1.get() and self.begin.entree_2.get():
            self.begin.place_forget()
            self.initialisation()

    def valider(self,event):
        """Cette fonction va nous permettre de valider les entree"""
        self.fonction_bouton_accueil()

    def initialisation(self):
        """Cette fonction va nous permettre d'initialiser les classes et fonctions essentielles pour toutes les classes et fonctions"""
        self.name = self.begin.entree_1.get()
        self.ip = self.begin.entree_2.get()
        #Première instance 
        self.instance = reception(self.name,self.ip) #On met en paramètre ce que la personne mettra
        #Deuxième instance 
        self.deuxieme_instance = module_c.reception(self.ip,self.name)
        
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

    def authentifiation(self):
        #Juste après la conexion avec le socket, on va envoyer notre message de bienvenue 
        self.instance.envoyer_message(destinataire='ordinateur',message='connexion réussi')  #L'important, c'est qu'il envoie un message 
    
            

    def widgets(self):
        """"Ici, on a les widgets qu'on va placer sur la fenêtre principale """
        self.rechercher = ctk.CTkEntry(self,placeholder_text='Recherche',corner_radius=10,font=('Helvetica',20))
        self.rechercher.place(relx = 0,rely=0,relheight = 0.1,relwidth = 0.5) #Lui , c'est pour me permettre de rechercher les gens
        
        #Self.boite 1 sera la boite qui prendra en compte la recherche de personne 
        self.boite_1 = ctk.CTkScrollableFrame(self,fg_color='white')
        self.boite_1.place(relx = 0,rely = 0.1,relheight = 1,relwidth = 0.5)
        self.entete = ctk.CTkLabel(self.boite_1,text="Liste de vos conctacts ",wraplength=200,text_color='blue',font=('Helvetica',14),fg_color="#ABB2BF",corner_radius=10)
        self.entete.pack(fill='x')
        #Dans cet deuxième frame que je vais créer, ce sera possible d'afficher un message de bienvenue au client 
        self.boite_2 = ctk.CTkFrame(self,corner_radius=15,fg_color='white')
        self.boite_2.place(relx = 0.5,rely = 0,relheight = 1,relwidth = 0.5)
        self.opening = ctk.CTkLabel(self.boite_2,text="Bienvenue dans l'app de messagerie NCZ \n Commencez par discuter avec vos proches 😍😍",font=('Times',25,'bold'),text_color='blue',wraplength=250)
        self.opening.place(relx=0,rely = 0.2,relheight=0.5,relwidth = 1)
        
        #Ici, les widgets pour la recherche 
        self.frame_de_recherche = ctk.CTkScrollableFrame(self,corner_radius=20,fg_color='white',border_color='blue',border_width=2)
        self.label_info = ctk.CTkLabel(self.frame_de_recherche,text='',corner_radius=10,fg_color='white',text_color='black',font=('Times',20,'bold'),wraplength=200)
        self.label_contact = ctk.CTkLabel(self.frame_de_recherche,text='Liste des contacts disponibles',corner_radius=10,fg_color='blue',text_color='white',font=('Times',15,'bold'),wraplength=200)
        self.bouton_unpack = ctk.CTkButton(self.frame_de_recherche,text='X',fg_color='blue',text_color='black',font=('Times',20,'bold'))
        self.bouton_unpack.pack(fill='x',side=ctk.TOP)
        self.label_info.pack(fill = 'x')


    def meilleur_choix(self,boite):
        """Cette fonction va nous permettre de faire le bon choix entre packer ou lifter"""
        boite.sur_ecran()
        boite.lift()
   
    def obtenir_nom(self,nouko:str):
        """C'est une fonction qui va nous permettre d'obtenir les noms d'utilisateurs adéquats dans certains cas de fonctions"""  
        if nouko == self.name:
            return self.name.capitalize() + '(Vous)'
        elif nouko == 'messagerie01234':
            return 'Messagerie NCZ '
        else:
            return nouko.capitalize() 

    #Le principe consiste à ne pas packer les boutons des frames de messagerie, mais à packet d'autre leurres à la place dans la frame de recherche pour la recherche

    def creation_fenetre_specifique(self):
        """Cette fonction va nous permettre de créer une fenêtre pour chaque connexion"""
        self.liste_amis = self.deuxieme_instance.liste_des_amis 
        #logging.info(str(self.liste_amis)) 
        for element in self.liste_amis:
            self.verificateur = list(self.base_de_fenetre.keys())

            if element[1] in self.verificateur and element[0]=='actif'  : #C'est l'élement 1 que j'ajoute à mon dictionnaire 
                if element[1] == self.name or element[1]=='messagerie01234':
                    pass
                else:
                    ajout = self.base_de_fenetre.get(element[1]) #Ici, on recueille les élements dont nous avons besoin 
                    ajout[2].configure(text=self.obtenir_nom(element[1]) +'(En ligne)')
                
            
            elif element[1] == self.name and element[0]=='actif':
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

            elif element[0] == 'left' and element[1]!='messagerie01234' and element[1]!=self.name :
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
    
            elif element[1] not in self.verificateur :
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
        self.after_cancel(self.marqueur)
        self.after_cancel(self.marqueur_0)
        for i in self.liste_des_leurres:
            i.pack_forget()

        

#Ici, on a l'exécution de notre app
app()
