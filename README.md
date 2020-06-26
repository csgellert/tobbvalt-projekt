# Többvált-projekt
A Többváltozós analízis mérnöki alkalmazásai tárgyhoz készült projekt feladat.

## Maga a projekt:
A projekt célja hogy a snake nevű játékot evolúciós algoritmus segítségével tanítsuk be, hogy egy neurális háló alapján magától is tudja játszani a játékot.
A játék szabályai:
* A játék célja minnél több almát (/ahogyan a kódban hívjuk "kaját") elfogyasztani és ezáltal minél több pontot szerezni.
* Ha a kígyó önmagának vagy a falnak ütközik, meghal.
* Ha a kígyó megeszik egy almát a hossza megnő.

A projekthez hozzáadtunk egy függvényt aminek segítségével le lehet menteni a program (evol osztály) állapotát, így nem kell minden futtatásnál újrakezdeni a háló betanítását, folytathatjuk onnan ahol abbahagytuk, vagy akár csak külön az eredmény is megtekinthető, anélkül hogy a hosszabb betanítási folyamatot is végig kellene várni.

## Az evolúciós algoritmus

A mesterséges intelligencia fejlesztésének különböző típusai közül az evolúciós megközelítést választottuk, aminek a működése a következőképpen történik.
1. Kezdeti állapotban létrehozunk egy kígyó populációt, amelyeknek a DNS-ét alkotó súlymátrixokat (**kigyo.weights**) random számokkal feltöltjük. A kezdő létszámot a globalis.py fájlban lehet változtatni. (A gyors futási sebesség érdekében mi 100 kígyóval kísérleteztünk)
2. Mindegyik kígyóval lejátszunk egy meccset és kiszámítjuk az elért eredményüket, azaz a **fitness-t**.
3. Az evol. algoritmus lényege, hogy a biológiai evolúcióhoz hasonlóan nagyobb esélyt adunk a jobb kígyóknak, hogy a "génjeiket" örököltethessék. A **select** függvény segítségével kiválasztunk két kígyót.
4. A két kiválasztott kígyó génjeit keresztezzük a **crossover** fgv-nyel, így létrejön egy a szülőktől különböző "gyerek" kígyó.
5. Esélyt adunk a gének véletlenszerű változásának, azaz mutációjának a **mutate** fgv-nyel.
6. A (3)-(5) pontokat addig ismételjük, amíg a következő generációhoz elég gyerek kígyó létre nem jön.
7. Létrehozunk egy új **evol** osztálypéldányt, amiben eltároljuk a gyerek kígyókat.

A (2)-(6) lépések ciklikus ismételgetésével egyre ügyesebb kígyók jönnek létre. Az elérhető maximális "intelligenciájuk" a neurális háló felépítése és a bemenő adatok mennyisége mellett az előbb felsorolt függvények kifinomultságától függ.

## A projekt felépítése:

A projekt során a futtatandó fájl a snake.py fájl. A játékhoz szükséges egyéb fájlokat az osztalyok mappába raktuk, egy python csomagba rendezve őket.
A játék megjelenítéséhez a "pygame" nevű csomagot használtuk fel. A "GAME" mappában megtalálható a "Snake" emberi felhasználó által játszható változata is.

### global.py

Ez a fájl tartalmazza golbális változókat, az evolúciós algoritmus hiperparamétereit, valamint a megjelenítéshez szükséges függvényeket.

### kigyo.py

A kigyo.py -ban található kigyo objektum tartalmazza egy darab példány adatait. Ezek a példányok "játszák" a játékot, versengenek az evolúció során. Minden példány egy egyedi DNS-sel rendelkezik, amiket a weights adattagban tárolunk. A neurális háló struktúrája egyértelműen meghatározza a DNS alakját.

### evol.py

Ez a fájl tartalmazza az evol osztályt, valamint a futáshoz szükséges egyéb függvényeket.

#### evol osztály
Ebben az osztályban vannak az evolúciós algoritmus függvényei (**select**,**crossover**,**mutate**), emellett osztálypéldányonként az **evol.peldanyok** tömbben tároljuk az egy-egy generációt alkotó egyedeket. Szintén ebben az osztályban található a döntéshozó rendszer is "**network()**", amely az aktuális bemenetek függvényében egy neurális háló segítségével eldönti hogy az adott példány milyen irányba fog továbbmenni.

#### fitness()
Az evolúciós AI legfontosabb függvénye, mivel az általa megállapított eredmény alapján rangsorolódnak a kígyók a kiválasztáskor. Tehát ezzel tudjuk beállítani, hogy milyen tulajdonságok részesüljenek előnyben. Úgy találtuk, hogy ha megevett almák száma: "**score**", a megtett lépések száma: "**steps**", akkor `2^score * steps` eredményezte a legügyesebb kígyókat kis **score** esetén. Ötnél több megevett alma esetén `2^score + step + (2^5 * steps)`.

#### select()
Két módszert próbáltunk ki, a sima rulettkerekeset, és a dupla oldalú rulettet. 
* Az elsőnél egy listába, azaz a rulett kerékre minden kígyóból annyit rakunk, amennyi **fitness-t** elért. (Ha **kritFit** felettit, akkor **kritÉrt**-szer többet rakunk fel belőle.) Ezután addig pörgetünk, amíg két különböző kígyót ki nem választunk.
* A második csak annyiban különbözik, hogy egyszer pörgetünk, és a szerencsés kígyóval együtt a rulettkeréken pont ellentétes oldalon lévőt is kiválasztjuk.

Végül az elsőt alkalmaztuk a könnyebb kezelhetőség a hibák könyebb azonosíthatósága érdekében.

#### crossover()
A két kiválasztott kígyó DNS-ét alkotó mátrixokat egysorossá lapítjuk (np.matrix.flatten()), majd mindkettőt ugyanazon a véletlenszerűen kiválasztott helyen elmetsszük. Az egyik DNS első részét összefűzzük a másik DNS második részével, így keletkezik a gyerek kígyó DNS-e.

#### mutate()
A gyerek kígyó DNS-nek összes elemén végigmegyünk, és **mutRate** valószínűséggel megváltoztatjuk egy véletlenszerű értékre 0 és 1 között. Ezzel biztosítjuk a diverzitást, és a fejlődésre való képességet. A **mutRate** értékének kiválasztása tapasztalati úton történt, későbbiekben még ki szeretnénk próbálni úgy is, hogy dinamikusan változik, mert jelenleg könnyedén elrontja a jó kígyókat, viszont esetenként meg túl alacsonynak bizonyul.

#### newgen()
Ez a függvény hozza létre az új generációt tartalmazó evol tipusú objektumot.

#### train()
Ezen függvény segítségével lehet betanítani az kígyókat. Megadható számú új generációt hoz létre.

#### save és load függvény
Ezek segítségével tudunk elmenteni és betölteni AI generációkat, így onnan tudjuk folytatni a taníttatást ahol legutóbb abbahagytuk. Ha nem találja a betöltendő fájlt, akkor egy kezdeti populációt hoz létre. A fájlokat a "Mentett" mappában tároljuk ".pkl" kiterjesztéssel.

## Konklúzió

A projektünket sikeresnek könyveljük el, mivel el tudtuk készíteni magát a "Snake" játékot, ami önmagában is megfelelt volna a tárgy által elvárt projekt kritériumainak. Ezen felül sikerült olyan Mesterséges Intelligencia által vezérelt kígyókat készítenünk, amelyek akár 8-10 almát is megettek. Természetesen még nagyon sok mindent lehetne javítani a programon, főleg a **fitness** függvényen, de a mostani állapotában már teljesíti a mesterséges intelligenciához fűzödő elvárásainkat, így leadásra késznek nyilvánítjuk.
