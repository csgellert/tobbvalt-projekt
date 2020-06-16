from .globalis import *
from .kigyo import kigyo

#main. Külön megírva menő :D
def main():
    piton=kigyo() #mi más lenne a neve?
    pygame.init() #ez mindig kell, hogy a pygame függvényei és objektumai jól meghívódjanak

    #a szoveg kiiratás előkészítése különböző objektumokkal. Ez elég macerás, három lépcsős folyamat, de annyira nem is fontos a projekt szempontjából
    #szoveg: Game over
    szoveg=pygame.font.Font('freesansbold.ttf',32) 
    #pont: 'Pontok' felira
    pont=pygame.font.Font('freesansbold.ttf',16)
    szoveg1=szoveg.render('Game over!',True,KEK,PIROS)
    pont1=pont.render('Pontok:',True,KEK,PIROS)
    #pontszam: az aktuális pontszám (megevett kaják száma)
    pont2=pont1.get_rect()
    szoveg2=szoveg1.get_rect()
    pont2.center=(MERET/2, MERET-MERET/RACS/2)
    szoveg2.center=(MERET/2,MERET/2)
    
    while True: #game loop: mindig fut, ebben történnek az események, és itt frissül a képernyő
       
        display.fill(FEKETE) #minden ciklus elején töröljük a képernyő tartalmát
        #racsrajzol() #racs rajzolása. kikommentelve jobb a játékélmény szerintem :D
        határrajzol() #a határok megrajzolása
        mozgott=False #minden kör elején False
        key=pygame.key.get_pressed() #gombnyomás objektum (?)
        l=len(kigyo.snake) #a kígyó aktuális hossza

        for event in pygame.event.get(): #végigmegy a ciklus alatt történt összes eventen: event handling
            if event.type==QUIT: #ezt mindig bele kell írni, nem egészen tiszta, hogy mit csinál, mert nem ez léptet ki
                pygame.quit
                sys.exit
            #ha az event gomb lenyomása:
            if event.type==KEYDOWN:
                #ha a gomb a fel/le/jobbra/balra
                if event.key==K_UP and piton.utolso!=0 and piton.utolso!=2:
                    piton.move(0,mozgott)
                    
                elif event.key==K_RIGHT and piton.utolso!=1 and piton.utolso!=3:
                    piton.move(1,mozgott)
                    
                elif event.key==K_DOWN and piton.utolso!=2 and piton.utolso!=0:
                    piton.move(2,mozgott)
                    
                elif event.key==K_LEFT and piton.utolso!=3 and piton.utolso!=1:
                    piton.move(3,mozgott)
                #a tesztelés alatt az tűnt jobbnak a "játékélmény" szempontjából, ha ide van berakva a kirajzolás
                piton.kigyorajzol()
                piton.kajarajzol()
                #a szoveget rá kell másolni (blit) az ablakra
                pontszam1=pont.render(str(l-3),True,KEK,PIROS)
                pontszam2=pontszam1.get_rect()
                pontszam2.center=(MERET/2+40, MERET-MERET/RACS/2)
                display.blit(pont1,pont2)
                display.blit(pontszam1,pontszam2)
                #ez nagyon fontos: ez frissíti a kijelzőt minden ciklusban
                pygame.display.update()
                continue #ez hasznosnak tűnt
        if mozgott==False: #ha a kígyó még nem mozgott a ciklusban, akkor automatikusan mozog
            piton.move(piton.utolso,mozgott)
            piton.kigyorajzol()
            piton.kajarajzol()
            #ide is jobbnak tűnt berakni
            pontszam1=pont.render(str(l-3),True,KEK,PIROS)
            pontszam2=pontszam1.get_rect()
            pontszam2.center=(MERET/2+40, MERET-MERET/RACS/2)
            display.blit(pont1,pont2)
            display.blit(pontszam1,pontszam2)
            pygame.display.update()
        #ha a kígyó meghal, kilép a game loop-ból
        if piton.utkozike():
            isAlive=False
            break
        CLOCK.tick(FPS)#csak akkor megy továb, ha 1/FPS sec eltelt az előző hívás óta, ez a sebesség szabályozója
        #game loop vége

    #a játék vége: Game over kiírása, majd kilépés
    display.blit(szoveg1,szoveg2)
    pygame.display.update()
    CLOCK.tick(1)
    del piton
    pygame.quit()
    sys.exit
