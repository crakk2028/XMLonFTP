from lxml import etree
from datetime import datetime
import random
import ftplib
from tkinter import *


def make_xml(file: str, date: datetime, compteur: int, rame: str):
    root = etree.Element("Comptage")

    num_rame = etree.Element("Num_Rame", titre="21")
    num_rame.text = rame1.get()
    root.append(num_rame)
    file_date = etree.SubElement(root, "Date")

    file_date.text = date
    file_counter = etree.SubElement(root, "Comptage")
    file_counter.text = compteur

    tree = etree.ElementTree(root)

    tree.write(xml_file, pretty_print=True, xml_declaration=True, encoding="utf-8")
    return True


def send_file_ftp(file: str):
    session = ftplib.FTP('SERVEUR', 'ID', 'MDP')
    file_ftp = open(file, 'rb')                     # file to send
    ftp_command = "STOR %s"%file                # FTP command
    session.storbinary(ftp_command, file_ftp)       # send the file
    file_ftp.close()                                # close file and FTP
    session.quit()


def new_seed():
    now = datetime.now()
    global date
    date = now.strftime("%m/%d/%Y, %H:%M")
    date1.config(text=date)
    global compteur
    compteur = str(random.randint(100, 2000))
    compteur1.config(text=compteur)


if __name__ == "__main__":
    # Configuration des variables
    xml_file = "Output.xml"
    now = datetime.now()
    date = now.strftime("%m/%d/%Y, %H:%M")
    compteur = str(random.randint(100, 2000))
    rame = "16A"

    top = Tk()
    L0 = Label(top, text="Logiciel de test compteur")
    L0.grid(row=0, column=0)

    L1 = Button(top, text="Nouvelle config", command=new_seed)
    L1.grid(row=0, column=1)

    #Rame
    rame0 = Label(top, text="Numéro de rame")
    rame0.grid(row=1, column=0)
    rame1 = Entry(top, bd=5, textvariable="%s"%rame)
    rame1.grid(row=1, column=1)

    #Date
    date0 = Label(top, text="Date :")
    date0.grid(row=2, column=0)
    date1 = Label(top, bd=5, text="%s"%date)
    date1.grid(row=2, column=1)

    #Compteur
    compteur0 = Label(top, text="Valeur de comptage : ")
    compteur0.grid(row=3, column=0)
    compteur1 = Label(top, bd=5, text="%s"%compteur)
    compteur1.grid(row=3, column=1)


    B = Button(top, text="Générer XML", command=lambda: make_xml(xml_file, date, compteur, rame))
    B.grid(row=4, column=0)

    B = Button(top, text="Envoyer XML", command=lambda: send_file_ftp(xml_file))
    B.grid(row=4, column=1)

    L1 = Label(top, text="")
    L1.grid(row=5, column=1)

    top.mainloop()
