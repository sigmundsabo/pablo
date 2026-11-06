import random

class Lap:
    def __init__(self, szin, figura):
        self.szin = szin
        self.figura = figura

    def pontertek(self):
        if self.szin in ["kőr", "káró"] and self.figura == "király":
            return -1
        elif self.figura == "joker":
            return 2
        elif self.figura in ["bubi", "dáma", "király"]:
            return 10
        elif self.figura == "ász":
            return 1
        else:
            return int(self.figura)
        
class Pakli:
    def __init__(self):
        self.lap = []
        szinek = ["kőr", "káró", "treff", "pikk"]
        figurak = ["ász", "2", "3", "4", "5", "6", "7", "8", "9", "10", "bubi", "dáma", "király" ]
        
        for szin in szinek:
            for figura in figurak:
                self.lap.append(Lap(szin, figura))
        self.lap.append(Lap("joker", "joker"))
        self.lap.append(Lap("joker", "joker"))
   
    def kever(self):
        random.shuffle(self.lap)

    def huz(self):
        elso = self.lap.pop(0)
        return elso

    def ures(self):
        if len(self.lap) == 0:
            return True
        else:
            return False

class Jatekos:
    def __init__(self, nev):
        self.nev = nev
        self.lapok = []
        self.ismert = []

    def kap(self, lap):
        self.lapok.append(lap)
        self.ismert.append(False)

    def megnez(self, index):
        self.ismert[index] = True
        return self.lapok[index]

    def csere(self, index, uj_lap):
        regi_lap = self.lapok[index]
        self.lapok[index] = uj_lap
        self.ismert[index] = True
        return regi_lap

    def osszeg(self):
        osszesen = 0
        for lap in self.lapok:
            osszesen += lap.pontertek()
        return osszesen

class Jatek:
    def __init__(self):
        self.pakli = Pakli()
        self.pakli.kever()
        self.dobopakli = []
        nev1 = input("Első játékos neve: ")
        nev2 = input("Második játékos neve: ")
        self.jatekosok = [Jatekos(nev1), Jatekos(nev2)]

    def osztas(self):
        for jatekos in self.jatekosok:
            for i in range(4):
                jatekos.kap(self.pakli.huz())

    def huzas(self):
        if self.pakli.ures():
            print("Elfogyott a pakli, újrakeverés!")
            felso = self.dobopakli.pop()
            self.pakli.lap = self.dobopakli
            self.dobopakli = [felso]
            self.pakli.kever()
        return self.pakli.huz()

    def szam_bekeres(self, kerdes, maximum):
        while True:
            valasz = input(kerdes).strip()
            if valasz.isdigit() and 1 <= int(valasz) <= maximum:
                return int(valasz) - 1
            print("Rossz válasz! Írj egy számot 1 és", maximum, "között." )
    
    def kezdo_nezes(self):
        for jatekos in self.jatekosok:
            print(jatekos.nev + ", nézz meg 2 lapot!")
            db = len(jatekos.lapok)
            nezett = 0
            while nezett < 3:
                index = self.szam_bekeres("Melyik lapot nézed meg? (1-" + str(db) + "): ", db)
                if jatekos.ismert[index]:
                    print("Ezt a lapot már megnézted, válassz másikat!")
                else:
                    lap = jatekos.megnez(index)
                    print("Ez a lap:", lap.szin, lap.figura)
                    nezett += 1

    def kor(self, jatekos):
        print()
        print(jatekos.nev + " köre")
        db = len(jatekos.lapok)
        huzott = self.huzas()
        print("Húztál:", huzott.szin, huzott.figura)

        dontes = input("Cserélsz (c) vagy eldobod (e)? ").strip().lower()
        if dontes == "c":
            index = self.szam_bekeres("Melyik lapodra cseréled? (1-" + str(db) + "): ", db)
            eldobott = jatekos.csere(index, huzott)
        else:
            eldobott = huzott

        self.dobopakli.append(eldobott)
        print("Eldobtad:", eldobott.szin, eldobott.figura)
        self.kepesseg(jatekos, eldobott)

    def kepesseg(self, jatekos, lap):
        db = len(jatekos.lapok)
        if lap.figura == "8":
            print("8-as ! Megnézheted egy lapod.")
            index = self.szam_bekeres("Melyik lapod nézed meg? (1-" + str(db) + "): ", db)
            megnezett = jatekos.megnez(index)
            print("Ez a lap:", megnezett.szin, megnezett.figura)

        elif lap.figura == "9":
            print("9-es! Megnézheted az ellenfél lapját.")

            ellenfel = None
            for j in self.jatekosok:
                if j != jatekos:
                    ellenfel = j

            db = len(ellenfel.lapok)
            e_index = self.szam_bekeres(ellenfel.nev + " melyik lapját nézed meg? (1-" + str(db) + "): ", db)
            print("Ez a lap:", ellenfel.lapok[e_index].szin, ellenfel.lapok[e_index].figura)

            dontes = input("Kicseréled valamelyik lapodra? (i/n): ").strip().lower()
            if dontes == "i":
                db = len(jatekos.lapok)
                s_index = self.szam_bekeres("Melyik lapodra cseréled? (1-" + str(db) + "): ", db)

                atmeneti = ellenfel.lapok[e_index]
                ellenfel.lapok[e_index] = jatekos.lapok[s_index]
                jatekos.lapok[s_index] = atmeneti

                jatekos.ismert[s_index] = True
                ellenfel.ismert[e_index] = False
                print("Kicserélted!")


    def kiertekeles(self):
        print()
        print("=== LAPOK FELFORDÍTÁSA ===")

        gyoztes = None
        dontetlen = False
        for jatekos in self.jatekosok:
            print(jatekos.nev + " lapjai:")
            for lap in jatekos.lapok:
                print("   ", lap.szin, lap.figura)
            print("   Összesen:", jatekos.osszeg())

            if gyoztes == None:
                gyoztes = jatekos
            elif jatekos.osszeg() < gyoztes.osszeg():
                dontetlen = False
                gyoztes = jatekos
            elif jatekos.osszeg() == gyoztes.osszeg() and len(jatekos.lapok) < len(gyoztes.lapok):
                dontetlen = False
                gyoztes = jatekos
            elif jatekos.osszeg() == gyoztes.osszeg() and len(jatekos.lapok) == len(gyoztes.lapok):
                dontetlen = True

        print()
        if dontetlen:
            print("Döntetlen!")
        else:
            print("A győztes:", gyoztes.nev, "🏆")

    def jatszik(self):
        self.osztas()
        self.kezdo_nezes()

        pablozo = None
        while pablozo == None:
            for jatekos in self.jatekosok:
                self.kor(jatekos)
                dontes = input("Pablozol? (i/n): ").strip().lower()
                if dontes == "i":
                    pablozo = jatekos
                    print(jatekos.nev + " pablozott!")
                    break

        print()
        print("=== UTOLSÓ KÖR ===")
        for jatekos in self.jatekosok:
            if jatekos != pablozo:
                self.kor(jatekos)

        self.kiertekeles()
        print("A játék véget ért!")

jatek = Jatek()
jatek.jatszik()