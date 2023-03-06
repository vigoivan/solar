from tkinter import*
import math
import matplotlib.pyplot as plt
import numpy as np

def hipotenusaxy(x,y):
   i= math.sqrt(x*x+y*y)
   return i
class diadelaño():
    def __init__(self,dia,amanece,anochece):
        self.dia=dia
        self.anochece=anochece
        self.amanece=amanece
        self.dif=self.anochece-self.amanece
    def copy(self,dia):
        self.dia=dia.dia
        self.anochece=dia.anochece
        self.amanece=dia.amanece
        self.dif=dia.dif
class punto():
    def __init__(self):
       self.x = 0
       self.y = 0
       self.z = 1

    def rotatexy(self,angulo):
        angulo=angulo*3.1415926535/180
        if (self.y) != 0 and self.x !=0:
            if (self.y < 0) and(self.x > 0):
                angulo2 = 1.57079632+math.atan(-self.y/self.x)
            elif (self.y < 0) and(self.x <= 0):
                angulo2=3.1415926+math.atan(self.x/self.y)
            elif (self.y > 0) and(self.x <= 0):
                angulo2=4.71238898+math.atan(self.y/-self.x)
            else:
                angulo2=math.atan(self.x/self.y)
        else:
            if self.x==0 and self.y>0:
               angulo2=0
            elif self.x==0 and self.y<0:
                angulo2=3.1415926
            elif self.y==0 and self.x>0:
               angulo2= 1.57079632
            elif self.y==0 and self.x<0:
                angulo2=4.71238898
        angulo += angulo2
        hipot = hipotenusaxy(self.x,self.y)
        self.x = hipot*math.sin(angulo)
        self.y = hipot*math.cos(angulo)
    def rotatexz(self,angulo):
        a = punto()
        a.x = self.x
        a.y = self.z
        a.rotatexy(angulo)
        self.x = a.x
        self.z = a.y
    def rotateyz(self,angulo):
        a = punto()
        a.y = self.y
        a.x = self.z
        a.rotatexy(angulo)
        self.y = a.y
        self.z = a.x
    def modulo(self):
        u=self.x*self.x+self.y*self.y+self.z*self.z 
        return math.sqrt(u)
    def angulo(self,inclinacion):
        i=self.x*inclinacion.x+self.y*inclinacion.y+self.z*inclinacion.z
        u=self.modulo()*inclinacion.modulo()
        return math.acos(i/u)
    def print(self):
        print("a",self.x,self.y,self.z)

def calcular(paralelo,inclinacion1,inclinacion2):
    mesespromedio=[]
 #  auxdia=diadelaño(0,0,0)
    tropico =23 +26/60 +14/3600
    b=punto()
    a=punto()
    c=punto()
    d=punto()
    e=punto()
    a.z=-1
    d.z=-1
    d.rotateyz(paralelo -inclinacion1)
    a.rotateyz(paralelo)
    luzsolaranual=0
    for mes in range(1,13,1):
        dia=int(mes*30.5+85.5) #21 de diciembre es el dia 90
        minutosdeldia=0
        luzsolardiaria=0
        angulo_diario = (tropico)*math.sin(2*math.pi*dia/365)
        amanecio = False
        anochece = False
        for hora in range(24):
            for minuto in range(60):
                minutosdeldia += 1
                b.x=a.x 
                b.y=a.y 
                b.z=a.z
                e.x=d.x
                e.y=d.y
                e.z=d.z
                c.z=1
                c.y=0
                c.x=0
 
                b.rotatexz(0.25 * minutosdeldia)
                e.rotatexz(0.25* minutosdeldia-inclinacion2)
                c.rotateyz(-angulo_diario)
                aux2radianes=e.angulo(c)
                aux2=(aux2radianes*180/math.pi)
                aux=b.angulo(c)*180/math.pi
                if ((aux < 90.0) and not amanecio):
                    amanecio = True
                #   auxdia.amanece=60*hora+minuto*1
                #   auxdia.dia=dia
                if amanecio and aux > 90.0 and not anochece:
                    anochece =True
                 #  auxdia.anochece=hora*60+minuto*1
                 #  auxdia.dif=auxdia.anochece-auxdia.amanece
                if aux2<90 and amanecio and not anochece:
                    luzsolardiaria += math.cos(aux2radianes)/60            
        luzsolaranual += luzsolardiaria
        mesespromedio.append(luzsolardiaria)
    luzsolaranual *= 30.5
    return round(luzsolaranual,2),mesespromedio

def invertirlista(list):
    largodelista=len(list)
    listaux=[]
    for i in range(largodelista):
        listaux.append(list[largodelista-i-1])
    return listaux

def borrado():
    for i in range(4,17):   #borrado de meses y datos
        texto4=Label(raiz,text="                                                           ")
        texto4.grid(row=i,column=0)
        texto4=Label(raiz,text="                                                           ")
        texto4.grid(row=i,column=1)


def enter():  #funcion del boton enter, valida entrada
    mesesdelaño=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","nobiembre","diciembre"]
    borrado()
    try:
        paralelo=float(valor.get())
        inclinacion1=float(valor1.get())
        inclinacion2=float(valor2.get())
    except:
        texto=Label(raiz,text=" revisa los datos ingresados ")
        texto.grid(row=4,column=0,columnspan=2)
    else:
        if paralelo>90:
            texto=Label(raiz,text="Introduzca un valor de latitud menor a 90º")
            texto.grid(row=4,column=0,columnspan=2)
        if inclinacion1>180:
            texto=Label(raiz,text="Introduzca un valor de inclinacion norte menor a 180º")
            texto.grid(row=5,column=0,columnspan=2)
        if inclinacion2>180:
            texto=Label(raiz,text="Introduzca un valor de inclinacion al este menor a 180º")
            texto.grid(row=6,column=0,columnspan=2)
        if paralelo<=90 and inclinacion1<=180 and inclinacion2<180:
            horasanuales,mesesprom=calcular(paralelo,inclinacion1,inclinacion2)
            texto=Label(raiz,text="horas solares al año equivalentes a hs con incidencia a 90ª: "+str(horasanuales))
            texto.grid(row=4,column=0,columnspan=2,sticky="w")
            for i in range(12): 
                texto=Label(raiz,text=mesesdelaño[i])
                texto.grid(row=5+i,column=0,sticky="w")
                texto=Label(raiz,text=str(round(mesesprom[i],1))+" hs solares diarias equivalentes")
                texto.grid(row=5+i,column=1,sticky="w")
            plt.clf()
            plt.title("horas solares promedio por dia equivalentes con 90ª de incidencia")
            plt.barh(invertirlista(mesesdelaño),invertirlista(mesesprom))
            plt.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
            plt.xticks(np.arange(0,10,0.5))  
            plt.show()


raiz=Tk()
raiz.title("solar")
raiz.geometry("380x500")
raiz.resizable(0,0)

texto=Label(raiz,text="introduzca latitud:")
texto.grid(row=0,column=0)

texto1=Label(raiz,text="introduzca inclinacion\n respecto al norte:")
texto1.grid(row=1,column=0)

texto2=Label(raiz,text="introduzca inclinacion\n respecto al este:")
texto2.grid(row=2,column=0)

valor=StringVar()
valor.set("35.00")  # latitud de buenos aires
entradadetexto=Entry(raiz,textvariable=valor)
entradadetexto.grid(row=0,column=1,pady=10)

valor1=StringVar()
valor1.set("0.00")
entradadetexto1=Entry(raiz,textvariable=valor1)
entradadetexto1.grid(row=1,column=1,pady=10)

valor2=StringVar()
valor2.set("0.00")
entradadetexto2=Entry(raiz,textvariable=valor2)
entradadetexto2.grid(row=2,column=1,pady=10)

boton=Button(raiz,text="ENTER",command= enter)
boton.grid(row=3,column=1,pady=10)
borrado()
raiz.mainloop()


