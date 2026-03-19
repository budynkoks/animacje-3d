import bpy
import math
import os


def wyczysc_scene():
    # Usuwa wszystkie obiekty ze sceny, by startować od zera
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def stworz_material_lodygi():
    # Ciemny, lekko metaliczny materiał dla łodygi
    mat = bpy.data.materials.new(name="Mat_Lodyga")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.3, 0.1, 0.02, 1.0) 
        bsdf.inputs["Metallic"].default_value = 0.9
        bsdf.inputs["Roughness"].default_value = 0.3
    return mat

def stworz_material_liscia():
    # Zielony materiał z lekką emisją dla liści
    mat = bpy.data.materials.new(name="Mat_Lisc")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.01, 0.2, 0.05, 1.0) 
        
        bsdf.inputs["Metallic"].default_value = 0.6
        bsdf.inputs["Roughness"].default_value = 0.2
        
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (0.01, 0.3, 0.05, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 1.0 
    return mat


def stworz_lodyge(pos_x, pos_y, wysokosc, material):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15, 
        depth=wysokosc, 
        location=(pos_x, pos_y, wysokosc / 2)
    )
    lodyga = bpy.context.active_object
    lodyga.name = "Lodyga"
    lodyga.data.materials.append(material)
    return lodyga

def stworz_liscie(pos_x, pos_y, wysokosc, liczba_lisci, promien_lisci, material):
    # Rozmieszczenie liści równomiernie po okręgu wokół łodygi
    odleglosc_od_srodka = 0.3
    
    for i in range(liczba_lisci):
        kat = i * (2 * math.pi / liczba_lisci) 
        
        lisc_x = pos_x + odleglosc_od_srodka * math.cos(kat)
        lisc_y = pos_y + odleglosc_od_srodka * math.sin(kat)
        lisc_z = wysokosc - 0.1
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lisc_x, lisc_y, lisc_z))
        lisc = bpy.context.active_object
        lisc.name = f"Lisc_{i}"
        
        lisc.scale = (promien_lisci , promien_lisci * 0.3, 0.05)
        
        # Stałe pochylenie liścia i obrót wokół osi Z wg kąta
        lisc.rotation_euler = (0, math.radians(30), kat)
        
        lisc.data.materials.append(material)

def stworz_korzenie(pos_x, pos_y, liczba_korzeni, material):
    odleglosc_od_srodka = 0.2
    
    for i in range(liczba_korzeni):
        kat = i * (2 * math.pi / liczba_korzeni)
        
        korzen_x = pos_x + odleglosc_od_srodka * math.cos(kat)
        korzen_y = pos_y + odleglosc_od_srodka * math.sin(kat)
        korzen_z = 0.05 
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(korzen_x, korzen_y, korzen_z))
        korzen = bpy.context.active_object
        korzen.name = f"Korzen_{i}"
        
        korzen.scale = (0.3, 0.1, 0.05)
        
        korzen.rotation_euler = (0, math.radians(30), kat)
        
        korzen.data.materials.append(material)

def stworz_rosline(pos_x=0.0, pos_y=0.0, wysokosc=2.0, liczba_lisci=3, promien_lisci=0.6, liczba_korzeni=4):
    mat_lodyga = stworz_material_lodygi()
    mat_lisc = stworz_material_liscia()
    
    stworz_lodyge(pos_x, pos_y, wysokosc, mat_lodyga)
    stworz_liscie(pos_x, pos_y, wysokosc, liczba_lisci, promien_lisci, mat_lisc)
    stworz_korzenie(pos_x, pos_y, liczba_korzeni, mat_lodyga)

wyczysc_scene()

stworz_rosline(pos_x=-2.0, pos_y=0.0, wysokosc=1.5, liczba_lisci=3, promien_lisci=0.7, liczba_korzeni=6) 
stworz_rosline(pos_x=0.0,  pos_y=0.0, wysokosc=2.5, liczba_lisci=11, promien_lisci=0.7, liczba_korzeni=8) 
stworz_rosline(pos_x=2.0,  pos_y=0.0, wysokosc=3.2, liczba_lisci=7, promien_lisci=0.6, liczba_korzeni=6) 

bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))
slonce = bpy.context.active_object
slonce.data.energy = 12.0
slonce.rotation_euler = (math.radians(45), 0, math.radians(45))

# Kamera
bpy.ops.object.camera_add(location=(0, -8, 4))
kamera = bpy.context.active_object
kamera.rotation_euler = (math.radians(75), 0, 0) 
bpy.context.scene.camera = kamera

# Ustawienia Renderu
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.filepath = os.path.abspath("rosliny_lab04.png")
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 800
scene.render.resolution_y = 600



# Wykonanie renderu
bpy.ops.render.render(write_still=True)
print("Render zapisany jako: rosliny_lab04.png")
