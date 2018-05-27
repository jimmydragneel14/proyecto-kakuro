from tkinter import * #se importan las librerias necesarias para el juego
import os
from tkinter import ttk
import threading
import winsound
from winsound import *
from threading import *
import time
import random
from tkinter import messagebox
global kakuro #se declara kakuro como global
global jugada
global cont_nivel
global lista_frases
cont_nivel=0
jugada=[]
audio_global=False
lista_top_uno=[]
lista_top_dos=[]
lista_top_tres=[]
contenido=[]
cont_frases=0
lista_jugada=[]
lista_frases=["El anime más largo tiene más de 7400 episodios", "“El Viaje de Chihiro” fue el primer anime en ganar un Oscar", "Los titanes de “Shingeki no Kyojin” están inspirados en una persona borracha","Un personaje de anime en particular tiene 22 actrices de voz diferentes",
              "Para ganar algo necesitas algo del mismo valor...\n Este es el principio del Intercambio Equivalente","Dime, ¿qué crees tú que es la muerte? ¿Un balazo en mitad del corazón? No.\n ¿Una enfermedad que consuma el cuerpo? Tampoco. ¿Un veneno que corrompa la sangre? \n No, señor. La muerte es cuando el mundo te olvida."]

def reproducir_audio():#funcion para ejecutar musica
    global audio_global
    if audio_global==True:
        winsound.PlaySound("Zelda", winsound.SND_FILENAME)
        return reproducir_audio()
def hilo_audio():#funcion que utiliza hilos para reproducir musica sin que afecte el funcionamiento del programa
    global audio_global
    audio_global=True
    audio=Thread(target = reproducir_audio, args=())
    audio.start()
    
def menu():#funcion del menu principal
    global menu_principal
    menu_principal= Tk()#se crea una ventana
    menu_principal.title("Menu principal")
    menu_principal.geometry("700x500")#Se define el tamaño del menu
    menu_principal.resizable(0,0)#se redimensiona la ventana
    menu_principal.configure(background="firebrick1")#se pone un color a la ventana

    Label(menu_principal, text="加算クロス", bg="firebrick1", fg="RoyalBlue1", font="Verdana 28").place(x=240, y=10)
    Label(menu_principal, text="ULTIMATE", bg="firebrick1", fg="Royal Blue", foreground="yellow2", font="Verdana 12").place(x=410, y=50)
    
    #se hacen botones para poder acceder a las distintas ventanas
    boton_jugar= Button(menu_principal, padx=64,pady=10, text="Jugar",  fg= "black", background= "SteelBlue1", command=jugar)
    boton_jugar.place(x=270, y=80)

    boton_configurar= Button(menu_principal, padx=40,pady=10, text="Configuracion",  fg= "black", background= "SteelBlue1", command=configurar)
    boton_configurar.place(x=270, y=160)

    botonAyuda= Button(menu_principal, padx=63,pady=10, text="Ayuda",  fg= "black", background= "SteelBlue1", command=manual)
    botonAyuda.place(x=270, y=240)

    botonacerca= Button(menu_principal, padx=55,pady=10, text="Acerca de",  fg= "black", background= "SteelBlue1", command=acerca_de)
    botonacerca.place(x=270, y=320)

    botonsalir= Button(menu_principal, padx=68,pady=10, text="Salir",  fg= "black", background= "SteelBlue1", command=ventana_salir)
    botonsalir.place(x=270, y=390)

    messagebox.showinfo("Aviso", "Recuerde configurar la partida primero!")


    def relojlocal():#funcion que muestra la hora local
        tiempo=time.strftime('%H:%M:%S',time.localtime())
        
        if tiempo!='':
            pantalla.config(text=tiempo,font='Arial 24')
            
        menu_principal.after(100,relojlocal)
        
    pantalla=Label(menu_principal, bg="firebrick1",justify='center')
    
    pantalla.place(x=10,y=10)
    
    relojlocal()
    
##    menu_principal.mainloop()

    
def leer_archivo_partidas():#funcion que nos permite el archivo en donde viene la estructura de las partidas
    global nivel
    global lista
    global partida
    global cont_nivel
    f = open("kakuro2018partidas.txt")#se abre el archivo
    lineas=f.readlines()#se leen las lineas dearchivo
    if nivel.get()=="1 Neurona":#condiciones para acceder a diversos niveles
        partida=lineas[0]
        partida=eval(partida)#se quitan los strings
        lista=random.choice(partida)#se saca una partida aleatoria
        celdas(lista)
    if nivel.get()=="2 Neuronas":
        partida=lineas[1]
        partida=eval(partida)#se quitan los strings
        lista=random.choice(partida)#se saca una partida aleatoria
        celdas(lista)
    if nivel.get()=="3 Neuronas":
        partida=lineas[2]
        partida=eval(partida)#se quitan los strings
        lista=random.choice(partida)#se saca una partida aleatoria
        celdas(lista)
    if nivel.get()=="Multinivel":
        if cont_nivel==2:
            partida=eval(lineas[2])
            partida=partida[0]
            cont_nivel=cont_nivel+1
            lista=partida
            celdas(lista)
        if cont_nivel<2:#si es menor a 2, va a entrar al nivel 1 o 2, dependiendo del estado del contador
            partida=eval(lineas[cont_nivel])#se saca la partida correspondiente, dependiendo del estado del contador
            partida=partida[0]#se saca la primera tabla del nivel correspondiente
            cont_nivel=cont_nivel+1#se suma uno para cuando complete la tabla, se pueda pasar de nivel
            lista=partida#se defina la lista con la que se va revisar la tabla
            celdas(lista)#se crea la tabla
        if cont_nivel>2:#si el contador es mayor que 2, el juego se queda en el nivel de 3 neuroas
            partida=lineas[2]#se saca la partida del archivo
            partida=eval(partida)#se quitan los strings
            lista=random.choice(partida)#se saca una partida aleatoria
            celdas(lista)#se crea la tabla
        
    if nivel.get()=="":
        pass
    #partida=eval(partida)#se quitan los strings
    #lista=random.choice(partida)#se saca una partida aleatoria
    
    #celdas(lista)#se forma la tabla, utilizando las indicaciones que se obtuvieron del archivo
    f.close()#se cierra el archivo
def celdas(lista):#funcion para crear la matriz grafica del juego
    
    global kakuro
    global marco
    global matriz
    global matrizInterfaz
    global tabla
    matriz=[[-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1]]#se pone una matriz que se podra cambiar
    matrizInterfaz=[[-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1]]
    for i in lista:#se recorre "lista", que es la variable que posee las especificaciones del tablero 
        num_fila=i[2]-1 #variable que saca el numero de fila en donde esta el numero clave
        num_columna=i[3]-1#variable que saca el numero de columna en donde esta el numero clave
        numero=i[1] #variable que indica el numero clave 
        cantidad_espacios=i[4]#variable que indica la cantidad del espacios (entry) que van a haber en el juego para poder digitar numeros
        forma=i[0]#variables que indica si se coloca los entrys de forma vertical u horizontal
        casilla_compartida="" #variable para formar el numero clave
        #Button(marco, text=numero,  fg= "black", bg="white", width=2, height=1, padx=12, pady=6).grid(column=num_columna,row=num_fila)
        if matriz[num_fila][num_columna]!=-1 and matriz[num_fila][num_columna]!=0:#si el numero en la matriz no es un 0 o un -1, sucede esto:
            casilla_compartida=casilla_compartida+str(matriz[num_fila][num_columna])+"/"+ str(numero)+"." + "," + str(cantidad_espacios)#se deduce que va a ser donde va el numero clave
            matriz[num_fila][num_columna]=casilla_compartida#se pone el numero clave, esta variable funcion cuando hay mas de un numero clave compartiendo una misma casilla
        else:
            matriz[num_fila][num_columna]=str(numero)+"." + "," + str(cantidad_espacios)#se coloca un numero clave
        casilla_compartida=""#se resetea la variabla
    
        casillas_blanco(matriz, num_fila, num_columna,cantidad_espacios, forma)#se llama a esta funcion para poner los "0"  que van a funcionar de indicadores para poner los entrys
    entry(matriz)#se llama a una funcion para crear la tabla del kakuro
        
def jugar():#funcion donde se encuentra la tabla y botones del juego
    global kakuro
    global marco
    global matriz
    global linea_texto
    global horas
    global minutos
    global segundos
    global lista_boton
    global et_horas, et_minutos, et_segundos
    global texto_nombre
    
    horas=0
    minutos=0
    segundos=0
    nombre=StringVar
    num_seleccionado=""
    kakuro= Tk()#se crea una ventana
    kakuro.title("Kakuro")
    kakuro.geometry("800x770")#Se define el tamaño del menu
    kakuro.resizable(0,0)#se redimensiona la ventana
    kakuro.configure(background="green2")#se pone un color a la ventana
    
    marco = Frame(kakuro)#se crea un marco para poner la tabla del kakuro
    marco.grid(column=10,row=10,padx=(120,120), pady=(80,80))
    marco.columnconfigure(0, weight=1)
    marco.rowconfigure(0, weight=1)

    messagebox.showinfo("Aviso","Recuerde ingresar su nombre de usuario en la partida!!!")
    
    Label(kakuro, text="Kakuro", bg="green2", fg="gray14", font="Verdana 20").place(x=370, y=10)
    #se crean botones que van a servir para jugar
    boton1= Button(kakuro, text="1",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6, state="disabled", command=lambda:numeros("1"))
    boton1.place(x=670,y= 80)

    boton2= Button(kakuro, text="2",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6, state="disabled", command=lambda:numeros("2"))
    boton2.place(x=670,y= 130)

    boton3= Button(kakuro, text="3",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6,state="disabled", command=lambda:numeros("3"))
    boton3.place(x=670,y= 180)

    boton4= Button(kakuro, text="4",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6,state="disabled", command=lambda:numeros("4"))
    boton4.place(x=670,y= 230)

    boton5= Button(kakuro, text="5",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6,state="disabled", command=lambda:numeros("5"))
    boton5.place(x=670,y= 280)

    boton6= Button(kakuro, text="6",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6,state="disabled", command=lambda:numeros("6"))
    boton6.place(x=670,y= 330)

    boton7= Button(kakuro, text="7",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6,state="disabled", command=lambda:numeros("7"))
    boton7.place(x=670,y= 380)
    
    boton8= Button(kakuro, text="8",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=6,state="disabled", command=lambda:numeros("8"))
    boton8.place(x=670,y= 430)
    
    boton9= Button(kakuro, text="9",  fg= "black", bg="white", width=2, height=1, font="Arial 12", padx=12, pady=4,state="disabled", command=lambda:numeros("9"))
    boton9.place(x=670,y= 480)

    boton_borrador_libre= Button(kakuro, text="Borra libre",  fg= "black", bg="white", width=2, height=1, font="Arial 10", padx=21, pady=6, command=lambda:numeros(""))
    boton_borrador_libre.place(x=590,y= 80)

    boton_iniciar= Button(kakuro, text="Iniciar Juego",  fg= "black", bg="salmon", width=2, height=1, font="Arial 12", padx=40, pady=6, command=lambda:iniciar(lista_boton))
    boton_iniciar.place(x=100,y= 560)

    boton_borrar_jugada= Button(kakuro, text="Deshacer jugada",  fg= "black", bg="cadet blue", width=2, height=1, font="Arial 12", padx=40, pady=6,state="disabled", command=borrar_jugada)
    boton_borrar_jugada.place(x=240,y= 560)

    boton_terminar= Button(kakuro, text="Terminar juego",  fg= "black", bg="cyan", width=2, height=1, font="Arial 12", padx=44, pady=6,state="disabled", command=terminar_juego)
    boton_terminar.place(x=380,y=560 )

    boton_borrar_juego= Button(kakuro, text="Borrar juego",  fg= "black", bg="RoyalBlue1", width=2, height=1, font="Arial 12", padx=35, pady=6,state="disabled", command=borrar_juego)
    boton_borrar_juego.place(x=530,y= 560)

    boton_rehacer= Button(kakuro, text="Rehacer Jugada",  fg= "black", bg="silver", width=2, height=1, font="Arial 12", padx=50, pady=5, command=rehacer_jugada)
    boton_rehacer.place(x=650,y= 660)

##    boton_top= Button(kakuro, text="Top 10",  fg= "black", bg="gold", width=2, height=1, font="Arial 12", padx=20, pady=6,state="disabled", command=top10)
##    boton_top.place(x=660,y= 560)
    #se almacena en una lista todos los botones 
##    lista_boton=[boton1,boton2,boton3,boton4,boton5,boton6,boton7,boton8,boton9, boton_iniciar, boton_borrar_jugada, boton_terminar, boton_top,boton_borrar_juego]
    #boton para musica
    Button(kakuro,text="sonido", command=hilo_audio, bg="sky blue", font="30").place(x=10,y=10)

    Button(kakuro,text=num_seleccionado,fg= "black", bg="light sky blue", width=2, height=1, font="Arial 12", padx=12, pady=6).place(x=670,y=30)    
    
    texto_nombre=Entry(kakuro, textvariable=nombre, font="Arial 10", width=30)
    texto_nombre.place(x=470,y= 620)
    Label(kakuro, text="Nombre del jugador:", bg="green2", fg="gray14", font="Arial 12").place(x=280,y= 620)
    #etiquetas que funcionan para indicar el tiempo
    Label(kakuro,bg="#FFFFFF",text="Tiempo", fg="#CF4647", font="verdana 12", width=19). place(x=50, y=620)
    Label(kakuro,bg="#FFFFFF",text="Horas", fg="#CF4647", font="verdana 8", width=8). place(x=50, y=650)
    Label(kakuro,bg="#FFFFFF",text="Minutos", fg="#CF4647", font="verdana 8", width=8). place(x=120, y=650)
    Label(kakuro,bg="#FFFFFF",text="Segundos", fg="#CF4647", font="verdana 8", width=8). place(x=190, y=650)

    et_horas=Label(kakuro,bg="#FFFFFF",text=horas, fg="#CF4647", font="verdana 7", width=8)
    et_horas. place(x=50, y=680)
    et_minutos=Label(kakuro,bg="#FFFFFF",text=minutos, fg="#CF4647", font="verdana 7", width=8)
    et_minutos. place(x=120, y=680)
    et_segundos=Label(kakuro,bg="#FFFFFF",text=segundos, fg="#CF4647", font="verdana 7", width=8)
    et_segundos. place(x=190, y=680)

    boton_guardar=Button(kakuro, text="Guardar juego", fg="black", bg="gold", font="Arial 12", padx=20, pady=4, command=guardar)
    boton_guardar.place(x=300,y=660)

    boton_cargar=Button(kakuro, text="Cargar juego", fg="black", bg="gold", font="Arial 12", padx=20, pady=4, command=cargar_partida)
    boton_cargar.place(x=500,y=660)
    
    leer_archivo_partidas()
    def top10():
        global texto_nombre
        global horas, segundos, minutos
        #nombre=StringVar()
        #texto_nombre=Entry(kakuro, textvariable=nombre, font="Arial 10", width=30).place(x=470,y= 620)
        lista_niveles=[]
        name=texto_nombre.get()
        if nivel.get()=="1 Neurona":
            horas=horas*3600
            minutos=minutos*60
            datos=[]
            segundos_total=horas+minutos+segundos
            datos.append(name)
            datos.append(segundos_total)
        
            lista_top_uno.insert(0,datos)
            top=dict(lista_top_uno)
            top=sorted(top)
            if len(lista_top_uno)>10:
                lista_top_uno.remove(len(lista_top_uno)-1)
            lista_niveles.append(lista_top_uno)
            f=open("kakuro2018top10","w")
            f.write(str(top))
            f.close()
        
    boton_top= Button(kakuro, text="Top 10",  fg= "black", bg="gold", width=2, height=1, font="Arial 12", padx=20, pady=6,state="disabled", command=top10)
    boton_top.place(x=660,y= 560)

    boton_frase= Button(kakuro, text="Datos curiosos y frases",fg= "black", bg="gold", width=2, height=1, font="Arial 12", padx=80, pady=6,command=frases)
    boton_frase.place(x=100,y= 10)
    

    lista_boton=[boton1,boton2,boton3,boton4,boton5,boton6,boton7,boton8,boton9, boton_iniciar, boton_borrar_jugada, boton_terminar, boton_top,boton_borrar_juego]

def frases():
    global lista_frases
    global cont_frases
    datos= Tk()#se crea una ventana
    datos.title("Datos curiosos")
    datos.geometry("950x100")#Se define el tamaño del menu
    datos.resizable(0,0)#se redimensiona la ventana
    datos.configure(background="gray")#se pone un color a la ventana
    if cont_frases>len(lista_frases)-1:
        cont_frases=0
    
    curioso=lista_frases[cont_frases]
    cont_frases=cont_frases+1
    texto_frase=Label(datos, text=curioso, fg="black", bg="gray", font="Arial 12").place(x=100,y=30)

    

    
def top_ventana():
    ventana_top=Tk()
    ventana_top.title("Top 10: Las leyendas")
    ventana_top.geometry("750x550")#Se define el tamaño del menu
    ventana_top.resizable(0,0)#se redimensiona la ventana
    ventana_top.configure(background="green2")#se pone un color a la ventana

    f=open("kakuro2018top10", "r")
    lineas=f.readlines
    
    
def numeros(numero):#funcion complemetaria que sirve para declarar el valor de la variable "num_seleccionado"
    global num_seleccionado
    num_seleccionado=""
    if numero=="1":
        num_seleccionado="1"
        
    if numero=="2":
        num_seleccionado="2"
        
    if numero=="3":
        num_seleccionado="3"
    if numero=="4":
        num_seleccionado="4"
    if numero=="5":
        num_seleccionado="5"
    if numero=="6":
        num_seleccionado="6"
    if numero=="7":
        num_seleccionado="7"
    if numero=="8":
        num_seleccionado="8"
    if numero=="9":
        num_seleccionado="9"
    if numero=="":
        num_seleccionado=""#num_seleccionado es un string vacio para poder quitar los elementos que hayan en una casilla 
    #boton en donde se podra visualizar que boton se selecciono
    Button(kakuro,text=num_seleccionado,fg= "black", bg="light sky blue", width=2, height=1, font="Arial 12", padx=12, pady=6).place(x=670,y=30)    
    return num_seleccionado
        
def callback(event):#funcion que sirve para poder ingresar numeros en el tablero
    global num_seleccionado
    global kakuro
    if numeros(num_seleccionado)=="1":#si numeros(num_seleccionado) es igual a "1" se puede digitar 1
        event.widget.delete(0,END)
        event.widget.insert(0,1)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
    
    if numeros(num_seleccionado)=="2":#si numeros(num_seleccionado) es igual a "2" se puede digitar 2
        event.widget.delete(0,END)
        event.widget.insert(0,2)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave

    if numeros(num_seleccionado)=="3":#si numeros(num_seleccionado) es igual a "3" se puede digitar 3
        event.widget.delete(0,END)
        event.widget.insert(0,3)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
        
    if numeros(num_seleccionado)=="4":#si numeros(num_seleccionado) es igual a "4" se puede digitar 4
        event.widget.delete(0,END)
        event.widget.insert(0,4)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
        
    if numeros(num_seleccionado)=="5":#si numeros(num_seleccionado) es igual a "5" se puede digitar 5
        event.widget.delete(0,END)
        event.widget.insert(0,5)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
        
    if numeros(num_seleccionado)=="6":#si numeros(num_seleccionado) es igual a "6" se puede digitar 6
        event.widget.delete(0,END)
        event.widget.insert(0,6)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
    
    if numeros(num_seleccionado)=="7":#si numeros(num_seleccionado) es igual a "7" se puede digitar 7
        event.widget.delete(0,END)
        event.widget.insert(0,7)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
        
    if numeros(num_seleccionado)=="8":#si numeros(num_seleccionado) es igual a "8" se puede digitar 8
        event.widget.delete(0,END)
        event.widget.insert(0,8)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
        
    if numeros(num_seleccionado)=="9":#si numeros(num_seleccionado) es igual a "9" se puede digitar 9
        event.widget.delete(0,END)
        event.widget.insert(0,9)
        matriz_espacios()#funcion para crear una matriz del estado actual de la tabla
        pasa_valor()#funcion que sirve para verificar si se repiten numeros en una misma columna o fila
        revisa_suma()#funcion que sirve para verificar si la suma de los numeros ingresados es igual al numero clave
        

    if numeros(num_seleccionado)=="":
        event.widget.delete(0,END)#funcion para borrar lo que haya en una casilla

    
    
    
def iniciar(botones):#funcion para iniciar el juego
    global reloj
    global horas
    global minutos
    global segundos
    for i in botones:#se desbloquean los botones en la lista
        i.config(state="normal")
    #parte del reloj
    if reloj.get()=="Si":#si de la listbox se obtiene un "si", se pone un cronometro
        cronometro()
    if reloj.get()=="No":#se se pone "no", no se pone ningun medidor de tiempo
        horas=0
        minutos=0
        segundos=0
    if reloj.get()=="Timer":#si se pone "timer", se pone un temporizador
        timer()
        


def casillas_blanco(matriz, fila, columna, cantidad, n):#funcion que sirve para poner la cantidad de "0" indicados en las especificacion para saber cuantos entrys poner
    if n == 2:
        for i in range(fila+1, fila + cantidad+1):
            matriz[i][columna] = 0
        
    if n == 1:
        for i in range(columna+1, columna + cantidad+1):
            matriz[fila][i] = 0

def entry(matriz):#funcion que crea la tabla
    global marco
    global linea_texto
    global sv
    global x
    global lista_num
    global lista
    global matrizInterfaz
    n="."#variable que sirve para poder diferenciar de labels y entrys
    fila=0
    columna=0
    lista_num=[[],[],[],[],[],[],[],[],[]]#variable en el que va crear una nueva matriz
    variable = StringVar()
    for i in matriz:#se recorre la matriz
        for casilla in i:
            if casilla==-1:#si en la matriz se encuentra un "-1", esto indica que es un relleno en el juego
                Entry(marco, width=2, font="Arial 27", justify="center",bg="red", state="disabled").grid(column=columna,row=fila)
                columna=columna+1#se suma uno para poder recorrer la matriz
                lista_num[fila].append(-1)
            if casilla==0:#si se encuentra un "0", esto indica que se va a poner un entry en el cual el usuario podra digitar numeros
                sv = StringVar()#se crean un stringvar
                
                x = Entry(marco, textvariable = sv , width=2, font="Arial 27", justify="center")
                x.grid(column=columna,row=fila)
                x.bind('<Button-1>', (lambda x = x: callback(x)))#se usa bind para poder enlazar los entry y poder ingresar numeros
                
                valor_casilla=x.get()#se saca lo que haya en el entry
                matrizInterfaz[fila][columna] = sv#se crea una gran cantidad de stringvar
                lista_num[fila].append(x)#se agrega en lista_num, el entry
                columna=columna+1#se suma uno para poder recorrer la matriz
                
            if casilla !=0 and casilla!=-1:#si la casilla es diferente de -1 y 0, sucede esto
                if n not in casilla:#si no posee ".", osea n, no es un label, sino un entry con un digito previamente ingresado
                    sv = StringVar()
                    matrizInterfaz[fila][columna] = sv
                    x=Entry(marco,bg="ivory3",width=2,fg="black", state="normal", justify="center")
                    x.bind('<Button-1>', (lambda x = x: callback(x)))
                    x.grid(column=columna,row=fila)
                    x.insert(0,casilla)
                    lista_num[fila].append(x)
                    columna=columna+1
                    direccion.append(x)
                if n in casilla:#si tiene un ".", osea n, significa que es un label con el numero clave
                    variable=casilla
                    matrizInterfaz[fila][columna] = str(variable)
                    variable_real=matrizInterfaz[fila][columna]            
                    x=Button(marco,text=casilla,bg="azure",fg="black",width=2, font="Arial 10", padx=10, pady=9, command=lambda  variable=variable: combinaciones(str(variable)))
                    x.grid(column=columna,row=fila)
                    columna=columna+1
                    lista_num[fila].append(casilla)
                    print(casilla)
        columna=0
        fila=fila+1
    
    
def matriz_espacios():#funcion que sirve para poder obtener una matriz que muestre el estado actual de la tabla
    global lista_num
    global valor
    global jugada
    
    n="."
    fila=0
    columna=0
    valor=[[],[],[],[],[],[],[],[],[]]
    
    for i in lista_num:#se analiza lista_num que posee 0, -1 y entrys
        for j in i:
            if j==-1 or j==0:#si son 0 o -1, se ponen en "valor"
                #valor[fila][columna]==j
                valor[fila].append(j)
                columna=columna+1
            if j!=-1 and j!=0:#si no son 0 o -1, quiere decir que son numeros clave o entrys
                if isinstance(j,str)==True and n in j:#se verifica si son strings y tienen un "." para ver si es un numero clave
                    valor[fila].append(j)#se agregar el numero clave
                #valor[fila][columna]==j.get()
##                    if len(j.get())>=2:
##                        j.config(bg="red")
##                    if len(j.get())==1:
##                        j.config(bg="white")
                    
                if not isinstance(j,str)==True and n not in j.get():#si no es string y no tiene ".", significa que es un entry
                
                    valor[fila].append(j.get())#se agrega el contenido que hay en el entry
                    h=j.get()
                    if h!='' and h!="":
                        if j not in jugada:
                            jugada.append(j)
        
                columna=columna+1
        columna=0
        fila=fila+1
    print(jugada)
    revision=[]
    e=''
    cont=0
    cont2=0
    for i in valor:
        if e not in i:
            cont=cont+1
        if e in i:
            cont2=cont2+1
    if cont2!=0:
        pass
    if cont==9:
        if nivel.get()=="Multinivel":
            answer=messagebox.askquestion("Aviso","Has logrado completar el juego, deseas continuar?")
            if answer=="yes" and nivel.get()=="Multinivel":#condicion para multinivel
                leer_archivo_partidas()
            else:
                messagebox.showinfo("Felicidades"," Has completado la tabla ")# se envia un aviso
            
    
    print(valor)
    return valor
def pasa_espacios():
    global valor
    pasa_espacios_aux(valor,0,casilla,0)

def pasa_espacios_aux(valor,cont,casilla,cont2):
    global lista
    #if valor[lista[cont][2]][[cont][3]]==casilla:
        
def borrar_jugada():
    global jugada
    global lista_jugada
    global contenido
    if len(jugada)==0:
        messagebox.showinfo("Aviso","No has ingresado ninguna jugada para borrar!!! >:v ")# se envia un aviso
    ultima=jugada[len(jugada)-1]
    lista_jugada.append(ultima)
    contenido.append(ultima.get())
    ultima.delete(0,END)
    jugada.remove(ultima)

def rehacer_jugada():
    global lista_jugada
    global contenido
    global jugada
    if len(lista_jugada)==0:
        messagebox.showinfo("Aviso","No hay ninguna por rehacer, ya que no se realizado ninguna!!!")# se envia un aviso
    lista_jugada[len(lista_jugada)-1].insert(0,contenido[len(contenido)-1])#se inserta la ultima jugada en su entry respectivo
    jugada.append(lista_jugada[len(lista_jugada)-1])
    contenido.pop()
    lista_jugada.remove(lista_jugada[len(lista_jugada)-1])

    
def pasa_valor():#funcion para verificar si se repiten numero en una misma columna o fila 
    global lista
    global valor
    global lista_num
    contenedor=[]#variavle para poder guardar los numero que se ingresan y verificar si ya estan
    for i in lista:#se recorre lista para sacar las especificaciones
        num_fila=i[2]-1
        num_columna=i[3]-1
        numero=i[1]
        cantidad_espacios=i[4]
        forma=i[0]
        if forma == 2:#si "forma " es 2, se recorre lista_num como una columna
            for e in range(num_fila+1, num_fila + cantidad_espacios+1):#recorremos la matriz "lista_num" en las partes que son entrys, basandonos en las indicaciones
                    valor_actual=lista_num[e][num_columna]#se asigna valor actual
                    
                
                    if not isinstance(valor_actual,str):#si no es un string, signica que es un entry
                        valor_actual.config(bg="white")#se declara su color para que cambia a su forma normal cuando el proceso termino
                        if valor_actual!=-1 and valor_actual!=0:#si no son -1 o 0, ya que estos no son entry y tampoco strings
                            if valor_actual.get() in contenedor:#se saca el contenido de valor_actual y si valor_actual esta en el contenedor, significa que se esta repetiendo numeros en la columna
                                if valor_actual.get()!="":
                                    valor_actual.config(bg="red")#se cambia el color del entry 
                                    messagebox.showinfo("Aviso","Este numero ya se encuentra en alguna parte de la columna")# se envia un aviso
                            else:#si no esta, se agrega en el contenedor
                                contenedor.append(valor_actual.get())
            contenedor=[]#se vacia el contenedor
                            
        if forma == 1:#si "forma" es 1, se recorre la lista_num como una fila
            for e in range(num_columna+1, num_columna + cantidad_espacios+1):#recorremos la matriz "lista_num" en las partes que son entrys, basandonos en las indicaciones
                    valor_actual=lista_num[num_fila][e]#se asigna un valor de la matriz a valor_actual
                    if not isinstance(valor_actual,str):#si no es un string, significa que puede ser un entry 
                        valor_actual.config(bg="white")#se configura el color del entry
                        if valor_actual!=-1 and valor_actual!=0:#si no es un 0 o -1, sucede esto:
                            if valor_actual.get() in contenedor:#si el valor obtenido de valor_actual ya esta en el contenedor sucede esto:
                                if valor_actual.get()!="":
                                    valor_actual.config(bg="red")#se cambia el color del entry
                                    messagebox.showinfo("Aviso","Este numero ya se encuentra en alguna parte de la fila")#se envia un aviso 
                            else:
                                contenedor.append(valor_actual.get())# si no esta, se agrega al contenedor
            contenedor=[]

def revisa_suma():# funcion que sirve para poder revisar si la suma de los digitos ingresados es igual que el numero clave
    global lista
    global valor
    global lista_num
    contenedor=[]
    result=0
    for i in lista:
        num_fila=i[2]-1
        num_columna=i[3]-1
        numero=i[1]
        cantidad_espacios=i[4]
        forma=i[0]
        if forma == 2:
            for e in range(num_fila+1, num_fila + cantidad_espacios+1):
                    valor_actual=lista_num[e][num_columna]
                    if not isinstance(valor_actual,str)==True:
                        valor_actual.config(bg="white")
                        if valor_actual!=-1 and valor_actual!=0:
                            if valor_actual.get()!="":
                                    contenedor.append(valor_actual.get())
            if len(contenedor)==cantidad_espacios:
                for j in contenedor:
                    result=result+float(j)
                if result!=numero:
                    valor_actual.config(bg="red")
                    messagebox.showinfo("Aviso","La suma no concuerda con el numero clave")
            result=0
            contenedor=[]
                            
        if forma == 1:
            for e in range(num_columna+1, num_columna + cantidad_espacios+1):
                    valor_actual=lista_num[num_fila][e]
                    valor_actual.config(bg="white")
                    if not isinstance(valor_actual,str)==True:
                        if valor_actual!=-1 and valor_actual!=0:
                                if valor_actual.get()!="":
                                    contenedor.append(valor_actual.get())
            if len(contenedor)==cantidad_espacios:
                for j in contenedor:
                    result=result+float(j)
                if result!=numero:
                    valor_actual.config(bg="red")
                    messagebox.showinfo("Aviso","La suma no concuerda con el numero clave")
            result=0
            contenedor=[]
    
        
def combinaciones(casilla):
    barra ="/"
    letra=","
    if barra in casilla:
        indice=casilla.find(",")
        space=casilla[indice+1]
        casilla=solo_numeros(casilla)
        combi=pruebas(int(space),int(casilla[0]))
        if letra in casilla:
            indice=casilla.find(",")
            space=casilla[indice+1]
        
            casilla=solo_numeros(casill)
            combi=pruebas(space,int(casilla[1]))
    else:
        indice=casilla.find(",")
        space=casilla[indice+1]        
        casilla=solo_numeros(casilla)
        combi=pruebas(int(space),int(casilla[0]))
        print(combi)
def solo_numeros(casilla):
    punto="."
    barra="/"
    
    if punto in casilla or barra in casilla:
        
        result = solo_numeros_aux(casilla,"",0,[],casilla)
        print(result)
        return result
        
    if punto not in casilla and barra not in casilla:
        return casilla
        

def solo_numeros_aux(casilla,result,cont,contenedor,casilla_copia):
    if len(casilla_copia)==cont:
        return contenedor
    if casilla[0].isdigit()==True:
        return solo_numeros_aux(casilla[1:],result+casilla[0],cont+1,contenedor,casilla_copia)
    if casilla[0].isdigit()==False:
        if result!="":
            return solo_numeros_aux(casilla[1:],"",cont+1,contenedor+[result],casilla_copia)
        else:
            return solo_numeros_aux(casilla[1:],"",cont+1,contenedor,casilla_copia)
def permutaciones(m,n):
    if m==2:
        return pares(n)
    else:
        return permutaciones_aux(m,n,[],0,pares(n))

def permutaciones_aux(m,n,lista,cont,ps):
    
    if cont>len(pares(n)):
        return []
    else:
         x = permutaciones_aux(m-1,ps[cont][0],cont+1,ps[1:])
         return [ps[cont][0]+x[cont][0]] + permutaciones_aux(m-1,ps[cont][0],cont+1,ps[1:])

##def pares(n):
##    return pares_aux(n,1)

def pares(n):
    lista=[]
    for i in range(n+1):
        lista.append([i,n-i])
    return lista
##    if cont>n:
##        return []
##    else:
##        return [[cont,n-cont]]+ pares_aux(n,cont+1)

def pruebas(m,n):
    
    if m==2:
        return pares(n)
    else:
        par=[]
        ps=pares(n)
        for p in ps:
            xs = pruebas(m-1,p[1])
            for x in xs:
                par.append([p[0]] + x)
        return par
def configurar():#funcion que abre la ventana de configuracion
    global linea_horas
    global linea_minutos
    global linea_segundos
    global reloj
    global seg,minu,hor
    global nivel
    seg=StringVar()
    minu=StringVar()
    hor=StringVar()
    configuracion= Tk()#se crea una ventana
    configuracion.title("configuracion")
    configuracion.geometry("750x550")#Se define el tamaño del menu
    configuracion.resizable(0,0)#se redimensiona la ventana
    configuracion.configure(background="green2")#se pone un color a la ventana

    Label(configuracion,text="Configuracion", fg="black", bg="green2", font="Arial 22").place(x=280,y=10)
    Label(configuracion,text="Tiempo", fg="black", bg="green2", font="Arial 16").place(x=150,y=50)
    Label(configuracion,text="Horas", fg="black", bg="green2", font="Arial 12").place(x=90,y=80)
    Label(configuracion,text="Minutos", fg="black", bg="green2", font="Arial 12").place(x=165,y=80)
    Label(configuracion,text="Segundos", fg="black", bg="green2", font="Arial 12").place(x=255,y=80)
    #se ponen entry para definir el tiempo que se quiere poner en un timer
    linea_horas=Entry(configuracion, textvariable=hor, width=2, font="Arial 27", justify="center")
    linea_horas.place(x=90,y=115)
    linea_minutos=Entry(configuracion, textvariable=minu,width=2, font="Arial 27", justify="center")
    linea_minutos.place(x=170,y=115)
    linea_segundos=Entry(configuracion, textvariable=seg,width=2, font="Arial 27", justify="center")
    linea_segundos.place(x=260,y=115)
    #opciones del reloj
    Label(configuracion,text="Reloj", fg="black", bg="green2", font="Arial 16").place(x=100,y=260)
    reloj=ttk.Combobox(configuracion)#se crea una lista desplegable 
    reloj.place(x=80, y = 300)
    reloj["values"]=["Si","No","Timer"]
    #opciones de los diferentes niveles
    Label(configuracion, text="Nivel", fg="black", bg="green2", font="Arial 16").place(x=500,y=260)
    nivel=ttk.Combobox(configuracion)#se crea una lista desplegable 
    nivel.place(x=460, y = 300)
    nivel["values"]=["1 Neurona","2 Neuronas","3 Neuronas","Multinivel"]
    


def cronometro():
    global et_horas, et_minutos, et_segundos
    global segundos
    global minutos
    global horas
    segundos=0
    minutos=0
    horas=0
    et_horas=Label(kakuro,bg="#FFFFFF",text=horas, fg="#CF4647", font="verdana 7", width=8)
    et_horas. place(x=50, y=680)
    et_minutos=Label(kakuro,bg="#FFFFFF",text=minutos, fg="#CF4647", font="verdana 7", width=8)
    et_minutos. place(x=120, y=680)
    et_segundos=Label(kakuro,bg="#FFFFFF",text=segundos, fg="#CF4647", font="verdana 7", width=8)
    et_segundos. place(x=190, y=680)
    while True:
        segundos=segundos+1
        et_segundos.configure(text=segundos)
        et_segundos.update()
        
        if segundos>=60:
            segundos=0
            minutos=minutos+1
            et_minutos.configure(text=minutos)
            et_segundos.configure(text=segundos)
            et_segundos.update()
            et_minutos.update()
            
            if minutos>=60:
                minutos=0
                horas=horas+1
                et_minutos.configure(text=minutos)
                et_horas.configure(text=horas)
                et_minutos.update()
                et_horas.update()
            
        time.sleep(1)
    return cronometro()
        
def hilo_tiempo():
    hilo=Thread(target=cronometro, args=())
    hilo.start()
    
def timer():
    global linea_horas
    global linea_minutos
    global linea_segundos
    global et_horas, et_minutos, et_segundos
    global horas, segundos, minutos
    global kakuro
    et_horas=Label(kakuro,bg="#FFFFFF",text=horas, fg="#CF4647", font="verdana 7", width=8)
    et_horas. place(x=50, y=680)
    et_minutos=Label(kakuro,bg="#FFFFFF",text=minutos, fg="#CF4647", font="verdana 7", width=8)
    et_minutos. place(x=120, y=680)
    et_segundos=Label(kakuro,bg="#FFFFFF",text=segundos, fg="#CF4647", font="verdana 7", width=8)
    et_segundos. place(x=190, y=680)
    et_segundos.configure(text=segundos)
    et_minutos.configure(text=minutos)
    et_horas.configure(text=horas)
    segundos=linea_segundos.get()
    segundos=int(segundos)
    minutos=linea_minutos.get()
    minutos=int(minutos)
    horas=linea_horas.get()
    horas=int(horas)
    while True:
        segundos=segundos-1
        et_segundos.configure(text=segundos)
        et_segundos.update()
        if segundos==0 and minutos==0 and segundos==0:
            answer=messagebox.askquestion("Aviso","Se acaba de terminar el tiempo ¿Desea continuar?")
            if answer=="yes":
                segundos=linea_segundos.get()
                segundos=int(segundos)
                minutos=linea_minutos.get()
                minutos=int(minutos)
                horas=linea_horas.get()
                horas=int(horas)
            if answer=="no":
                kakuro.destroy()
        if segundos==0 and minutos!=0:
            segundos=59
            minutos=minutos-1
            et_minutos.configure(text=minutos)
            et_segundos.configure(text=segundos)
            et_segundos.update()
            et_minutos.update()
            if minutos==0 and horas!=0:
                minutos=59
                et_minutos.configure(text=minutos)
                et_horas.configure(text=horas)
                et_minutos.update()
            if minutos==0 and horas==0:
                minutos=0
                segundos=59
                if horas!=0:
                    horas=horas-1
                    et_horas.configure(text=horas)
                et_horas.update()
        
        time.sleep(1)
    return timer()

def hilo_timer():
    hilo=Thread(target=timer, args=())
    hilo.start()
    
def guardar():#funcion para sacar una ventana para confirmar si se quiere guardar el juego
    global ventana_guardar
    ventana_guardar= Tk()#se crea una ventana
    ventana_guardar.title("Guardar")#se define un titulo
    ventana_guardar.geometry("400x300")#se define tamaño
    ventana_guardar.resizable(0,0)#se redimenciona
    ventana_guardar.configure(background="gray")#se define color de fondo

    Label(ventana_guardar, text="¿Desea guardar el juego?", fg="black", bg="gold", font="Arial 18").place(x=40,y=40)

    boton_si=Button(ventana_guardar,text="Si", fg="black", bg="gold", font="Arial 12", padx=10, pady=8, command=si_guardar).place(x=80,y=130)
    boton_no=Button(ventana_guardar,text="No", fg="black", bg="gold", font="Arial 12", padx=8, pady=8, command=no_guardar).place(x=240,y=130)

def no_guardar():#funcion por si se escoge que no se quiere guardar la partida
    global kakuro
    ventana_guardar.destroy()#se destruye la ventana de confirmacion
    kakuro.destroy()#se destruye la ventana kakuro
    
def si_guardar():#funcion por si se quiere guardar la partida
    global valor
    global lista
    global ventana_guardar
    f=open("kakuro2018juegoactual","w")#se abre el archivo y se pone "w", es decir, que se quiere escribir
    f.write(str(valor))#se escribe los datos como string
    f.close()#se cierra el documento
    h=open("lista_matriz", "w")#se abre un documento aparte que va a guardar la lista que se uso para esta partida
    h.write(str(lista))#se escribe la lista
    h.close()# se cierra el documente
    ventana_guardar.destroy()#se destruye la ventana de confirmacion
    
def cargar_partida():#funcion que sirve para cargar una partida guardada
    global lista
    f=open("kakuro2018juegoactual","r")#se abre el archivo en modo de lectura
    lineas=f.readlines()#se crean una variable que representa la lectura de lineas
    lineas=eval(lineas[0])#se quitan los strings
    #lista=eval(lineas[1])
    #print(lista)
    entry_lineas(lineas)#se llama una funcion para crear la tabla de la partida guardada
    f.close()# se cierra el documento
    g=open("lista_matriz", "r")#se llama al archivo que guardo la tupla que tenia las especificaciones de esa partida en estructura
    lista=g.readlines()#se crea  una variable que representa la lectura de lineas del archivo
    lista=eval(lista[0])#se quitan strings
    
    g.close()#se cierra el archivo
    lista=eval(lista[0])
    
def entry_lineas(matriz):#funcion para crear la tabla de la partida guardada
    global marco
    global linea_texto
    global string
    global x
    global lista_num
    global lista
    global matrizInterfaz #se crea una matriz
    matrizInterfaz=[[-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1]]
    n="."
    fila=0
    columna=0
    lista_num=[[],[],[],[],[],[],[],[],[]]#
    variable = StringVar()
    for i in matriz:#se recorre la matriz 
        for casilla in i:
            if casilla==-1:#si aparece un -1, significa que se tiene que agregar un entry bloqueado, que funcione como relleno
                Entry(marco, width=2, font="Arial 27", justify="center",bg="red", state="disabled").grid(column=columna,row=fila)
                columna=columna+1
                lista_num[fila].append(-1)
            if casilla=='':#si es un string vacio, es un entry normal
                string= StringVar()
                matrizInterfaz[fila][columna] = string
                x = Entry(marco, textvariable = string , width=2, font="Arial 27", justify="center")
                x.grid(column=columna,row=fila)
                x.bind('<Button-1>', (lambda x = x: callback(x)))
                
                valor_casilla=x.get()
                
                lista_num[fila].append(x)
                columna=columna+1
        
            if  casilla!=-1 and casilla!='':#si no es un -1 o un string vacio, sucede esto:
                if n not in casilla:#si no tiene un ".", significa que es un entry que anteriormente tenia un digito
                    string = StringVar()
                    matrizInterfaz[fila][columna] = string
                    x=Entry(marco,width=2,textvariable=string,bg="white",fg="black", state="normal",font="Arial 27", justify="center")
                    x.bind('<Button-1>', (lambda x = x: callback(x)))
                    x.grid(column=columna,row=fila)
                    x.insert(0,casilla)
                    lista_num[fila].append(x)
                    columna=columna+1
        
                
            if n in casilla:#si tiene un ".", osea n, significa que es un label con el numero clave
                variable=casilla
                matrizInterfaz[fila][columna] = str(variable)
                variable_real=matrizInterfaz[fila][columna]            
                x=Button(marco,text=casilla,bg="azure",fg="black",width=2, font="Arial 10", padx=10, pady=9, command=lambda  variable=variable: combinaciones(str(variable)))
                x.grid(column=columna,row=fila)
                columna=columna+1
                lista_num[fila].append(casilla)
                print(casilla)
        columna=0
        fila=fila+1

def borrar_juego():#funcion que abre una ventana para confirmar si se quiere borrar la partida
    global ventana_borrar_juego
    ventana_borrar_juego= Tk()#se crea una ventana
    ventana_borrar_juego.title("Guardar")#se define un titulo
    ventana_borrar_juego.geometry("400x300")#se define tamaño
    ventana_borrar_juego.resizable(0,0)#se redimenciona
    ventana_borrar_juego.configure(background="gray")

    Label(ventana_borrar_juego, text="¿Desea guardar el juego?", fg="black", bg="gold", font="Arial 18").place(x=40,y=40)

    boton_si=Button(ventana_borrar_juego,text="Si", fg="black", bg="gold", font="Arial 12", padx=10, pady=8, command=borrar_si).place(x=80,y=130)
    boton_no=Button(ventana_borrar_juego,text="No", fg="black", bg="gold", font="Arial 12", padx=8, pady=8, command=borrar_no).place(x=240,y=130)

def borrar_si():#funcion del boton_si que es para borrar la partida
    global lista
    global ventana_borrar_juego
    celdas(lista)#se crea la misma tabla pero reseteada
    ventana_borrar_juego.destroy()#se destruye la ventana de confirmacion
    
def borrar_no():#funcion de boton "no", que destruye la ventana de confirmacion para poder seguir con la partida actual
    global ventana_borrar_juego
    ventana_borrar_juego.destroy()

def terminar_juego():#funcion que crea una ventana de confirmacion para saber si se quiere terminar el juego
    global ventana_terminar
    ventana_terminar= Tk()#se crea una ventana
    ventana_terminar.title("Guardar")#se define un titulo
    ventana_terminar.geometry("400x300")#se define tamaño
    ventana_terminar.resizable(0,0)#se redimenciona
    ventana_terminar.configure(background="gray")

    Label(ventana_terminar, text="¿Desea terminar el juego?", fg="black", bg="gold", font="Arial 18").place(x=40,y=40)

    boton_si=Button(ventana_terminar,text="Si", fg="black", bg="gold", font="Arial 12", padx=10, pady=8, command=terminar_si).place(x=80,y=130)
    boton_no=Button(ventana_terminar,text="No", fg="black", bg="gold", font="Arial 12", padx=8, pady=8, command=terminar_no).place(x=240,y=130)


def terminar_no():#funcion por si no se quiere terminar el juego
    global ventana_terminar
    ventana_terminar.destroy()#destruye la ventana de confirmacion

def terminar_si():#funcion por si se quiere terminar el juego
    global lista
    global nivel
    global partida
    lista_actual=random.choice(partida)#se saca una lista con especificacion de un nuevo tablera de kakuro random de "partida"
    while lista==lista_actual:#mientras que las variables sean iguales se sigue sacando una lista random
        lista_actual=random.choice(partida)#se hace esto para poder sacar una partida diferente
    lista=lista_actual#se pone que lista es igual a la nueva lista, osea lista_actual
    ventana_terminar.destroy()#se destruye la ventana de confirmacion
    celdas(lista)#se forma el tablero nuevo
    
##def top10():
##    global texto_nombre
##    global horas, segundos, minutos
##    #nombre=StringVar()
##    #texto_nombre=Entry(kakuro, textvariable=nombre, font="Arial 10", width=30).place(x=470,y= 620)
##    print(horas)
##    name=texto_nombre.get()
##    print(name)
##    horas=eval(horas)*3600
##    minutos=eval(minutos)*60
##    segundos_total=horas+minutos+eval(segundos)
##    f=open("kakuro2018top10","w")
##    f.write(name,str(segundos_total))
##    f.close()
            
def acerca_de():#funcion con los detalles del programa
    info= Tk()#se crea una ventana
    info.title("Acerca del programa")#se define un titulo
    info.geometry("800x500")#se define tamaño
    info.resizable(0,0)#se redimenciona
    info.configure(background="gold")#se define color de fondo
    #se hace un texto con el titulo de la pagina
    Label(info, text= "Acerca del programa:",fg="black",bg="gold", font=("Arial",18), padx=8, bd=6).place(x=290,y=90)
    #se hace un texto con el nombre del programa
    Label(info, text= "Nombre del programa: Kakuro",fg="black",bg="gold", font=("Arial",18), padx=8, bd=6).place(x=200,y=160)
    #se hace un texto del numero de version
    Label(info, text= "Version: 2.0",fg="black",bg="gold", font=("Arial",18), padx=8, bd=6).place(x=330,y=230)
    #se hace un texto de la fecha de creacion
    Label(info, text= "Fecha de creacion: 4 de Mayo del 2018",fg="black",bg="gold", font=("Arial",18), padx=8, bd=6).place(x=185,y=300)
    #se hace un texto del nombre del autor
    Label(info, text= "Autor: Jimmy Mok Zheng",fg="black",bg="gold", font=("Arial",18), padx=8, bd=6).place(x=260,y=370)

def manual():#se usa "startfile" para abrir el archivo
    os.startfile("manual_de_usuario_kakuro.pdf")
    
def ventana_salir():#funcion para abrir una ventana de confirmacion de salida
    global ventana_salir#se declaran variables globales
    global menu_principal
    global kakuro
    ventana_salir= Tk()#se crea la ventana
    ventana_salir.title("Salir")
    ventana_salir.geometry("380x200")#se define tamaaño
    ventana_salir.configure(background='LightSteelBlue1')#se define color

    Label(ventana_salir, fg="yellow2",text="¿Seguro que quiere salir?", background="black",font="Arial 18", padx=16,pady=6, bd=4).place(x=40,y=50)#se pone un texto de pregunta 
    boton_si= Button(ventana_salir, padx=16,pady=6, bd=4, text="Si",  fg= "black", background= "yellow2", command=salir)#se crea el boton "si" para salir del menu_principal
    boton_si.place(x=70, y=130)

    boton_no= Button(ventana_salir, padx=16,pady=6, bd=4, text="No",  fg= "black", background= "yellow2", command=salir_ventana_salir)#se crea el boton "no" para salir solo de la ventana salir
    boton_no.place(x=200, y=130)

def salir():#funcion para salir del menu principal
    global kakuro
    menu_principal.destroy()#se destruye el menu principal y la ventana de salir y todas las ventanas abiertas
    ventana_salir.destroy()
    kakuro.destroy()
    acerca_de.destroy()
    
def salir_ventana_salir():#se define una funcion solo para destruir la ventana de salir
    ventana_salir.destroy()
menu()#se pone esto para poder abrir el menu principla de una vez, al probar el programa




    
   
        
        
            

