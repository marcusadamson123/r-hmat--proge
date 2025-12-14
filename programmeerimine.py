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
# Võtmeks on kasutaja lühend, väärtuses nii kirjeldus kui sümbol
sumbolid = {
    "pp": {"nimi": "Parempidine silmus", "symbol": "□"},
    "ph": {"nimi": "Pahempidine silmus", "symbol": "▪"},
    "õs": {"nimi": "Õhksilmus", "symbol": "○"},
    "2kp": {"nimi": "2 kokku paremale", "symbol": "//"},
    "2kv": {"nimi": "2 kokku vasakule", "symbol": "\\"},
    "2kph": {"nimi": "2 kokku pahempidi", "symbol": "⌃"},
    "3pp": {"nimi": "3 kokku parempidi", "symbol": "△"},
    "3ph": {"nimi": "3 kokku pahempidi", "symbol": "▼"},
    "0": {"nimi": "Silmust pole", "symbol": "▨"},
    "p_e": {"nimi": "Palmik 2x2 ette", "symbol": "⌓"},
    "p_t": {"nimi": "Palmik 2x2 taha", "symbol": "⌒"},
    "n": {"nimi": "Nupp", "symbol": "⊙"},
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
    aken = tk.Toplevel()
    aken.title("Muuda sümboleid")
    aken.geometry("520x500")

    tk.Label(aken, text="Muuda lühendit, nimetust ja sümbolit",
             font=("Arial", 13, "bold")).pack(pady=10)

    sisestused = {}

    for luhend, andmed in sumbolid.items():
        rida = tk.Frame(aken)
        rida.pack(fill="x", padx=10, pady=4)

        tk.Label(rida, text="Lühend:", width=8).pack(side="left")
        e_luhend = tk.Entry(rida, width=8)
        e_luhend.insert(0, luhend)
        e_luhend.pack(side="left")

        tk.Label(rida, text="Nimi:", width=8).pack(side="left")
        e_nimi = tk.Entry(rida, width=22)
        e_nimi.insert(0, andmed["nimi"])
        e_nimi.pack(side="left")

        tk.Label(rida, text="Sümbol:", width=8).pack(side="left")
        e_sym = tk.Entry(rida, width=6)
        e_sym.insert(0, andmed["symbol"])
        e_sym.pack(side="left")

        sisestused[luhend] = (e_luhend, e_nimi, e_sym)

    # Sisemine funktsioon, mis läheb lahti nupuvajutusega ja salvestab mustrid
    def salvesta():
        global sumbolid
        uus = {}

        for vana, (e_l, e_n, e_s) in sisestused.items():
            uus_l = e_l.get().strip()
            uus_n = e_n.get().strip()
            uus_s = e_s.get().strip()

            if not uus_l or not uus_s:
                messagebox.showerror("Viga", "Lühend ja sümbol ei tohi olla tühjad!")
                return

            uus[uus_l] = {
                "nimi": uus_n,
                "symbol": uus_s
            }

        sumbolid = uus
        uuenda_luhendite_tabel()
        messagebox.showinfo("Valmis", "Sümbolid uuendatud!")
        aken.destroy()

    tk.Button(aken, text="Salvesta", command=salvesta,
              font=("Arial", 11, "bold")).pack(pady=12)
    
# Uuendab lühendite tabelit, kui kasutaja on neid muutnud
def uuenda_luhendite_tabel():
    for widget in luhendid_raam.winfo_children():
        widget.destroy()

    tk.Label(
        luhendid_raam,
        text="Sümbolid:",
        font=("Arial", 12, "bold"),
        bg=RAAM,
        fg=TEKST
    ).pack(pady=5)

    for andmed in sumbolid.values():
        tk.Label(
            luhendid_raam,
            text=f"{andmed['nimi']}  =  {andmed['symbol']}",
            font=("Consolas", 12),
            bg=RAAM,
            fg=TEKST
        ).pack(anchor="w")


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
    global luhendid_raam
    luhendid_raam = tk.Frame(parem_raam, bg=RAAM, bd=2, relief="sunken")
    luhendid_raam.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    tk.Label(luhendid_raam, text="Sümbolid:", font=("Arial", 12, "bold"),
         bg=RAAM, fg=TEKST).pack(pady=5)

    # Iga sümboli rida tabelisse
    for andmed in sumbolid.values():
        tk.Label(
        luhendid_raam,
            text=f"{andmed['nimi']}  =  {andmed['symbol']}",
            font=("Consolas", 12),
            bg=RAAM,
            fg=TEKST
        ).pack(anchor="w")

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
            sumbol = sumbolid.get(luhend, {}).get("symbol", luhend)

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