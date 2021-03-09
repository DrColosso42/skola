from tkinter import *
import tkinter.filedialog
import csv

class Aplikacija:

    def __init__(self,root):
        self.root = root
        self.root.title("Proizvod GUI")
        self.proizvodi = {}
        self.racun = {}

        self.poslednji_red=4
        self.create_gui()
        self.azuriraj_listbox()

    def create_gui(self):


        Label(root,text="Izaberite proizvod:").grid(row=0,column=0,columnspan=4,pady=20)

        self.magacinListBox = Listbox(root,height=5,width=30)
        self.magacinListBox.bind("<<ListboxSelect>>",self.listbox_callback)

        self.magacinListBox.grid(row=1,column=0,columnspan=2,rowspan=2,padx=10)

        self.racunKolicina = Spinbox(root,from_=0,to_=999)
        self.racunKolicina.grid(row=1,column=2,padx=10)

        self.cenaLabel = Label(root,text="Cena: ")
        self.cenaLabel.grid(row=1,column=3)

        Button(root,text="Dodaj Aktivni Proizvod u Racun",command=self.dodaj_racun).grid(row=2,column=2,columnspan=2)

        Label(root,text="Racun:").grid(row=3,column=0,columnspan=3,pady=20)

        Button(root,text="Napravi Prodaju",command=self.napravi_prodaju).grid(row=3,column=3,rowspan=5,padx=10)

    def listbox_callback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.trenutni_proizvod = event.widget.get(index)
        
        self.cenaLabel.config(text=f"Cena: {self.proizvodi[self.trenutni_proizvod]}")
    

    def azuriraj_listbox(self):
        self.magacinListBox.delete(0,END)
        with open('cenovnik.csv', 'r') as cenovnik_csv:
            cenovnik = csv.reader(cenovnik_csv)

            next(cenovnik)
            
            for line in cenovnik:
                self.proizvodi[line[0]] = line[1]

        for proizvod in self.proizvodi.keys():
            self.magacinListBox.insert(0,f"{proizvod}")
        

    def dodaj_racun(self):
        
        kolicina = int(self.racunKolicina.get())
        cena = int(self.proizvodi[self.trenutni_proizvod])

        self.racun[self.trenutni_proizvod] = [kolicina,cena*kolicina]

        Label(root,text=f"Proizvod: {self.trenutni_proizvod.capitalize()}; Kolicina: {kolicina}; Cena: {kolicina*cena} ").grid(row=self.poslednji_red,column=0,columnspan=3)
        self.poslednji_red +=1
        
    def napravi_prodaju(self):
        fajl = tkinter.filedialog.asksaveasfilename()

        racun_lista = ['-------------------------- Racun --------------------------']
        cena = 0

        for proizvod in self.racun.keys():
            racun_lista.append(f"Ime proizvoda: {proizvod}, Kolicina: {self.racun[proizvod][0]}, Cena: {self.racun[proizvod][1]}")

            cena += int(self.racun[proizvod][1])
        
        racun_lista.append(f"-------------------- Ukupna cena: {cena} --------------------")


        with open(fajl,'w') as f:
            f.write('\n'.join(racun_lista))
        
        self.racun = {}
        self.azuriraj_listbox()
            

        
        
        

if __name__ == '__main__':
    root = Tk()
    Aplikacija(root)
    root.mainloop()
