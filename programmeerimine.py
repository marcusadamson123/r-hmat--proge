# ---------------------------------------------------------
# Projekt: Kudumismustri skeemigeneraator
# Autorid: Marcus Adamson ja Mia Grossthal
# Kursus: Programmeerimine (LTAT.03.001)
# Kirjeldus: Programm võtab sisendiks kudumismustri teksti
# ja genereerib skeemi pildi, kus kasutatakse kudumismustrite tingmärke.
# Kasutatud teegid: tkinter, Pillow, re
# Eeskuju: PEP 8 ja PEP 257 dokumentatsioon ja ...........
# ---------------------------------------------------------

# ------------- Impordid -------------------------------------
import re  # avaldised
import tkinter as tk  # Pythoni GUI teek
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageGrab  # pildi loomised ja joonistamised
from tkinter import filedialog, messagebox  # Tkinteri teegi dialoogid ja seal toimetamised

# ----------------------------------------------------------
# ------------- UI stiilid ------------------
TAUST = "#f5f3e9"        # beež taust
RAAM = "#e6e2d1"         # tumedam taust
KAST = "#ffffff"         # valge taust kastidele
TEKST = "#403c2f"        # pruunikas tekst
NUPP_BG = "#dfdbca"      # nuppude taust
NUPP_BG2 = "#cbc6b5"     # hover värv

# ------------------------ Sümbolid -------------------------
sumbolid = {
    "pp": "□",    # parempidine silmus
    "ph": "▪",    # pahempidine silmus
    "õs": "○",    # õhksilmus
    "2kp": "//",  # kaks kokku paremale kallutatud
    "2kv": "\\",  # kaks kokku vasakule kallutatud
    "2kph": "⌃",  # pahempidi 2 kokku kootud
    "3pp": "△",   # 3 kokku parempidi
    "3ph": "▼",   # 3 kokku pahempidi
    "0": "▨",     # tühi koht (pole silmust)
    "p_e": "⌓",   # palmik 2x2 ette
    "p_t": "⌒",   # palmik 2x2 taha
    "n": "⊙",     # *pp, õs* 3-4 korda
}

# ----------------------------------------------------------
# ----------------------- Mõõtmed ----------------------------
CELL = 48           # ühe ruudu suurus pikslites laius = kõrgus
PAD = 72            # ääre suurus pildi ümber padding
GRID_W = 1          # ruudustiku joone paksus
FONT = ImageFont.truetype("consola.ttf", 28)
LINE_NUM_W = 56     # ruum rea numbrite jaoks vasakul ja paremal

# ----------------------------------------------------------------
# --------------------- Funktsioonid ------------------------------


# Funktsioon, mis avab eraldi akna kudumissümbolite lühendite muutmiseks
def muuda_luhendeid():
    # Loob uue alamakna
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
    aken.geometry("1100x800")
    aken.configure(bg=TAUST)

    # Tervitustekst
    tervitus = tk.Label(
        aken,
        text="🧶 Kudumismustri skeemigeneraator 🧶",
        font=("Arial", 20, "bold"),
        bg=TAUST,
        fg=TEKST
    )
    tervitus.pack(pady=10)

    # Vasak raam (sisendi jaoks)
    vasak_raam = tk.Frame(aken, bg=RAAM, bd=2, relief="ridge")
    vasak_raam.pack(side=tk.LEFT, fill=tk.BOTH, padx=12, pady=12)

    tk.Label(
        vasak_raam,
        text="Sisesta muster (üks rida = üks korda):",
        font=("Arial", 11, "bold"),
        bg=RAAM,
        fg=TEKST
    ).pack(anchor="w", pady=5)

    tekstikast = tk.Text(
        vasak_raam,
        width=48,
        height=24,
        font=("Consolas", 12),
        bg=KAST,
        fg=TEKST
    )
    tekstikast.pack(fill=tk.BOTH, expand=True, pady=5)

    tekstikast.insert(
        "1.0",
        "Rida 1: pp ph pp ph pp\n"
        "Rida 2: ph pp ph pp ph\n"
        "Rida 3: ph ph ph ph pp\n"
        "Rida 4: pp pp ph ph pp\n"
    )
    # Reaalajas muutumine
    tekstikast.bind("<<Modified>>", lambda e: realajas_uuenda(skeem, tekstikast))

    # Nupud paneel
    nupud = tk.Frame(vasak_raam, bg=RAAM)
    nupud.pack(fill=tk.X, pady=8)

    # Nupu stiil
    def uus_nupp(parent, tekst, käsk):
        n = tk.Button(
            parent,
            text=tekst,
            command=käsk,
            font=("Arial", 11, "bold"),
            bg=NUPP_BG,
            fg=TEKST,
            activebackground=NUPP_BG2,
            relief="raised",
            bd=2,
            padx=8,
            pady=4
        )
        n.pack(side=tk.LEFT, padx=5)
        return n

    uus_nupp(nupud, "Salvesta PNG", lambda: salvesta_canvas_pildina(skeem))
    uus_nupp(
        nupud,
        "Abi",
        lambda: messagebox.showinfo(
            "Abi",
            "Sisesta muster ja klõpsa 'Genereeri skeem'.\n"
            "Üks rida = üks mustririda!"
        )
    )
    uus_nupp(nupud, "Muuda lühendeid", muuda_luhendeid)

    # Parem raam (skeem)
    parem_raam = tk.Frame(aken, bg=RAAM, bd=2, relief="ridge")
    parem_raam.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)

    # Vasak osa – skeem
    skeemi_raam = tk.Frame(parem_raam, bg=RAAM)
    skeemi_raam.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    global skeem
    skeem = tk.Canvas(skeemi_raam, bg="#fff9e0")  # heledam taust skeemile
    skeem.pack(fill=tk.BOTH, expand=True)

    # Parem osa – lühendite tabel
    luhendid_raam = tk.Frame(parem_raam, bg=RAAM, bd=2, relief="sunken")
    luhendid_raam.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    tk.Label(luhendid_raam, text="Sümbolid:", font=("Arial", 12, "bold"),
         bg=RAAM, fg=TEKST).pack(pady=5)

    # Iga sümboli rida tabelisse
    for l, s in sumbolid.items():
        tk.Label(luhendid_raam, text=f"{l}  =  {s}",
                 font=("Consolas", 12),
                 bg=RAAM, fg=TEKST).pack(anchor="w")

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


# Järjend järjenditest, et saaks mustrit genereerida skeemiks
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
        skeem_canvas.create_text(20, i * CELL + 65, text=f"{i + 1}", font=("Arial", 12))
        
def realajas_uuenda(skeem_canvas, tekstikast):
    if tekstikast.edit_modified():   # kontrolli kas muutus
        genereeri_skeem(skeem_canvas, tekstikast)
        tekstikast.edit_modified(False)  # eemalda "modified" märge


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ava_aken()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
# Algversiooni esitamise kommentaarid:
# Kuidas senine koostöö sujunud? Kuidas on rollid jagatud? 
    # Vastus: Seni on läinud koostöö hästi ja sujuvalt. Oleme pidevas suhtluses omavahel ja mõlemad tegeleme erinevate funktsioonide koostamisega.
# Kui palju aega projektile on kulunud?
    # Vastus: Projektile hetkel on kulunud meil mõlemal arvatavasti kokku kulunud ligikaudu 13 tundi, kuid ei ole tea täpselt, kuna pole seda mõõtnud.
# Millised on projektiga seoses edasised plaanid ja edasiarendused?
    # Vastus: Edasised plaanid on järgmised : 1) Kudumismustri andmebaasi tegemine, kus on kasutaja saab salvestada erinevaid mustreid 2) Reaalajas eelvaade, kus mustrid uuenduvad reaalajas, 3) Kasutajaliidese ilusamaks tegemine
# 4) Keeletugi 5) Sümbolite ja värvide kohandamine 6) Automaatne mustri kontroll. Need on praegused plaanid, mis võivad muutuda.

