# Lab 05 – Proceduralny Generator Lasu i Biomów (bpy)

## Co zostało zrealizowane
Zaimplementowałem proceduralny generator lasu w Blenderze przy użyciu API Pythona (`bpy`). Głównym celem ćwiczenia było przejście z twardo zakodowanej logiki tworzenia pojedynczego obiektu na elastyczny, oparty na danych system (podejście data-driven). 

Skonfigurowałem słownik parametrów dla trzech typów roślin (drzewo, krzew, paproć) oraz napisałem system biomów, który decyduje o rodzaju rośliny na podstawie jej odległości od centrum sceny (drzewa w środku, mniejsze rośliny na peryferiach). Dodatkowo zaimplementowałem system zarządzania sceną – skrypt automatycznie czyści starą geometrię i organizuje nowe obiekty w hierarchiczne kolekcje (Outliner). Całość oparta jest na ziarnie losowości (`seed`), co gwarantuje pełną odtwarzalność generowanego lasu.

## Uruchomienie
1. Otwórz program Blender.
2. Przejdź do zakładki **Scripting** na górnym pasku.
3. Utwórz nowy tekst (przycisk *New*), wklej kod ze skryptu `las.py`.
4. Uruchom skrypt klikając **Run Script** (lub skrótem `Alt + P`).
