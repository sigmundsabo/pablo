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
def lap_kep(lap):
    kep = pygame.image.load(lap.kepfajl())
    kep = pygame.transform.scale(kep, (96, 96))
    return kep
pakli = Pakli()
pakli.kever()

en = Jatekos("zsigi")
for i in range(4):
    en.kap(pakli.huz())

bot = Jatekos("bot")
for i in range(4):
    bot.kap(pakli.huz())

bot.megnez(0)
bot.megnez(1)

hatlap_kep = pygame.image.load("kepek/card_back.png")
hatlap_kep = pygame.transform.scale(hatlap_kep, (96, 96))
fut = True
felforditott = None
felforditas_ideje = 0
nezes_maradt = 2
dobopakli = []
allapot = "nezes"
huzott = None
betu = pygame.font.SysFont("arial", 12)
bot_kezdete = None
pablozo = None
pablo_gomb = pygame.Rect(560, 210, 120, 36)
uzenetek = {
    "nezes": "Nézz meg 2 lapot! Kattints rájuk.",
    "huzas": "Húzz egy lapot a pakliból!",
    "dontes": "Cseréld ki a lapot, vagy dobd el!",
    "bot": "A bot gondolkodik...",
    "vege": "Vége a játéknak!",
    "nyolcas": "8-as! Kattints egy lapodra, és megnézheted.",
    "nyolcas_nez": "Jegyezd meg! Kattints, ha megvan."
}

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
                    terulet = pygame.Rect(x, 338, 96, 96)
                    if terulet.collidepoint(esemeny.pos):
                        kattintott = i
                        break

                #kukucskálás
                if kattintott == felforditott:
                    felforditott = None
                elif kattintott != None and nezes_maradt > 0 and en.ismert[kattintott] == False:
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
                    terulet = pygame.Rect(x, 338, 96, 96)
                    if terulet.collidepoint(esemeny.pos):
                        kattintott = i
                        break

                dobo_terulet = pygame.Rect(412, 202, 96, 96)

                #kattintás
                eldobott_lap = None
                if kattintott != None:
                    eldobott_lap = en.csere(kattintott, huzott)
                elif dobo_terulet.collidepoint(esemeny.pos):
                    eldobott_lap = huzott

                if eldobott_lap != None:
                    dobopakli.append(eldobott_lap)
                    huzott = None
                    if eldobott_lap.figura == "8":
                        allapot = "nyolcas"
                    else:
                        allapot = "bot"

    if felforditott != None and pygame.time.get_ticks() - felforditas_ideje > 10000:
        felforditott = None

    #bot
    if allapot == "bot":
        if pablozo == "bot":
            allapot = "vege"
        elif bot_kezdete == None:
            bot_kezdete = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - bot_kezdete > 2000:
            bot_huzott = pakli.huz()

            legrosszabb_index = None
            legrosszabb_ertek = -999
            for i in range(len(bot.lapok)):
                if bot.ismert[i] and bot.lapok[i].pontertek() > legrosszabb_ertek:
                    legrosszabb_index = i
                    legrosszabb_ertek = bot.lapok[i].pontertek()

            if legrosszabb_index != None and bot_huzott.pontertek() < legrosszabb_ertek:
                eldobott = bot.csere(legrosszabb_index, bot_huzott)
            else:
                eldobott = bot_huzott
            dobopakli.append(eldobott)

            if pablozo == None:
                becsult = 0
                for i in range(len(bot.lapok)):
                    if bot.ismert[i]:
                        becsult += bot.lapok[i].pontertek()
                    else:
                        becsult += 6
                if becsult <= 16:
                    pablozo = "bot"

            if pablozo == "en":
                allapot = "vege"
            else:
                allapot = "huzas"

            bot_kezdete = None
    #nyolcas
    elif allapot == "nyolcas":
        for i in range(len(en.lapok)):
            x = 172 +  i * 120
            terulet = pygame.Rect(x, 338, 96, 96)
            if terulet.collidepoint(esemeny.pos):
                felforditott = en.lapok[i]
                felforditas_ideje = pygame.time.get_ticks()
                en.megnez(i)
                allapot = "nyolcas_nez"
                break

    elif allapot == "nyolcas_nez":
        felforditott = None

    if allapot == "nezes" and nezes_maradt == 0 and felforditott == None:
        allapot = "huzas"

    #Rajzolás
    ablak.fill((20, 100, 50))

    for i in range(len(en.lapok)):
        x = 172 + i * 120
        if i == felforditott or allapot == "vege":
            kep = lap_kep(en.lapok[i])
        else:
            kep = hatlap_kep
        ablak.blit(kep, (x, 338))

    for i in range(len(bot.lapok)):
        x = 172 + i * 120
        if allapot == "vege":
            kep = lap_kep(bot.lapok[i])
        else:
            kep = hatlap_kep
        ablak.blit(kep, (x, 70))


    if not pakli.ures():
        ablak.blit(hatlap_kep, (292, 202))

    if len(dobopakli) > 0:
        felso = dobopakli[-1]
        kep = lap_kep(felso)
        ablak.blit(kep, (412, 202))
    else:
        pygame.draw.rect(ablak, (255, 255, 255), pygame.Rect(412, 202, 96, 96), 2)

    if huzott!= None:
        kep = lap_kep(huzott)
        ablak.blit(kep, (560, 202))

    felirat = betu.render(uzenetek[allapot], True, (255, 255, 255))
    ablak.blit(felirat, (20, 16))

    if allapot == "bot" and pablozo == None:    
        pygame.draw.rect(ablak, (200, 50, 50), pablo_gomb)
        felirat_p = betu.render("Pablo!", True, (255, 255, 255))
        ablak.blit(felirat_p, (pablo_gomb.x + 10, pablo_gomb.y + 8))

    if allapot == "nezes":
        szoveg = "Még " + str(nezes_maradt) + " lapot nézhetsz meg."
        felirat2 = betu.render(szoveg, True, (255, 255, 255))
        ablak.blit(felirat2, (20, 36))

    if allapot == "vege":
        en_ossz = en.osszeg()
        bot_ossz = bot.osszeg()

        if en_ossz < bot_ossz:
            eredmeny = "Nyertél!"
        elif en_ossz > bot_ossz:
            eredmeny = "A bot nyert!"
        elif len(en.lapok) < len(bot.lapok):
            eredmeny = "Nyertél! (kevesebb lappal)"
        elif len(en.lapok) > len(bot.lapok):
            eredmeny = "A bot nyert! (kevesebb lappal)"
        else:
            eredmeny = "Döntetlen!"

        szoveg = "Te: "+ str(en_ossz) + " pont | Bot: " + str(bot_ossz) + " pont"
        felirat3 = betu.render(szoveg, True, (255, 255, 255))
        ablak.blit(felirat3, (20, 36))
        felirat4 = betu.render( eredmeny, True, (255, 255, 255))
        ablak.blit(felirat4, (560, 210))

    if pablozo == "bot" and allapot != "vege":
        felirat5 = betu.render("A bot bemondta: PABLO! Ez az utolsó köröd.", True, (255, 255, 255))
        ablak.blit(felirat5, (20, 36))

    pygame.display.flip()
    ora.tick(60)

pygame.quit()