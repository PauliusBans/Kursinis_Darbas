<p align="center"><font size="6"><strong>TETRIS<strong></font></p>
<p align="center"><font size="2"><strong>Autorius: Paulius Bansevičius Ef-24/2<strong></font></p>

# Tikslas
Šio kursinio darbo tikslas - parodyti pagrindinius OOP programavimo principus, naudoti _design patterns_, failų įrašymą bei skaitymą, _unit test_`ą.

Rezultatas - funkcionalus žaidimas, kuris imituoja klasikinį žaidimą "Tetris". Jam sukurti buvo naudojami _Python_ programavimo kalba ir _Pygame_. 

Pagrindinis žaidimo funkcionalumas:
* Paprašomas žaidėjo vardas.
* Krentančios figūruos (originalus pavadinimas - Tetromino).
* Figūros, pasiekusios žaidimo lauko apačią arba kitą figūrą, sustoja.
* Jei sustojusios figūros sudaro tiesią liniją, jos yra panaikinamos ir žaidėjui yra priskiriami taškai.
* Žaidimas yra begalinis, tačiau laikui bėgant greitėja ir užsipildžius visam žadimio laukui, žaidėjas pralaimi.
* Vardas ir taškai išsaugojami faile.

## Žaidimo įjungimas
Norint paleisti žaidimą, būtina turėti _Python_ ir _Pygame_

Žaidimą galima įjungti į terminalą parašius:
```
python filename.py
```
(originalus filename - tetris)

Taip pat žaidimas įsijungs atidarius .py failą ir paspaudus "_Run Python file_".

## Kaip naudotis programa
Paleidus programą:

* Įvedamas žaidėjo vardas.
* Žaidimas prasideda!
* Surenkama kiek įmanoma daugiau taškų.

Žaidimo kontrolės:

* ← - figūra judinama į kairę
* → - figūra judinama į dešinę
* ↑ - figūra pasukama 90° kampu
* ↓ - pagreitinamas figūros kritimas
* space - figūra iškart nukrenta

# Kriterijai
## Polymorphism
````python
rotated = tetrominoes.rotate(current_piece)
````
"rotate" yra iškviečiamas objektui "tetrominoes", tačiau tai gali būti bet kokia figūra.
## Abstraction
````python
def update_position(self, tetromino, x, y):
        self.screen = copy.deepcopy(self.static_screen)
        self.get_dxdy(tetromino, x, y)
        for i in range(len(self.positions) // 2):
            dx = self.positions[i * 2]
            dy = self.positions[i * 2 + 1]
            if 0 <= dy < 20 and 0 <= dx < 10:
                tx = dx - x
                ty = dy - y
                if 0 <= ty < len(tetromino) and 0 <= tx < len(tetromino[0]):
                    self.screen[dy][dx] = tetromino[ty][tx]
````
Abstrakcija - kadangi keičiant figūros koordinates visada reikia žinoti jos dabartinę vietą, todėl metodas "get_dxdy" yra "paslėptas" metode "update_position". Iškviečiant metodą "update_position" nereikia prieš tai iškviesti "get_dxdy". Tai yra padaroma automatiškai.
## Inheritance
````python
class ColorChanger(Tetromino):
    def create_colored(self, number):
        shape = super().create(number)
        return [[number if cell else 0 for cell in row] for row in shape]

    def rotate(self, shape):
        return [list(row) for row in zip(*shape[::-1])]
````
Paveldėjimas - klasė "ColorChanger" iškviečia tėvinės klasės "Tetromino" metodą "create" ir prideda funkcionalumą - pakeičia figūros spalvą ir/arba ją pasuka.
## Encapsulation
````python
class GameStats:
    def __init__(self):
        self._score = 0
        self.level = 0
        self.lines_cleared = 0

    def update(self, cleared_lines):
        _score_table = [0, 100, 300, 500, 800]
        self._score += _score_table[cleared_lines] if cleared_lines < len(_score_table) else 1000
        self.lines_cleared += cleared_lines
        self.level = self.lines_cleared // 10

    def get_speed(self, base_speed):
        return max(100, base_speed - self.level * 40)
````
````python
def get_nickname():
    _nickname = ""
````
Enkapsuliacija - klasės atributas "score" ir metodo atributas "nickname" yra apsaugoti (_protected_).

````python
def create(self, number):
        return self.shapes.get(number, self._O)()

    def _O(self):
        return [[1, 1], [1, 1]]

    def _I(self):
        return [[1, 1, 1, 1]]

    def _T(self):
        return [[0, 1, 0], [1, 1, 1]]

    def _L(self):
        return [[1, 0], [1, 0], [1, 1]]

    def _J(self):
        return [[0, 1], [0, 1], [1, 1]]

    def _Z(self):
        return [[1, 1, 0], [0, 1, 1]]

    def _S(self):
        return [[0, 1, 1], [1, 1, 0]]
`````
Šiame pavyzdyje visų figūrų formos nėra tiesiogiai pasiekiamos. Tam yra naudojamas metodas "create".

# Design pattern
Šiame kursiniame darbe yra naudojamas tik vienas projektavimo šablonas - "factory":
````python
class Tetromino():
    def __init__(self):
        self.shapes = {
            1: self._O, 2: self._I, 3: self._T,
            4: self._L, 5: self._J, 6: self._Z, 7: self._S
        }

    def create(self, number):
        return self.shapes.get(number, self._O)()

    def _O(self): return [[1, 1], [1, 1]]
    def _I(self): return [[1, 1, 1, 1]]
    def _T(self): return [[0, 1, 0], [1, 1, 1]]
    def _L(self): return [[1, 0], [1, 0], [1, 1]]
    def _J(self): return [[0, 1], [0, 1], [1, 1]]
    def _Z(self): return [[1, 1, 0], [0, 1, 1]]
    def _S(self): return [[0, 1, 1], [1, 1, 0]]
````
Žaidėjas nenurodo, kaip konkreti figūra turėtų atrodyti – vietoj to, jis pateikia numerį, o klasė Tetromino pasirūpina tinkamos figūros logika. Toks sprendimas leidžia lengvai pridėti naujas figūras, spalvotas versijas (ColorChanger) ar pakeisti figūrų kūrimo mechanizmą nekeičiant pagrindinės žaidimo logikos.
# Composition
````python
class Field():
    def __init__(self):
        self.screen = [[0 for _ in range(10)] for _ in range(20)]
        self.static_screen = copy.deepcopy(self.screen)
        self.positions = []
        self.stats = GameStats() 
````
Kompozicija - objektas "stats" egzistuos tik tada, jei egzistuoja objektas pagal klasę "Field" 
# Reading/writing to a file
````python
with open("scores.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nickname, score])
````
Žaidėjui pralaimėjus į failą "scores.csv" yra įrašomas laikas, slaptyvardis ir jo taškai.

````python
try:
        with open("scores.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3:
                    try:
                        past_score = int(row[2])
                        if past_score > highscore:
                            highscore = past_score
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
````
Failas "scores.csv" yra nuskenuojamas : ieškoma, ar žaidėjas dabartiniame žaidime surinko daugiausiai taškų palyginus su senesniais bandymais.


## Pagrindiniai iššūkiai
* Iškilo sunkumų randant geriausią variantą, kaip išsaugoti žaidimo lauką. Dabartinėje implementacijoje visas žaidimas egzistuoja 2D _list_'e, tad galima žaisti ir be "Pygame" atspausdinant viską terminale. "0" - tai tuščia vieta, o bet koks kitas skaičius - figūra (skirtingi skaičiai - tai nuoroda Pygame, kokią spalvą priskirti). Pradinėje implementacijoje viskas buvo daroma tik su Pygame (t.y. žaidimas egzistavo tik Pygame lange). Tai sudarė daug nereikalingų sunkumų išsaugant stacionarias figūras ir randant, kada krentančią figūrą reikia sustabdyti.

Pavyzdys, kaip žaidimas atrodo terminale:
````
[0, 0, 0, 0, 0, 2, 2, 2, 2, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 3, 0, 0, 0]
[0, 0, 0, 0, 0, 3, 3, 3, 0, 0]
[0, 0, 0, 0, 0, 4, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 4, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 4, 4, 0, 0, 0]
[0, 0, 0, 0, 0, 4, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 4, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 4, 4, 0, 0, 0]
````

Čia matyti 3 apačioje nukritusios figūros viena ant kitos - 2 L formos ir 1 T formos. Taip pat matoma ir krentanti I figūra viršuje.

* Figūrų pasukimas, kai jos yra šalia žaidimo lauko ribų (ypač "I" figūra). Jų tiesioginis pasukimas yra nelegalus, kadangi tada figūra egzistuotų už žaidimo lauko ribų. Tam buvo implementuotas _kick offsets_ funkcionalumas - figūra pastumiama į šoną tiek kartų, kol jos pozicija tampa legali (žaidimo ribose)

* Gebėjimas figūrą pastumti į šoną, kai ji yra nusileidus. Ankstensė "Tetris" versija iškart užfiksuodavo figūrą kai ji nusileidžia. Tai sukėlė sunkumų figūrą pastumiant į _overhang_'us. Dabartinėje implementacijoje yra palaukiama kelis momentus kol figūra galutinai padaroma stacionaria.

# Rezultatai
* Šio darbo metu buvo sukurta pilnai veikianti „Tetris“ tipo žaidimo programa, parašyta naudojant _Python_ ir _Pygame_. Darbe buvo taikomi pagrindiniai objektinio programavimo principai – enkapsuliacija, paveldėjimas ir tam tikrose vietose – polimorfizmas, o taip pat pritaikytas Factory (gamyklos) dizaino šablonas, skirtas tetromino figūrų generavimui.

* Ateityje būtų galima pridėti muziką, garso efektus, main menu, įvairius žaidimo rėžimus.


