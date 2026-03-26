import bpy
import math
import os
import random


TYPY_ROSLIN = {
    "drzewo": {
        "wysokosc": (3.0, 5.0),
        "liczba_lisci": (4, 6),
        "promien_lisci": (0.4, 0.7),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.15, 0.08, 0.02, 1),  # ciemny brąz
        "kolor_lisci": (0.05, 0.35, 0.1, 1),    # ciemna zieleń
    },
    "krzew": {
        "wysokosc": (0.8, 1.8),
        "liczba_lisci": (5, 8),
        "promien_lisci": (0.5, 0.9),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.25, 0.15, 0.05, 1),  # jasny brąz
        "kolor_lisci": (0.1, 0.5, 0.05, 1),     # żywa zieleń
    },
    "paproc": {
        "wysokosc": (0.5, 1.2),
        "liczba_lisci": (6, 10),
        "promien_lisci": (0.6, 1.0),
        "liczba_korzeni": (2, 3),
        "kolor_lodygi": (0.2, 0.3, 0.1, 1),     # oliwkowy
        "kolor_lisci": (0.0, 0.6, 0.15, 1),     # soczysty zielony
    },
}


def wyczysc_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    for coll in bpy.data.collections:
        if coll.name.startswith("Las"):
            bpy.data.collections.remove(coll)

def stworz_material(nazwa, kolor, metaliczny, szorstkosc, emisja=False):
    mat = bpy.data.materials.new(name=nazwa)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = kolor
        bsdf.inputs["Metallic"].default_value = metaliczny
        bsdf.inputs["Roughness"].default_value = szorstkosc
        if emisja and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = kolor
            bsdf.inputs["Emission Strength"].default_value = 0.5
    return mat

def stworz_lodyge(x, z, wysokosc, material):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15, 
        depth=wysokosc, 
        location=(x, z, wysokosc / 2)
    )
    lodyga = bpy.context.active_object
    lodyga.name = "Lodyga"
    lodyga.data.materials.append(material)
    return lodyga

def stworz_liscie(x, z, wysokosc, liczba_lisci, promien_lisci, material):
    odleglosc = 0.3
    liscie_obiekty = []
    
    for i in range(liczba_lisci):
        kat = i * (2 * math.pi / liczba_lisci) 
        lisc_x = x + odleglosc * math.cos(kat)
        lisc_y = z + odleglosc * math.sin(kat)
        lisc_z = wysokosc - 0.1
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lisc_x, lisc_y, lisc_z))
        lisc = bpy.context.active_object
        lisc.name = f"Lisc_{i}"
        lisc.scale = (promien_lisci, promien_lisci * 0.3, 0.05)
        lisc.rotation_euler = (0, math.radians(30), kat)
        lisc.data.materials.append(material)
        liscie_obiekty.append(lisc)
        
    return liscie_obiekty

def stworz_korzenie(x, z, liczba_korzeni, material):
    odleglosc = 0.2
    korzenie_obiekty = []
    
    for i in range(liczba_korzeni):
        kat = i * (2 * math.pi / liczba_korzeni)
        korzen_x = x + odleglosc * math.cos(kat)
        korzen_y = z + odleglosc * math.sin(kat)
        korzen_z = 0.05 
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(korzen_x, korzen_y, korzen_z))
        korzen = bpy.context.active_object
        korzen.name = f"Korzen_{i}"
        korzen.scale = (0.3, 0.1, 0.05)
        korzen.rotation_euler = (0, math.radians(30), kat)
        korzen.data.materials.append(material)
        korzenie_obiekty.append(korzen)
        
    return korzenie_obiekty

def stworz_rosline(x, z, wysokosc, liczba_lisci, promien_lisci, liczba_korzeni, kolor_lodygi, kolor_lisci):
    mat_lodyga = stworz_material("Mat_Lodyga", kolor_lodygi, 0.1, 0.8)
    mat_lisc = stworz_material("Mat_Lisc", kolor_lisci, 0.1, 0.5, emisja=True)
    
    lodyga = stworz_lodyge(x, z, wysokosc, mat_lodyga)
    liscie = stworz_liscie(x, z, wysokosc, liczba_lisci, promien_lisci, mat_lisc)
    korzenie = stworz_korzenie(x, z, liczba_korzeni, mat_lodyga)
   
    return [lodyga] + liscie + korzenie


def stworz_rosline_typ(x, z, typ):
    parametry = TYPY_ROSLIN[typ]
    
    wysokosc = random.uniform(*parametry["wysokosc"])
    liczba_lisci = random.randint(*parametry["liczba_lisci"])
    promien_lisci = random.uniform(*parametry["promien_lisci"])
    liczba_korzeni = random.randint(*parametry["liczba_korzeni"])
    
    obiekty = stworz_rosline(
        x, z, 
        wysokosc, liczba_lisci, promien_lisci, liczba_korzeni, 
        parametry["kolor_lodygi"], parametry["kolor_lisci"]
    )
    
    return obiekty


def wybierz_typ_biomu(x, z, rozmiar_pola):
    max_odleglosc = max(abs(x), abs(z))
    prog_wewnetrzny = 0.3 * (rozmiar_pola / 2)
    prog_zewnetrzny = 0.7 * (rozmiar_pola / 2)
    
    if max_odleglosc < prog_wewnetrzny:
        return "drzewo"
    elif max_odleglosc < prog_zewnetrzny:
        return "krzew" if random.random() < 0.7 else "drzewo"
    else:
        return "paproc" if random.random() < 0.6 else "krzew"


def generuj_las(liczba_roslin=40, rozmiar_pola=15.0, seed=42):
    random.seed(seed)
    wyczysc_scene()
    
    kolekcja_las = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(kolekcja_las)
    

    podkolekcje = {}
    for typ in TYPY_ROSLIN.keys():
        sub_coll = bpy.data.collections.new(f"Las_{typ.capitalize()}")
        kolekcja_las.children.link(sub_coll)
        podkolekcje[typ] = sub_coll


    for _ in range(liczba_roslin):
        x = random.uniform(-rozmiar_pola/2, rozmiar_pola/2)
        z = random.uniform(-rozmiar_pola/2, rozmiar_pola/2)
        
        typ = wybierz_typ_biomu(x, z, rozmiar_pola)
        nowe_obiekty = stworz_rosline_typ(x, z, typ)
        
  
        docelowa_kolekcja = podkolekcje[typ]
        for obj in nowe_obiekty:
            for obecna_kolekcja in obj.users_collection:
                obecna_kolekcja.objects.unlink(obj)
            docelowa_kolekcja.objects.link(obj)

    # --- KAMERA I ŚWIATŁO ---
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    slonce = bpy.context.active_object
    slonce.data.energy = 5.0
    slonce.rotation_euler = (math.radians(45), 0, math.radians(45))


    bpy.ops.object.camera_add(location=(0, -rozmiar_pola*0.9, rozmiar_pola*0.7))
    kamera = bpy.context.active_object
    kamera.rotation_euler = (math.radians(55), 0, 0) 
    bpy.context.scene.camera = kamera

    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.filepath = os.path.abspath("las_05.png")
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800

    bpy.ops.render.render(write_still=True)
    print(f"Wygenerowano las ({liczba_roslin} roślin) z seedem {seed}.")
    print("Render zapisany jako: las_05.png")


generuj_las(liczba_roslin=60, rozmiar_pola=20.0, seed=123)