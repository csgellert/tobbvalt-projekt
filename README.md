# Többvált-projekt
A Többváltozós analízis mérnöki alkalmazásai tárgyhoz készült projekt feladat.

## Maga a projekt:
A projekt célja hogy a snake nevű játékot evolúciós algoritmus segítségével tanítsuk be, hogy egy neurális háló alapján magától is tudja játszani a játékot.
A játék szabályai:
- A játék célja minnél több almát elfogyasztani és ezáltal minnél több pontot szerezni.
- Ha a kígyó önmagának vagy a falnak ütközik, meghal.
- Ha a kígyó megeszik egy almát a hossza megnő.

A projekthez hozzáadtunk egy funkciót aminek segítségével le lehet menteni a program (evol osztály) állapotát, így nem kell minden futtatásnál újrakezdeni a háló betanítását, folytathatjuk onnan ahol abbahagytuk, vagy akár csak külön az eredmény is megtekinthető, anélkül hogy a hosszabb betanítási folyamatot is végig kellene várni.

## Az evolúciós algoritmus
Ide még írni kéne valamit

## A projekt felépítése:

A projekt során a futtatandó fájl a snake.py fájl. A játékhoz szükséges egyéb fájlokat az osztalyok mappába raktuk, egy csomagba rendezve őket.

### kigyo.py

A kigyo.py -ban található kigyo objektum tartalmazza egy darab példány adatait. Ezek a példányok "játszák" a játékot, versengenek az evolúció során. Minden példány egy egyedi DNS-sel rendelkezik, amiket a weights adattagban tárolunk.

### evol.py

Ez a fájl tartalmazza az evol osztályt, valamint a futáshoz szükséges egyéb függvényeket.

#### evol osztály
Ez az osztály végzi az evolúciós algoritmust, egy generáció egyedeit tartalmazza. A példányok tömbben tároljuk az egyedeket, majd az osztály tagfüggvényeivel hajtunk végre rajtuk műveleteket. (Például játék, statisztikák, megjelenítés...) Szintén ebben az osztályban található a döntéshozó rendszer is, amely az aktuális bemenetek függvényében egy neurális háló segítségével eldönti hogy az adott példány milyen irányba fog továbbmenni. Ebben az osztályban találhatóak továbbá az új generáció létrehozásához szükséges szükséges függvények is. (Például a kiválasztáshoz, keresztezéshez, mutációhoz... szükséges függvények)

#### newgen függvény
Ez a függvény hozza létre az új generációt tartalmazó evol tipusú objektumot.

#### train függvény
EZ a függvény segítségével lehet betanítani a játékot. Megadható számú új generációt hoz létre.

#### load függvény
Ennek a segítségével tudjuk betölteni a korábbi állását a programnak, vagy ha nem találja a betöltendő fájlt, akkor egy kezdeti populációt hoz létre.

### global.py

Ez a fájl tartalmazza golbális változókat, az evolúciós algoritmus hiperparamétereit, valamint a megjelenítéshez szükséges függvényeket.

## Konklúzió

Ide is írni kéne még valamit...
