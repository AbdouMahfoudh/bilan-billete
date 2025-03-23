
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.properties import StringProperty
from functions import select, insert
lb_font_size = 30
color = (0,0,0,1)
class MainWindow(Screen):
    
    #x1 = 0
    #x2 = 0
    #l = 0
    lb = {}
    lc = {}
    x1_inst = 0
    x2_inst = 0
    retour = False
    dialog1 = None
    #bilanA = 0
    #bilanB = 0
    sj1 = {}
    sj2 = {}
    ordre = []
    #cont = 0
    tete1 = StringProperty()
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.tete1="Bilan"
    
    
    def ajouter(self):
                    self.bil()
                    try : 
                        self.x1_inst = int(self.input1.text)
                    except:
                        self.x1_inst = 0
                    try :
                        self.x2_inst = int(self.input2.text)
                    except:
                        self.x2_inst = 0
                    mode = select ("select mode from Mode")
                    res = select("select * from result")
                    if mode[0][0] == "sans" :
                        #print (mode)
                        if (self.x1_inst in (25,35) and (res==[] or res[-1][2] <50 ) and self.x2_inst == 0) or (self.x1_inst == 52 and res == []) : 
                            self.x1_inst = 100
                            #print('okkk')
                        if (self.x2_inst in (25,35) and (res==[] or res[-1][1] <50 ) and self.x1_inst == 0) or (self.x2_inst == 52 and res == []) : 
                            self.x2_inst = 100
                        
                    if len(res)!= 0 and (self.x1_inst != 0 or self.x2_inst != 0):
                        insert("insert into result (res1, res2) values (?,?)", (res[-1][1]+self.x1_inst,res[-1][2]+self.x2_inst))
                    elif self.x1_inst != 0 or self.x2_inst != 0 : insert("insert into result (res1, res2) values (?,?)", (self.x1_inst,self.x2_inst))
                    
                    res = select("select * from result")
                    
                    for i in range(5):
                            self.ids[f'lb{i+1}'].text = ''
                            self.ids[f'lc{i+1}'].text = ''
                    if len(self.lb) > 0 :
                                    for j in range(len(self.lb)):
                                        self.gr1.remove_widget(self.lb[j])
                                        self.gr1.remove_widget(self.lc[j])
                                    self.lb = {}
                                    self.lc = {}
                    self.ids.xx1.text = '0'
                    self.ids.xx2.text = '0'
                    if len(res) > 0:
                        for i in range(len(res)) :
                            if i < 5:
                                #self.ids[f'sj1_5'].text = str(5)
                                self.ids[f'lb{i+1}'].text = str(res[i][1])
                                self.ids[f'lc{i+1}'].text =str(res[i][2])
                            else :
                                
                                self.lb[i-5] = Label(text = str(res[i][1]),font_size = 40, bold = True, color = (0,0,0,1))
                                self.gr1.add_widget(self.lb[i-5])
                                self.lc[i-5] = Label(text = str(res[i][2]),font_size = 40, bold = True, color = (0,0,0,1))
                                self.gr1.add_widget(self.lc[i-5])
                    
                    
                        self.ids.input1.text = ''
                        self.ids.input2.text = ''
                        self.retour = True
                        con1 = len(res) ==2 and res[-1][2] == 0 and mode[0][0]=="sans"
                        if (res[-1][1] >99 and res[-1][1]>res[-1][2]) or con1:
                            win = self.ids.moi.text
                            tit = f"Felicitation {win} a gagné"
                            if con1 :
                                tit+= " deux pépe"
                            self.dialog_open(tit,"1 victoire ajouté")
                            
                            res_bil = select("select bil1 from bilan")
                            #print(res_bil)
                            insert("update bilan set bil1 = ? where id = ?", (res_bil[0][0] + 1, 1))
                            self.bil()
                            self.btn3()
                        con2 = len(res) == 2 and res[-1][1] == 0 and mode[0][0]=="sans"
                        if (res[-1][2] >99 and res[-1][2]>res[-1][1]) or con2:
                            win = self.ids.toi.text
                            tit = f"Felicitation {win} a gagné"
                            if con2 :
                                tit+= " deux pépe"
                            self.dialog_open(tit,"1 victoire ajouté")
                            res_bil = select("select bil2 from bilan")
                            #print(res_bil)
                            insert("update bilan set bil2 = ? where id = ?", (res_bil[0][0] + 1, 1))
                            self.bil()
                            self.btn3()
                        res = select ("select * from result")
                        if len(res) >0 :
                            self.ids.xx1.text = str(res[-1][1])
                            self.ids.xx2.text = str(res[-1][2])
                        else : 
                            self.ids.xx1.text = '0'
                            self.ids.xx2.text = '0'
                    else :
                        for i in range(5):
                            self.ids[f'lb{i+1}'].text = ''
                            self.ids[f'lc{i+1}'].text = ''
                        #print(len (self.lb))
                        if len(self.lb) > 0:
                            for i in range(len (self.lb)):
                                self.gr1.remove_widget(self.lb[i])
                                self.gr1.remove_widget(self.lc[i])
                            self.lb = {}
                            self.lc = {}
                        self.ids.xx1.text = '0'
                        self.ids.xx2.text = '0'

    def dialog_open(self, tit, tex):
        self.dialog1 = MDDialog(
                    title = tit ,
                    text = tex,
                    buttons = [
                        MDRectangleFlatButton(text= "OK", on_release= self.ggg2),
                    ],
                )
        self.dialog1.open()

    def dialog_open2(self, tit, tex, func):
        self.dialog1 = MDDialog(
                    title = tit ,
                    text = tex,
                    buttons = [
                        MDFlatButton (text="Non", on_press= self.ggg2),
                        #MDRectangleFlatButton(text= "OK", on_release= self.bilA2),
                        MDRectangleFlatButton(text= "OK", on_release= func),
                    ],
                )
        self.dialog1.open()
    def btn (self):
        
        if self.input1.text.isdigit() and self.input2.text.isdigit() :
            if  int(self.input1.text) < 100 and  int(self.input2.text) < 100:
                if int(self.input1.text) == 0 and int(self.input2.text) == 0 :
                    pass
                else:
                    if int(self.input1.text) + int(self.input2.text) != 26 and int(self.input1.text) + int(self.input2.text) != 16 :
                        
                        self.dialog_open("","movaises entrées")
                    else :
                        self.ajouter()
            else:
                self.dialog_open("entrée invalidée","entrer des nombres inferieure à 100")
                
    
    
        else:
            if self.ids.input1.text.isdigit() and int(self.ids.input1.text)==200 and ( self.ids.input2.text =='' ):
                win = self.ids.moi.text
                title11 = f"Felicitation {win} a gagné une victoire claire"
                text11 = "2 victoires ajoutées"
                self.dialog_open2(title11, text11, self.bilA2 )
                
            else:
                if self.ids.input2.text.isdigit() and int(self.ids.input2.text)==200 and ( self.ids.input1.text =='' ):
                    win = self.ids.toi.text
                    title11 = f"Felicitation {win} a gagné une victoire claire"
                    text11 = "2 victoires ajoutées"
                    self.dialog_open2(title11, text11, self.bilB2)
                    
                else:
                    if self.ids.input1.text.isdigit() and int(self.ids.input1.text)==700 and ( self.ids.input2.text =='' ):
                        win = self.ids.moi.text
                        title11 = f"Felicitation {win} a gagné avec teycé"
                        text11 = "7 victoires ajoutées"
                        self.dialog_open2(title11, text11, self.bilA7)
                        
                        
                    else:
                        if self.ids.input2.text.isdigit() and int(self.ids.input2.text)==700 and ( self.ids.input1.text =='' ):
                            win = self.ids.toi.text
                            title11 = f"Felicitation {win} a gagné avec teycé"
                            text11 = "7 victoires ajoutées"
                            self.dialog_open2(title11, text11, self.bilB7)
                        else :
                            if (self.ids.input1.text.isdigit() and int(self.ids.input1.text) in (26,25,35, 16, 52, 32) and ( self.ids.input2.text =='')) or (self.ids.input2.text.isdigit() and int(self.ids.input2.text) in (26,25,35, 16, 52, 32) and ( self.ids.input1.text =='')  ):
                               self.ajouter()
                            else :
                                self.dialog_open("", "ces champs n'acceptent que des entiers")
                            
        if(len(self.lb) > 8):
            
            text = "apparament ce n'est plus un jeu de billete vous devriez recommencer"
            self.dialog_open2("",text, self.ggg1)
            #self.btn3()
        

    
    def bil(self):
        res_bil = select ("select * from bilan")
        max1 = max(res_bil[0][1], res_bil[0][2])
        if len (self.sj1) >0:
            for i in range (len(self.sj1)):
                self.gr2.remove_widget(self.sj2[i])
                self.gr2.remove_widget(self.sj1[i])
            self.sj1 = {}
            self.sj2  = {}
        for i in range (5):
            self.ids[f'sj1_{i+1}'].text = ''
            self.ids[f'sj2_{i+1}'].text = ''
        for i in range (max1) : 
            if i < 5 :
                if i < res_bil[0][1]:
                    self.ids[f'sj1_{i+1}'].text = str(i+1)
                if i < res_bil[0][2]:
                    self.ids[f'sj2_{i+1}'].text = str(i+1)
            else :
                if i < res_bil[0][1]:
                    self.sj1[i-5] = Label(text = str(i+1),font_size = lb_font_size, bold = True, color = color)
                    self.gr2.add_widget(self.sj1[i-5])
                else :
                    self.sj1[i-5] = Label(text = "",font_size = lb_font_size, bold = True, color = color)
                    self.gr2.add_widget(self.sj1[i-5])

                if i < res_bil[0][2]:
                    self.sj2[i-5] = Label(text = str(i+1),font_size = lb_font_size, bold = True, color = color)
                    self.gr2.add_widget(self.sj2[i-5])
                else :
                    self.sj2[i-5] = Label(text = "",font_size = lb_font_size, bold = True, color = color)
                    self.gr2.add_widget(self.sj2[i-5])
        mini = min(res_bil[0][1], res_bil[0][2])
        if mini <= 0:
                if mini == res_bil[0][1]:
                    self.ids[f'sj1_1'].text = str(mini)
                if mini == res_bil[0][2]:
                    self.ids[f'sj2_1'].text = str(mini)

    def bilA2(self,obj):
        res = select("select bil1 from bilan")
        insert("update bilan set bil1 = ? where id=?",(res[0][0]+2, 1))
        self.dialog1.dismiss()
        self.ids.input1.text = ''
        self.btn3()

    def bilB2(self ,obj):

        res = select("select bil2 from bilan")
        insert("update bilan set bil2 = ? where id=?",(res[0][0]+2, 1))
        #self.bil()
        self.dialog1.dismiss()
        self.ids.input2.text = ''
        self.btn3()
        
    def bilA7(self,obj):
        res = select("select * from teyce")
        res2 = select("select * from bilan")
        if res[0][1]==1:
            insert("update bilan set bil1 = ? where id=?",(res2[0][1]+7, 1))
        elif res[0][1]==2:
            insert("update bilan set bil1 = ?, bil2 = ? where id=?",(res2[0][1]+3,res2[0][2]-3, 1))
        else :
            insert("update bilan set bil1 = ?, bil2 = ? where id=?",(res2[0][1]+2,res2[0][2]-2, 1))
        self.dialog1.dismiss()
        self.ids.input1.text = ''
        self.btn3()
        
    def bilB7(self, obj):
        res = select("select * from teyce")
        res2 = select("select * from bilan")
        if res[0][1]==1:
            insert("update bilan set bil2 = ? where id=?",(res2[0][2]+7, 1))
        elif res[0][1]==2:
            insert("update bilan set bil1 = ?, bil2 = ? where id=?",(res2[0][1]-3,res2[0][2]+3, 1))
        else :
            insert("update bilan set bil1 = ?, bil2 = ? where id=?",(res2[0][1]-2,res2[0][2]+2, 1))
        self.dialog1.dismiss()
        self.ids.input2.text = ''
        self.btn3()
      

    def ggg2(self, obj):
        self.dialog1.dismiss()
    def ggg1(self, obj):
        #self.bil()
        self.btn3()
        self.dialog1.dismiss()
    
    def btn2 ( self):
        insert("DELETE FROM result WHERE id = (SELECT MAX(id) FROM result)")
        self.ajouter()
        
    def btn3(self):
        insert("delete from result")
        self.ajouter()
        