# ---------------------------------------------------------
# Projekt: Kudumismustri skeemigeneraator
# Autorid: Marcus Adamson ja Mia Grossthal
# Kursus: Programmeerimine (LTAT.03.001)
# Kirjeldus: Programm võtab sisendiks kudumismustri teksti
# ja genereerib skeemi pildi, kus kasutatakse kudumismustrite tingmärke.
# Kasutatud teegid: tkinter, Pillow, re
# Eeskuju: PEP 8 ja PEP 257 dokumentatsioon ja ...........
# ---------------------------------------------------------
#-------------Impordid-------------------------------------
import re  #avaldised                            
import tkinter as tk #Pythoni GUI teek                    
from PIL import Image, ImageDraw, ImageFont, ImageTk #pildi loomised ja joonistamised
from tkinter import filedialog, messagebox #Tkinteri teegi dialoogid ja seal toimetamised

#----------------------------------------------------------
#_------------------------Sümbolid-------------------------
sumbolid = {
    "p": "parempidine",    # parempidine silmus
    "v": "pahempidine",    # pahempidine silmus (v nagu "vasak", et lihtsam meelde jätta)
    "õ": "õhksilmus",      # õhksilmus
    "2kp": "2kokku_paremale",  # kaks kokku paremale kallutatud
    "2kv": "2kokku_vasakule",  # kaks kokku vasakule kallutatud
    "0": "pole_silmust",       # tühi koht (pole silmust)
    "p_e": "palmik_ette",       # palmik 2x2 ette
    "p_t": "palmik_taha",       # palmik 2x2 taha
   
}
#----------------------------------------------------------
#-----------------------Mõõtmed----------------------------
CELL = 48           # ühe ruudu suurus pikslites (laius = kõrgus)
PAD = 72            # ääre suurus pildi ümber (padding)
GRID_W = 1          # ruudustiku joone paksus
FONT = None         # siia laeme font-objekti hiljem
LINE_NUM_W = 56     # ruum rea numbrite jaoks vasakul ja paremal
#----------------------------------------------------------------
#---------------------Abitekst-----------------------------------
def ava_aken():
    #----------------------Akna suurus ja asjad---------------
    aken=tk.Tk()
    aken.title("Kudumismustri skeemigeneraator")
    greeting=tk.Label(aken, text="Genereeri oma skeem")
    greeting.pack()
    aken.geometry("1100x800")
    #-------------------------------------------------------

    #-------------------Tekstikast-----------------------------
    left=tk.Frame(aken)
    left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=12, pady=12)
    
    tk.Label(left, text="Sisesta muster (üks rida = üks koerida):").pack(anchor="w")
    
    text = tk.Text(left, width=48, height=24)
    text.pack(fill=tk.BOTH, expand=True)
    #---------------------------------------------------------------------------

    # ------------------kuidas peaks valja nagema see kirjutamine-----------
    text.insert(
        "1.0",
        "Rida 1: p v p v p\n"
        "Rida 2: v p v p v\n"
        "Rida 3: v v v v p\n"
        "Rida 4: p p v v p\n"
    )
    #-------------------------------------------------------
    #------------------------Nupud------------------------------
    nupp=tk.Frame(left)
    nupp.pack(fill=tk.X, pady=8)
    
    tk.Button(nupp, text="Genereeri skeem",
              command=lambda: messagebox.showinfo("Salvesta", "Siin tuleks skeem salvestada")).pack(side=tk.LEFT,padx=8)
    
    tk.Button(nupp, text="Salvesta PNG",
              command=lambda: messagebox.showinfo("Salvesta", "Siin tuleks skeem salvestada")).pack(side=tk.LEFT, padx=8)

    tk.Button(nupp, text="Abi",
              command=lambda: messagebox.showinfo("Abi", "See on abitekst")).pack(side=tk.LEFT)
    #--------------------------------------------------------------
    #------------------------Skeemi frame-------------------------
    right = tk.Frame(aken)
    right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)

    canvas = tk.Canvas(right, bg="#ffffcc")
    canvas.pack(fill=tk.BOTH, expand=True)
    #--------------------------------------------------------
    
    
    aken.mainloop()

    

#-----------------------------------------------------------------
ava_aken()
