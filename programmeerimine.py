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
    "pp": "parempidine",    # parempidine silmus □
    "ph": "pahempidine",    # pahempidine silmus ▪
    "õs": "õhksilmus",      # õhksilmus ○
    "2kp": "2kokku_paremale",  # kaks kokku paremale kallutatud /
    "2kv": "2kokku_vasakule",  # kaks kokku vasakule kallutatud \
    "2kph": "2kokku_pahempidi", # pahempidi 2 kokku kootud ⌃
    "3pp": "3parempidi_kokku", # 3 kokku parempidi △
    "3ph": "3pahempidi_kokku", # 3 kokku pahempidi ▼
    "0": "pole_silmust",       # tühi koht (pole silmust) ▨
    "p_e": "palmik_ette",       # palmik 2x2 ette ⌓
    "p_t": "palmik_taha",       # palmik 2x2 taha ⌒
    "n": "nupp", # *pp, õs* 3-4 korda ⊙
   
}
#----------------------------------------------------------
#-----------------------Mõõtmed----------------------------
CELL = 48           # ühe ruudu suurus pikslites laius = kõrgus
PAD = 72            # ääre suurus pildi ümber padding
GRID_W = 1          # ruudustiku joone paksus
FONT = ImageFont.truetype("consola.ttf", 28)
LINE_NUM_W = 56     # ruum rea numbrite jaoks vasakul ja paremal
#----------------------------------------------------------------
#---------------------Funktsioonid-------------------------------------------------------------------------------------------------------------------------------------------------------------
def muuda_luhendeid():
    luhendite_aken = tk.Toplevel()
    luhendite_aken.title("Muuda lühendeid")
    luhendite_aken.geometry("400x400")

    tk.Label(luhendite_aken, text="Muuda lühendeid:", font=("Arial", 12)).pack(pady=10)
    sisestusvaljad = {}

    for luhend in list(sumbolid.keys()):
        rida = tk.Frame(luhendite_aken)
        rida.pack(fill="x", pady=2, padx=10)

        tk.Label(rida, text=sumbolid[luhend], width=18, anchor="w").pack(side="left")

        sisestus = tk.Entry(rida)  
        sisestus.insert(0, luhend)
        sisestus.pack(side="left", fill="x", expand=True)

        sisestusvaljad[luhend] = sisestus

    def salvesta():
        global sumbolid
        uued_sumbolid = {}
        for vana_luhend, sisestus in sisestusvaljad.items():
            uus_luhend = sisestus.get().strip()
            uued_sumbolid[uus_luhend] = sumbolid[vana_luhend]
        sumbolid = uued_sumbolid
        messagebox.showinfo("Salvestatud", "Lühendid muudetud!")
        luhendite_aken.destroy()

    tk.Button(luhendite_aken, text="Salvesta", command=salvesta).pack(pady=12)
   
def ava_aken():
    aken = tk.Tk()
    aken.title("Kudumismustri skeemigeneraator")
    tervitus = tk.Label(aken, text="Genereeri oma skeem")
    tervitus.pack()
    aken.geometry("1100x800")

    vasak_raam = tk.Frame(aken)
    vasak_raam.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=12, pady=12)

    tk.Label(vasak_raam, text="Sisesta muster (üks rida = üks korda):").pack(anchor="w")

    tekstikast = tk.Text(vasak_raam, width=48, height=24)
    tekstikast.pack(fill=tk.BOTH, expand=True)

    tekstikast.insert(
        "1.0",
        "Rida 1: p v p v p\n"
        "Rida 2: v p v p v\n"
        "Rida 3: v v v v p\n"
        "Rida 4: p p v v p\n"
    )

    nupud = tk.Frame(vasak_raam)
    nupud.pack(fill=tk.X, pady=8)

    tk.Button(nupud, text="Genereeri skeem",
              command=lambda: messagebox.showinfo("Salvesta", "Siin tuleks skeem salvestada")).pack(side=tk.LEFT, padx=8)

    tk.Button(nupud, text="Salvesta PNG",
              command=lambda: messagebox.showinfo("Salvesta", "Siin tuleks skeem salvestada")).pack(side=tk.LEFT, padx=8)

    tk.Button(nupud, text="Abi",
              command=lambda: messagebox.showinfo("Abi", "See on abitekst")).pack(side=tk.LEFT, padx=8)

    tk.Button(nupud, text="Muuda lühendeid", command=muuda_luhendeid).pack(side=tk.LEFT, padx=8)

    parem_raam = tk.Frame(aken)
    parem_raam.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)

    skeem = tk.Canvas(parem_raam, bg="#ffffcc")
    skeem.pack(fill=tk.BOTH, expand=True)

    aken.mainloop()

    

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ava_aken()

