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
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageGrab #pildi loomised ja joonistamised
from tkinter import filedialog, messagebox #Tkinteri teegi dialoogid ja seal toimetamised

#----------------------------------------------------------
#_------------------------Sümbolid-------------------------
sumbolid = {
    "pp": "□",    # parempidine silmus 
    "ph": "▪",    # pahempidine silmus 
    "õs": "○",      # õhksilmus 
    "2kp": "//",  # kaks kokku paremale kallutatud 
    "2kv": "\\",  # kaks kokku vasakule kallutatud 
    "2kph": "⌃", # pahempidi 2 kokku kootud 
    "3pp": "△", # 3 kokku parempidi 
    "3ph": "▼", # 3 kokku pahempidi 
    "0": "▨",       # tühi koht (pole silmust) 
    "p_e": "⌓",       # palmik 2x2 ette 
    "p_t": "⌒",       # palmik 2x2 taha 
    "n": "⊙", # *pp, õs* 3-4 korda 
   
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
# Funktsioon, mis avab eraldi akna kudumissümbolite lühendite muutmiseks
def muuda_luhendeid():
    #Loob uue alamakna
    luhendite_aken = tk.Toplevel()
    luhendite_aken.title("Muuda lühendeid")
    luhendite_aken.geometry("400x400")

    tk.Label(luhendite_aken, text="Muuda lühendeid:", font=("Arial", 12)).pack(pady=10)
    # Sõnastik, kuhu hiljem salvestatakse kasutaja sisestusväljad
    sisestusvaljad = {}

    for luhend in list(sumbolid.keys()):
        # Iga lühendi jaoks luuakse eraldi rida
        rida = tk.Frame(luhendite_aken)
        rida.pack(fill="x", pady=2, padx=10)
        # Vasakule kuvatakse vastava lühendi sümbol
        tk.Label(rida, text=sumbolid[luhend], width=18, anchor="w").pack(side="left")
        # Paremale lisatakse tekstiväli, kus kasutaja saab lühendit muuta
        sisestus = tk.Entry(rida)  
        sisestus.insert(0, luhend)
        sisestus.pack(side="left", fill="x", expand=True)

        sisestusvaljad[luhend] = sisestus
 # Sisemine funktsioon, mis läheb lahti nupuvajutusega ja salvestab mustrid
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
# Peamine funktsioon, mis loob ja kuvab kogu rakenduse akna
def ava_aken():
     # Põhiaken 
    aken = tk.Tk()
    aken.title("Kudumismustri skeemigeneraator")
    tervitus = tk.Label(aken, text="Genereeri oma skeem")
    tervitus.pack()
    aken.geometry("1100x800")
#Vasak pool (sisendi jaoks)
    vasak_raam = tk.Frame(aken)
    vasak_raam.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=12, pady=12)

    tk.Label(vasak_raam, text="Sisesta muster (üks rida = üks korda):").pack(anchor="w")

    tekstikast = tk.Text(vasak_raam, width=48, height=24)
    tekstikast.pack(fill=tk.BOTH, expand=True)
#Näidismuster, mis kuvatakse kohe avamisel
    tekstikast.insert(
        "1.0",
        "Rida 1: pp ph pp ph pp\n"
        "Rida 2: ph pp ph pp ph\n"
        "Rida 3: ph ph ph ph pp\n"
        "Rida 4: pp pp ph ph pp\n"
    )
 # Nuppude rida vasakul
    nupud = tk.Frame(vasak_raam)
    nupud.pack(fill=tk.X, pady=8)

    tk.Button(nupud, text="Genereeri skeem",
          command=lambda: genereeri_skeem(skeem, tekstikast)).pack(side=tk.LEFT, padx=8)
# Nupp skeemi salvestamiseks
    tk.Button(nupud, text="Salvesta PNG",
              command=lambda: salvesta_canvas_pildina(skeem)).pack(side=tk.LEFT, padx=8)
# Abiinfo nupp (selgitab kasutajale programmi kasutust
    tk.Button(nupud, text="Abi",
              command=lambda: messagebox.showinfo("Abi", "Sisesta oma muster kastikesse ning klõpsa 'genereeri skeem'. Igale reale kirjuta vaid 1 mustririda! \nEt lühendeid muuta vali menüüst 'muuda lühendeid'.")).pack(side=tk.LEFT, padx=8)
 # Nupp, mis avab muuda lühendeid akna
    tk.Button(nupud, text="Muuda lühendeid", command=muuda_luhendeid).pack(side=tk.LEFT, padx=8)
 # Parem raam, kuhu joonistatakse genereeritud skeem
    parem_raam = tk.Frame(aken)
    parem_raam.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)
# Canvas, kuhu hiljem kuvatakse kudumisskeem
    skeem = tk.Canvas(parem_raam, bg="#ffffcc")
    skeem.pack(fill=tk.BOTH, expand=True)

    aken.mainloop()
    
def salvesta_canvas_pildina(canvas):
    # Failinime küsimine
    failitee = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG failid", "*.png")],
        title="Salvesta skeem pildina"
    )
    if not failitee:
        return

    # Uuendab canvase
    canvas.update()

    # Ekraanipildi kommentaarid
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    # Teeb ekraanipildi
    pilt = ImageGrab.grab(bbox=(x, y, x1, y1))
    pilt.save(failitee)

    messagebox.showinfo("Salvestatud", f"Skeem salvestatud faili:\n{failitee} 😀 ")

    

#järjend järjenditest, et saaks mustrit genereerida skeemiks
def muster_listiks(tekst: str):
    read = []
    for rida in tekst.strip().splitlines():
        rida = rida.strip()
        if not rida:
            continue
        rida = re.sub(r"^[Rr]ida\s*\d+\s*[:\-]?\s*", "", rida)
        silmused = rida.split()
        read.append(silmused)
    return read

def genereeri_skeem(skeem_canvas, tekstikast):
    tekst = tekstikast.get("1.0", tk.END)
    muster = muster_listiks(tekst)
    
    skeem_canvas.delete("all")  # kustutab vana skeemi

    # arvutab skeemi mõõtmed
    read_arv = len(muster)
    if read_arv == 0:
        messagebox.showwarning("Tühi muster", "Sisesta muster enne genereerimist!")
        return
    
    veerud = max(len(rida) for rida in muster)

    # ruudustiku joonistamine
    for r in range(read_arv):
        for c in range(len(muster[r])):
            x1 = c * CELL + 40
            y1 = r * CELL + 40
            x2 = x1 + CELL
            y2 = y1 + CELL

            skeem_canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1)

            luhend = muster[r][c]
            sumbol = sumbolid.get(luhend, luhend)
            
            skeem_canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=sumbol,
                font=("Consolas", 14)
            )

    # ridade numbrid vasakule
    for i in range(read_arv):
        skeem_canvas.create_text(20, i * CELL + 65, text=f"{i+1}", font=("Arial", 12))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ava_aken()
