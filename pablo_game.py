import pygame
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

    def kepfajl(self):
        szinek = {"kőr": "hearts", "káró": "diamonds", "treff": "clubs", "pikk": "spades"}
        figurak = {"ász": "A", "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07", "8": "08", "9": "09", "10": "10", "bubi": "J", "dáma": "Q", "király": "K"}

        if self.figura == "joker":
            return "kepek/card_joker_red.png"
        else:
            angol_szin = szinek[self.szin]
            angol_figura = figurak[self.figura]
            return "kepek/card_" + angol_szin + "_" + angol_figura + ".png"
        
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

pygame.init()

SZELESSEG = 800
MAGASSAG = 500
ablak = pygame.display.set_mode((SZELESSEG, MAGASSAG))
pygame.display.set_caption("Pablo")

ora = pygame.time.Clock()

pakli = Pakli()
pakli.kever()
en = Jatekos("zsigi")
for i in range(4):
    en.kap(pakli.huz())

hatlap_kep = pygame.image.load("kepek/card_back.png")
hatlap_kep = pygame.transform.scale(hatlap_kep, (96, 96))

fut = True
felforditott = None
felforditas_ideje = 0
nezes_maradt = 2
dobopakli = []
allapot = "nezes"
huzott = None
while fut:
    for esemeny in pygame.event.get():
        if esemeny.type == pygame.QUIT:
            fut = False
        elif esemeny.type == pygame.KEYDOWN and esemeny.key == pygame.K_ESCAPE:
            fut = False
        elif esemeny.type == pygame.MOUSEBUTTONDOWN:
            if allapot == "nezes":
                kattintott = None
                for i in range(len(en.lapok)):
                    x = 172 + i * 120
                    terulet = pygame.Rect(x, 374, 96, 96)
                    if terulet.collidepoint(esemeny.pos):
                        kattintott = i
                        break

                if kattintott == felforditott:
                    felforditott = None
                elif kattintott != None and felforditott == None and nezes_maradt > 0 and en.ismert[kattintott] == False:
                    felforditott = kattintott
                    felforditas_ideje = pygame.time.get_ticks()
                    nezes_maradt -= 1
                    en.megnez(kattintott)
                else:
                    felforditott = None
            elif allapot == "huzas":
                pakli_terulet = pygame.Rect(292, 202, 96, 96)
                if pakli_terulet.collidepoint(esemeny.pos):
                    huzott = pakli.huz()
                    allapot = "dontes"
            elif allapot =="dontes":
                kattintott = None
                for i in range(len(en.lapok)):
                    x = 172 + i * 120
                    terulet = pygame.Rect(x, 374, 96, 96)
                    if terulet.collidepoint(esemeny.pos):
                        kattintott = i
                        break

                dobo_terulet = pygame.Rect(412, 202, 96, 96)

                if kattintott != None:
                    regi = en.csere(kattintott, huzott)
                    dobopakli.append(regi)
                    huzott = None
                    allapot = "huzas"
                elif dobo_terulet.collidepoint(esemeny.pos):
                    dobopakli.append(huzott)
                    huzott = None
                    allapot = "huzas"


    

    if felforditott != None and pygame.time.get_ticks() - felforditas_ideje > 10000:
        felforditott = None

    if allapot == "nezes" and nezes_maradt == 0 and felforditott == None:
        allapot = "huzas"

    ablak.fill((20, 100, 50))

    for i in range(len(en.lapok)):
        x = 172 + i * 120
        if i == felforditott:
            kep = pygame.image.load(en.lapok[i].kepfajl())
            kep = pygame.transform.scale(kep, (96, 96))
        else:
            kep = hatlap_kep
        ablak.blit(kep, (x, 374))

    if not pakli.ures():
        ablak.blit(hatlap_kep, (292, 202))

    if len(dobopakli) > 0:
        felso = dobopakli[-1]
        kep = pygame.image.load(felso.kepfajl())
        kep = pygame.transform.scale(kep, (96, 96))
        ablak.blit(kep, (412, 202))
    else:
        pygame.draw.rect(ablak, (255, 255, 255), pygame.Rect(412, 202, 96, 96), 2)

    if huzott!= None:
        kep = pygame.image.load(huzott.kepfajl())
        kep = pygame.transform.scale(kep, (96, 96))
        ablak.blit(kep, (560, 202))

    pygame.display.flip()
    ora.tick(60)

pygame.quit()