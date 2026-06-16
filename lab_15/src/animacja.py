import bpy



INTENSYWNOSC_DESZCZU = 15000     # Liczba cząsteczek deszczu
PREDKOSC_OPADANIA = 20.0         # Prędkość początkowa (wpływa na efekt rozmycia)
CZAS_TRWANIA_ANIMACJI = 250      # Klatka końcowa (min. 150 wg wymagań)
WIELKOSC_CHMURY = 30.0           # Rozmiar obszaru, z którego pada deszcz
# ==========================================

def stworz_deszcz():
    # 1. Utworzenie emitera (chmury) wysoko nad ulicą
    bpy.ops.mesh.primitive_plane_add(size=WIELKOSC_CHMURY, location=(0, 0, 15))
    emiter = bpy.context.object
    emiter.name = "Emiter_Deszczu"
    
    # Ukrycie samego płaskiego emitera w renderze (chcemy widzieć tylko deszcz)
    emiter.show_instancer_for_render = False
    emiter.show_instancer_for_viewport = False

    # 2. Utworzenie systemu cząsteczek
    bpy.ops.object.particle_system_add()
    psys = emiter.particle_systems[0]
    psys.name = "System_Deszczu"
    pset = psys.settings
    
    # 3. Konfiguracja fizyki deszczu
    pset.count = INTENSYWNOSC_DESZCZU
    # Ujemna klatka startowa gwarantuje, że w klatce 0 deszcz już pada na ziemię
    pset.frame_start = -50 
    pset.frame_end = CZAS_TRWANIA_ANIMACJI
    pset.lifetime = 100
    pset.normal_factor = -PREDKOSC_OPADANIA  # Emisja w dół
    pset.factor_random = 0.3                 # Losowość prędkości kropel

    # 4. Utworzenie fizycznego modelu pojedynczej kropli (wydłużony walec)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.3, location=(0, 0, 0))
    kropla = bpy.context.object
    kropla.name = "Wzor_Kropli"
    # Ukrycie wzoru kropli poza kadrem
    kropla.location = (100, 100, 100)
    kropla.hide_render = True

    # 5. Generowanie materiału kropli (Blender 4.x - Principled BSDF)
    mat = bpy.data.materials.new(name="Material_Kropli")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.05
        # Ustawienia refrakcji dla wody
        if 'Transmission Weight' in bsdf.inputs: # Blender 4.0+
            bsdf.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in bsdf.inputs:      # Wsteczna kompatybilność
            bsdf.inputs['Transmission'].default_value = 1.0
        bsdf.inputs['IOR'].default_value = 1.33  # IOR dla wody
    
    kropla.data.materials.append(mat)

    # 6. Przypisanie modelu kropli do systemu cząsteczek
    pset.render_type = 'OBJECT'
    pset.instance_object = kropla
    pset.particle_size = 0.2
    pset.size_random = 0.6
    
    # 7. Dynamiczna rotacja: krople odwracają się zgodnie z wektorem prędkości (w dół)
    pset.use_dynamic_rotation = True
    pset.rotation_mode = 'VEL'
    
    print("Sukces: System deszczu został wygenerowany!")

stworz_deszcz()