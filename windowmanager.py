
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from functools import partial
import sqlite3
from kivy.uix.image import Image
from datetime import datetime, date
from kivy.core.window import Window
from kivy.app import App
from functions import select, insert

class WindowManager(ScreenManager):
    dialog1 =None
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Window.bind(on_request_close=self.exit_check)
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.on_keyboard)
        #self.counter = 0
    def on_keyboard(self, window, key, *args):
        if key == 27:  # Code de la touche de retour (27 pour Android)
            # Naviguer vers l'écran précédent
            if self.current == 'victoir' or self.current == 'second' :
                self.current = 'main'
                return True  # Indique que l'événement a été géré
            if self.current == 'mode' or self.current == 'instructions' or self.current == 'historique' :
                self.current = 'second'
                return True  # Indique que l'événement a été géré
            if self.current == 'main' or self.current == 'users':
                self.exit_check("")
                return True  # Indique que l'événement a été géré
            
        return False
    def exit_check(self, *args):
        self.dialog= MDDialog(
            title = "vous etes sur",
            text = "vous comptez sortir",
            buttons = [
                MDFlatButton(text= "Non", on_press= self.ddd1),
                MDRectangleFlatButton(text= "Oui", on_press= self.ddd2),
            ],
        )
        self.dialog.open()
        return self.dialog
    def ddd1( self, obj):
        self.dialog.dismiss()
        return False
    def ddd2 (self, obj):
        App.get_running_app().stop()
        #Window.close()
        
    def hhh(self):
        screen1 = self.get_screen("main")
        screen1.btn3()
    def comm1(self):
        screen1 = self.get_screen("main")
        screen2 = self.get_screen("users")
        if len(str(screen2.ids.Joueur1.text))>10 or len(str(screen2.ids.Joueur2.text))>10:
            
            if not self.dialog1:
                self.dialog= MDDialog(
                    text = "Le nom ne doit pas depasser 10 lettres",
                    buttons = [
                        MDRectangleFlatButton(text= "OK", on_press= self.ggg2),
                    ],
                )
            self.dialog.open()
        else :
            if len(str(screen2.ids.Joueur1.text))==0 or len(str(screen2.ids.Joueur2.text))==0:
            
                self.dialog= MDDialog(
                    text = "remplir les champs ou clicker sur avancer",
                    buttons = [
                        MDRectangleFlatButton(text= "OK", on_press= self.ggg2),
                    ],
                )
                self.dialog.open()
            else:
                screen1 = self.get_screen("main")
                screen2 = self.get_screen("users")
                screen1.ids.moi.text = screen2.ids.Joueur1.text
                screen1.ids.toi.text = screen2.ids.Joueur2.text
                screen1.ids.m.text = screen2.ids.Joueur1.text[0:2]
                screen1.ids.t.text = screen2.ids.Joueur2.text[0:2]
                #self.current = "historique"
                #self.current = "victoir"
                screen1.ajouter()
                self.current = "main"
    
    def ggg2(self, obj):
        self.dialog.dismiss()    
        #screen1.comm2()
    def vict1(self):
        screen1 = self.get_screen("main")
        screen2 = self.get_screen("victoir")
        screen2.ids.j1.text = screen1.ids.moi.text
        screen2.ids.j2.text = screen1.ids.toi.text
        res_bil = select ("select * from bilan")
        screen2.ids.xx1.text = str(res_bil[0][1])
        screen2.ids.xx2.text = str(res_bil[0][2])
        max1 = max(res_bil[0][1], res_bil[0][2])
        if len (screen2.sj1) >0:
            for i in range (len(screen2.sj1)):
                screen2.gr2.remove_widget(screen2.sj2[i])
                screen2.gr2.remove_widget(screen2.sj1[i])
            screen2.sj1 = {}
            screen2.sj2  = {}

        for i in range (max1) : 
            
                if i < res_bil[0][1]:
                    screen2.sj1[i] = Label(text = str(i+1),font_size = screen2.lb_font, bold = True, color = screen2.color,
                                            size_hint_y = None ,height = 90)
                    screen2.gr2.add_widget(screen2.sj1[i])
                    
                else :
                    screen2.sj1[i] = Label(text = "",font_size = screen2.lb_font, bold = True, color = screen2.color)
                    screen2.gr2.add_widget(screen2.sj1[i])

                if i < res_bil[0][2]:
                    screen2.sj2[i] = Label(text = str(i+1),font_size = screen2.lb_font, bold = True, color = screen2.color,
                                                    size_hint_y = None ,height = 90)
                    screen2.gr2.add_widget(screen2.sj2[i])
                else :
                    screen2.sj2[i] = Label(text = "",font_size = screen2.lb_font, bold = True, color = screen2.color)
                    screen2.gr2.add_widget(screen2.sj2[i])
        mini = min(res_bil[0][1], res_bil[0][2])
        if mini <= 0:
                if mini == res_bil[0][1]:
                    if len (screen2.sj1)>0:
                        screen2.sj1[0].text = str(mini)
                    else:
                        screen2.sj1[0] = Label(text = str(mini),font_size = screen2.lb_font, bold = True, color = screen2.color)
                        screen2.gr2.add_widget(screen2.sj1[0])
                if mini == res_bil[0][2]:
                    if len (screen2.sj2)>0:
                        screen2.sj2[0].text = str(mini)
                    else:
                        screen2.sj2[0] = Label(text = str(mini),font_size = screen2.lb_font, bold = True, color = screen2.color)
                        screen2.gr2.add_widget(screen2.sj2[0])
        
        self.current = "victoir"
        
        
    def man1(self):
        screen1 = self.get_screen("main")
        screen2 = self.get_screen("victoir")
        current_date = date.today()
        current_time = str(datetime.now().time())[:8]
        #print(screen1.ids.moi.text, screen1.ids.toi.text, current_date, str(current_time)[:8])
        
        res_bil = select ("select * from bilan")
        sql = "insert into victoires (name1, name2, bilan1, bilan2, date_match, time_match) values (?,?,?,?,?,?)"
        parm = (screen1.ids.moi.text,screen1.ids.toi.text,res_bil[0][1],res_bil[0][2], current_date,current_time)
        insert(sql,parm)
        
        insert ("delete from bilan")
        insert("Insert into bilan (bil1, bil2) values (?,?)", (0,0))
        screen1.btn3()
        self.vict1()
    
    def avan1(self):
        #self.current = "historique"
        #self.current = "victoir"
        screen1 = self.get_screen('main')
        screen1.ajouter()
        self.current = "main"
    
    def hist1(self):
        screen1 = self.get_screen('historique')
        
        records = select("select * from victoires")
        screen1.bx.clear_widgets()
        if len(records) == 0:
            screen1.box[0]= Label (text = " Historique vide ", color = (0,0,0,1), size_hint_y = None,height = 80)
            #screen1.box[0] = BoxLayout(size_hint_y = None,height = 60)

            screen1.bx.add_widget(screen1.box[0])
        i = 0
        for record in records[::-1]:
            
            
            m = Label (text = record[1][:7]+" x "+record[2][:7] ,size_hint_x= 2, shorten=True,
                        shorten_from='right', color = (0,0,0,1))
            m.text_size = (m.width, None)
            s = Label (text = str(record[3])+" - "+str(record[4]), color = (0,0,0,1))
            d = Label (text = str(record[5]), color = (0,0,0,1),size_hint_x = 1.1)
            t = Label (text = str(record[6][:5]), color = (0,0,0,1),size_hint_x = 1.1)
                    
            b = Button (text = "" ,background_normal='images/su4.png',
                            background_down= "images/su5.png", on_press=partial(self.sup1, str(record[0])))
                
            screen1.box[i] = BoxLayout(size_hint_y = None,height = 80)
            screen1.box[i].add_widget(m)
            screen1.box[i].add_widget(s)
            screen1.box[i].add_widget(d)
            screen1.box[i].add_widget(t)
            screen1.box[i].add_widget(b)
            screen1.bx.add_widget(screen1.box[i])
            i+=1
        self.current = "historique"

    def sup1(self, a , obj):
        
        
        insert("delete from victoires where id = ?", (int(a),))
        self.hist1()

    def mode1(self):
        screen1 = self.get_screen('mode')
        
        res = select("select mode from Mode ")
        
        if res [0][0] == 'sans':
            screen1.ids.op1.active = True
        else :
            screen1.ids.op2.active = True
        self.current = "mode"
        res2 = select("select * from teyce ")
        screen1.ids[f'op{res2[0][1] + 2}'].active = True
