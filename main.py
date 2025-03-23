from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
#from kivy.uix.widget import Widget
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.properties import StringProperty
from functions import select, insert
#from kivy.core.window import Window

from mainwindow1 import MainWindow
from windowmanager import WindowManager

#Window.size = (300, 580)



class Users(Screen):
    pass
class Victoir(Screen):
    sj1={}
    sj2={}
    lb_font =0
    color = (0,0,0,1)
    def __init__(self, **kwargs):
        super(Victoir, self).__init__(**kwargs)
        self.lb_font= 45
        self.color = (0,0,0,1)

        
    
MainWindow()
    


class Instructions(Screen):
    ins = ""
    def __init__(self, **kwargs):

        super(Instructions, self).__init__(**kwargs)
        self.ins= str("Cette application est pour garder les bilans de jeu de cartes billette \n"
        +"Pour l'utiliser l'interface est claire \n"
        +"1.  Vous commencer en mettant les nims des groupes qui vont jouer dans la page choisir les groupes et vous clicker sur commencer \n"
        +"Ou vous clicker sur avencer et les noms seront par defaut group1 et group2 \n"
        +"2.  L'interface principale est Bilan billet \n"
        +"Vous mettez les resultats de chaques jeu dans les input et vous clicker sur ajouter pour garder les resultat \n"
        +"Le bouton precedent est pour annuler les enregistrements precedents \n"
        +"Le boutton Recommencer est pour est pour annuler le jeu et commecer dés le debut \n"
        +"Les victoires seront ajouter automatiquement a chaque fois que l'un de goupe depasse 100 points \n"
        +"Si la victoire etait claire contre 0 vous ajouter 200 dans l'input du groupe gagnant et 2 victoires seront ajoutées \n"
        +"Si la victoire etait teycé vous ajouter 700 dans l'input du groupe gagnant et 7 victoires seront ajoutées \n"
        +"3.  Vous pouvez acceder à l'interface des victoires en cliquant sur le bouton victoire \n"
        +"Pour réinitialiser les victoures vous cliquez sur le boutton Recommencer")
        

class Paramettres(Screen):
    pass

class Mode(Screen):
    def checkbox_selected1 (self, checked):
        if checked:
            other_checkbox = self.ids.op2 #if checkbox.id == 'checkbox2' else self.root.ids.checkbox2
            other_checkbox.active = False
            
            insert("update mode set mode = ? where id = ?", ("sans", 1))
    
    def checkbox_selected2 (self, checked):
        if checked:
            other_checkbox = self.ids.op1 #if checkbox.id == 'checkbox2' else self.root.ids.checkbox2
            other_checkbox.active = False
            
            insert("update mode set mode = ? where id = ?", ("avec", 1))
    def checkbox_selected3 (self, checked, n):
        if checked:
            for i in range(3):
                if i+1 != n:
                    self.ids[f'op{i+3}'].active = False
            
            insert("update teyce set teyce1 = ? where id = ?", (n, 1))


class Historique(Screen):
    match = ""
    box = {}
    dialog1 = None
    def __init__(self, **kwargs):
        super(Historique, self).__init__(**kwargs)
    def efhist(self):
        self.dialog1 = MDDialog(
            title = "Vous etes certins",
            text = "les historiques seront effacées",
            buttons = [
                MDFlatButton (text="Non", on_press= self.ggg2),
                MDRectangleFlatButton(text= "Oui", on_release= self.ggg1),
                ],
            )
        self.dialog1.open()
        
    
    def ggg2(self, obj):
        self.dialog1.dismiss()
    def ggg1(self, obj):
        
        con = sqlite3.connect('Mybase.db')

        c = con.cursor()

        c.execute(""" delete from victoires
        """)
        con.commit()
        con.close()
        '''l = [self.ids.box1, self.ids.box2, self.ids.box3, self.ids.box4, self.ids.box5,self.ids.box6,self.ids.box7]
        for i in range (7):
            l[i].clear_widgets()'''
        self.bx.clear_widgets()
        
        #m = Label (text = " Historique vide ", color = (0,0,0,1), size_hint_x = 2)
        
        self.box = {}
        self.box[0]= Label (text = " Historique vide ", color = (0,0,0,1), size_hint_y = None,height = 60)
            #screen1.box[0] = BoxLayout(size_hint_y = None,height = 60)
        self.bx.add_widget(self.box[0])
        self.dialog1.dismiss()
        
    
        


            
WindowManager()

kv = Builder.load_file("kivy.kv")

class MyMainApp(MDApp):
    dialog = None
    #root1=None
    
    def build(self):
        con = sqlite3.connect('Mybase.db')

        c = con.cursor()

        c.execute("""
            create table if not exists victoires ( 
                id INTEGER PRIMARY KEY,
                name1 TEXT,
                name2 TEXT,
                bilan1 INTEGER,
                bilan2 INTEGER,
                date_match DATE,
                time_match TEXT)
        """)
        c.execute("""
            create table if not exists Mode ( 
                id INTEGER PRIMARY KEY,
                mode TEXT
                )
        """)
        c.execute("""
            create table if not exists result ( 
                id INTEGER PRIMARY KEY,
                res1 INTEGER,
                res2 INTEGER
                )
        """)
        c.execute("""
            create table if not exists bilan ( 
                id INTEGER PRIMARY KEY,
                bil1 INTEGER,
                bil2 INTEGER
                )
        """)

        c.execute("""
            create table if not exists teyce ( 
                id INTEGER PRIMARY KEY,
                teyce1 INTEGER
                )
        """)
        c.execute("select * from teyce")
        res = c.fetchall()
        if len (res) == 0:
            c.execute("Insert into teyce (teyce1) values (?)", (1,))

        c.execute("select * from bilan")
        res = c.fetchall()
        if len (res) == 0:
            c.execute("Insert into bilan (bil1, bil2) values (?,?)", (0,0))

        c.execute("select * from Mode")
        res = c.fetchall()
        if len (res) == 0:
            c.execute("Insert into Mode (mode) values (?)", ("sans",))

        con.commit()
        con.close()
        return kv
        
    def ggg (self):
        self.dialog= MDDialog(
            title = "Vous etes sur",
            text = "Vous allez perdre les resultats",
            buttons = [
                    MDFlatButton (text="Non", on_press= self.ggg1),
                    MDRectangleFlatButton(text= "Oui", on_press= self.ggg2),
                ],
            )
        self.dialog.open()
    def ggg1(self, obj):
        self.dialog.dismiss()
    def ggg2(self, obj):
        
        self.root.hhh()
        self.dialog.dismiss()
    
    def comm(self):
        self.root.comm1()
    def vict(self):
        self.root.vict1()
    def man(self):
        self.dialog= MDDialog(
                    title = "vous etez sur",
                    text = "vous allez perdre les bilans",
                    buttons = [
                        MDFlatButton (text="Non", on_press= self.ggg1),
                        MDRectangleFlatButton(text= "Oui", on_press= self.man1),
                    ],
                )
        self.dialog.open()
    def man1(self, obj):
        self.root.man1()
        self.dialog.dismiss()
    def avan(self):
        self.root.avan1()
    def hist(self):
        self.root.hist1()
    def sup1(self):
        self.root.sup1()
    def mode1(self):
        self.root.mode1()

if __name__ == "__main__":
    MyMainApp().run()
