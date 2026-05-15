import bpy
import math
import os

SCIEZKA_LAB07 = r"C:/Users\saumo\Documents\lab_07.blend"
NAZWA_KOLEKCJI = "Roslina_Hero"

KLATKA_START = 1
KLATKA_KONIEC = 125
FPS = 25

def wyczysc_animacje(obj):
    """Usuwa dane animacji, aby skrypt był idempotentny."""
    if obj and obj.animation_data and obj.animation_data.action:
        obj.animation_data.action = None

def importuj_rosline(sciezka_blend, nazwa_kolekcji):
    """Importuje kolekcję z zewnętrznego pliku .blend."""
    if not os.path.exists(sciezka_blend):
        print(f"BŁĄD: Plik {sciezka_blend} nie istnieje!")
        return False
        
    sciezka_kolekcji = os.path.join(sciezka_blend, "Collection", nazwa_kolekcji)
    bpy.ops.wm.append(
        filepath=sciezka_kolekcji,
        directory=os.path.join(sciezka_blend, "Collection"),
        filename=nazwa_kolekcji
    )
    return True

def animuj_lisc(obj, faza, czestosc=0.05, amplituda=0.3):
    """Generuje sinusoidalny ruch liścia na osi Y."""
    wyczysc_animacje(obj)
    rotacja_bazowa_y = obj.rotation_euler[1]
    
    for klatka in range(KLATKA_START, KLATKA_KONIEC + 1):
        # Równanie ruchu: kąt = baza + A * sin(omega * t + phi)
        kat = rotacja_bazowa_y + amplituda * math.sin(klatka * czestosc + faza)
        obj.rotation_euler[1] = kat
        obj.keyframe_insert(data_path="rotation_euler", frame=klatka, index=1)

def animuj_wszystkie_liscie(prefix_nazwy="RoslinaLisc"):
    """Iteruje po obiektach i nakłada animację z przesunięciem fazowym."""
    liscie = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]
    if not liscie:
        print(f"Ostrzeżenie: Nie znaleziono obiektów z prefixem {prefix_nazwy}")
        return

    n = len(liscie)
    for i, lisc in enumerate(liscie):
        faza_lisc = i * (2 * math.pi / max(n, 1))
        animuj_lisc(lisc, faza=faza_lisc)
    print(f"Zaanimowano {n} liści.")

def animuj_pak(obj, klatka_otwarcia, klatka_zamkniecia):
    """Animuje skalowanie pojedynczego pąka."""
    wyczysc_animacje(obj)
    

    obj.scale = (0.1, 0.1, 0.1)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_START)
    
   
    obj.scale = (0.1, 0.1, 0.1)
    obj.keyframe_insert(data_path="scale", frame=klatka_otwarcia)
    
    obj.scale = (0.19, 0.19, 0.18)
    obj.keyframe_insert(data_path="scale", frame=klatka_zamkniecia)
    
  
    obj.keyframe_insert(data_path="scale", frame=KLATKA_KONIEC)

def animuj_wszystkie_paki(prefix_nazwy="Roslina_Pak"):
    """Znajduje wszystkie pąki i animuje je z asynchronicznym opóźnieniem."""
    paki = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]
    
    if not paki:
        print(f"Błąd: Nie znaleziono pąków z prefixem '{prefix_nazwy}'.")
        print(f"Dostępne obiekty to np.: {[o.name for o in bpy.data.objects][:10]}...")
        return

    opoznienie = 10  
    
    for i, pak in enumerate(paki):
        start = 30 + (i * opoznienie)
        koniec = 90 + (i * opoznienie)
        
        if koniec > KLATKA_KONIEC:
            koniec = KLATKA_KONIEC
            
        animuj_pak(pak, klatka_otwarcia=start, klatka_zamkniecia=koniec)
        
    print(f"Zaanimowano {len(paki)} pąków (asynchronicznie).")

def ustaw_scene():
    bpy.context.scene.frame_start = KLATKA_START
    bpy.context.scene.frame_end = KLATKA_KONIEC
    bpy.context.scene.render.fps = FPS

if __name__ == "__main__":
    ustaw_scene()
    
    if NAZWA_KOLEKCJI not in bpy.data.collections:
        importuj_rosline(SCIEZKA_LAB07, NAZWA_KOLEKCJI)
    
    animuj_wszystkie_liscie()
    animuj_wszystkie_paki(prefix_nazwy="Roslina_Pak") 
    
    print("System animacji zakończył pracę pomyślnie.")