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
import re                             
import tkinter as tk                    
from PIL import Image, ImageDraw, ImageFont
#----------------------------------------------------------
#_------------------------Sümbolid-------------------------
SYMBOLS = {
   
}
#----------------------------------------------------------
