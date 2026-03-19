<img width="800" height="600" alt="rosliny_lab04" src="https://github.com/user-attachments/assets/2ea4e365-9811-414f-a769-038c62d93ab0" />

#  Lab 04 – Proceduralne generowanie roślin biomechanicznych (bpy)

W ramach tego zadania stworzyłem skrypt w języku Python wykorzystujący API Blendera (`bpy`) do proceduralnego generowania trójwymiarowych modeli w stylu biomechanicznym. Zamiast ręcznego modelowania w interfejsie graficznym, cała geometria, materiały i ustawienia sceny tworzone są w 100% z poziomu kodu.

---

##  Co zostało zrealizowane?

* **Podejście modułowe:** Główna, sparametryzowana funkcja `stworz_rosline()` wywołuje mniejsze funkcje pomocnicze (`stworz_lodyge()`, `stworz_liscie()`, `stworz_korzenie()`). Zapewnia to dużą czytelność i łatwość modyfikacji kodu.
* **Materiały proceduralne:** Rośliny posiadają wygenerowane materiały oparte na węźle *Principled BSDF* – charakteryzują się metaliczną łodygą oraz ciemnymi, lekko emitującymi światło liśćmi.
* **Automatyzacja sceny:** Skrypt wykonuje pełen cykl przygotowania do renderu:
    * Czyści obecną scenę ze zbędnych elementów.
    * Generuje trzy różniące się od siebie warianty roślin.
    * Ustawia kamerę oraz oświetlenie typu *SUN*.
    * Automatycznie renderuje całość do pliku `rosliny_lab04.png`.

---

##  Jak uruchomić?

Skrypt można uruchomić na dwa sposoby – bezpośrednio w programie lub w tle z poziomu terminala.

### Opcja 1: W interfejsie graficznym Blendera (GUI)
1. Otwórz program Blender.
2. Przejdź do przestrzeni roboczej **Scripting** (górny pasek zakładek).
3. Utwórz nowy tekst i wklej tam zawartość pliku `.py`.
4. Kliknij przycisk **Run Script** (lub użyj skrótu klawiszowego `Alt + P`).

### Opcja 2: Z poziomu wiersza poleceń (Headless mode)
Uruchomienie w tle (bez włączania interfejsu). Zakładając, że Blender jest dodany do zmiennych środowiskowych `PATH`, otwórz terminal i wpisz:

```bash
blender -b --python skrypt.py

