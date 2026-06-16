
## 1. Opis sceny
Animacja prezentuje ujęcie POV (z perspektywy pierwszej osoby) symulujące spacer wzdłuż opustoszałej miejskiej ulicy tuż po zmroku. Kamera płynnie rozgląda się po okolicy, rejestrując mokry asfalt, w którym odbijają się światła latarni oraz okoliczne budynki — m.in. szpital z wyraźnym, czerwonym neonem, stację benzynową w stylu retro oraz bank. Głównym elementem ożywiającym scenę są przejeżdżające pojazdy: najpierw ulicę pokonuje klasyczny muscle car (Ford Mustang) z charakterystycznymi pasami, a chwilę po nim przejeżdża radiowóz policyjny (Sheriff). Błyskające, niebiesko-czerwone światła radiowozu dynamicznie oświetlają otoczenie i odbijają się w mokrej nawierzchni oraz na elewacjach budynków.

Jaki nastrój/klimat chciałem osiągnąć:
Chciałem uzyskać mroczny, filmowy klimat rodem z thrillera akcji. Mokry asfalt, chłodne światła latarni i pulsujące "koguty" przejeżdżającego radiowozu budują napięcie, dając wrażenie trwającego nocnego pościgu lub policyjnej obławy na uciekiniera w opustoszałym mieście.

## 2. Instrukcja uruchomienia
1. Upewnij się, że posiadasz zainstalowany program **Blender w wersji 4.x** (lub nowszej).
2. Pobierz zawartość repozytorium (upewnij się, że pliki binarne pobrały się poprawnie przez Git LFS).
3. Otwórz plik sceny znajdujący się w ścieżce: `assets/scena.blend`.
4. Aby zainicjalizować system deszczu za pomocą skryptu:
   - Przejdź do zakładki **Scripting** w górnym menu Blendera.
   - Otwórz plik skryptu `src/animacja.py`.
   - Kliknij przycisk **Run Script** (ikona strzałki lub skrót `Alt + P`). W konsoli systemowej powinien pojawić się komunikat: *„Sukces: System deszczu został wygenerowany!”*.
5. Aby wyrenderować gotową animację:
   - Przejdź do zakładki **Output Properties** i sprawdź ścieżkę zapisu w sekcji *Output* (domyślnie `renders/`).
   - Z górnego paska menu wybierz `Render` -> `Render Animation` (lub użyj skrótu `Ctrl + F12`).

## 3. Opis skryptu Python (`animacja.py`)
Zaimplementowany skrypt automatyzuje proces tworzenia fizycznego i wizualnego systemu deszczu w programie Blender przy użyciu API `bpy`. 

**Główne etapy działania skryptu:**
1. **Tworzenie emitera:** Nad ulicą (na wysokości 15 jednostek) generowana jest płaszczyzna pełniąca rolę chmury, która zostaje ukryta w widoku viewportu oraz ostatecznym renderze.
2. **Konfiguracja fizyki:** Skrypt tworzy system cząsteczek, ustawiając ujemną klatkę startową (`frame_start = -50`), dzięki czemu deszcz pada już od pierwszej klatki animacji. Kropelki uzyskują wektor prędkości skierowany w dół oraz losowość ruchu.
3. **Model kropli:** Proceduralnie tworzony jest wydłużony walec służący jako obiekt referencyjny (`Instance Object`) dla cząsteczek. Skrypt automatycznie włącza rotację dopasowaną do wektora prędkości (`VEL`), aby krople spadały pionowo.
4. **Materiał wody:** Skrypt dynamicznie tworzy i przypisuje materiał oparty na węźle `Principled BSDF`. Posiada on niską szorstkość (`Roughness = 0.05`), pełną przezroczystość/załamianie światła (`Transmission Weight = 1.0`) oraz współczynnik załamania światła właściwy dla wody (`IOR = 1.33`), co pozwala na uzyskanie realistycznych refleksów świetlnych.

**Zmienne sterujące (parametryzacja na początku pliku):**
Przed uruchomieniem skryptu użytkownik może łatwo dostosować efekt za pomocą następujących zmiennych:
* `INTENSYWNOSC_DESZCZU` (domyślnie `15000`) — całkowita liczba generowanych cząsteczek deszczu.
* `PREDKOSC_OPADANIA` (domyślnie `20.0`) — startowa prędkość pionowa kropel (wpływa bezpośrednio na rozmycie w ruchu).
* `CZAS_TRWANIA_ANIMACJI` (domyślnie `250`) — klatka, na której system kończy emisję nowych kropel.
* `WIELKOSC_CHMURY` (domyślnie `30.0`) — szerokość i długość obszaru, nad którym generowane są opady.

## 4. Lista użytych assetów z zewnątrz

| Nazwa obiektu / Tekstury | Źródło | Licencja | Link / Uwagi |
| :--- | :--- | :--- | :--- |
| **Samochód: Police Car** | BlenderKit | Royalty Free | [Link do modelu](https://www.blenderkit.com/asset-gallery-detail/763449f0-7223-42d9-ac01-41aad01e6981/) |
| **Samochód: Mustang** | BlenderKit | Royalty Free | [Link do modelu](https://www.blenderkit.com/asset-gallery-detail/cd558b89-0331-4eb2-8124-53e5835da861/) |
| **Środowisko: Scena miasta** | BlenderKit | Royalty Free | [Link do modelu](https://www.blenderkit.com/asset-gallery-detail/a1600774-b49a-4590-82f8-f663047f5c8d/) |


## 5. Znane bugi i ograniczenia
* Ze względu na optymalizację wydajnościową renderowania, cząsteczki deszczu nie posiadają włączonej pełnej kolizji fizycznej ze skomplikowaną geometrią każdego dachu i krawędzi budynków (przelatują przez nie na wylot do poziomu ulicy).

