# Lab 08 – GUI: Materiały i Oświetlenie Organiczne

## Co zostało zrealizowane

* **Materiały organiczne:** Dla łodygi i liści wykorzystałem/am węzeł Principled BSDF z odpowiednio ustawionym parametrem Subsurface Scattering (aby symulować przenikanie światła przez tkankę roślinną). Dodatkowo zróżnicowałem/am parametr Roughness za pomocą proceduralnej tekstury szumu (Noise Texture + ColorRamp), co nadało powierzchni bardziej realistyczny wygląd.
* **Materiały mechaniczne:** Skonfigurowałem/am w pełni metaliczny materiał (Metallic = 1.0) dla technicznych detali rośliny.
* **Bioluminescencja:** Wybrane fragmenty rośliny otrzymały materiał świecący, zbudowany przy użyciu węzła Mix Shader, który łączy bazowy Principled BSDF z węzłem Emission (współczynnik Fac poniżej 1.0).
* **Oświetlenie i tło:** Zastosowałem/am klasyczny schemat Three-Point Lighting (Key Light, Fill Light, Rim Light), aby uwypuklić bryłę modelu i nadać scenie odpowiedni klimat. Scenę wzbogacono o tło oparte na mapie HDRI.
* **Postprodukcja:** Rendering wykonano w rozdzielczości 1920x1080 przy użyciu silnika Eevee. Efekt poświaty (Bloom) wokół świecących elementów został zrealizowany po stronie postprodukcji, za pomocą węzła Glare w Blender Compositor. Zapisano plik wynikowy `swiatlo_08.png`.

## Uruchomienie

Projekt został wykonany w programie Blender. Aby poprawnie obejrzeć scenę i materiały:
1. Otwórz plik `.blend` w programie Blender.
2. Aby podejrzeć sieć węzłów dla konkretnego elementu, zaznacz go i przejdź do obszaru roboczego **Shading** (Shader Editor).
3. Aby zobaczyć materiały i oświetlenie (w tym tło HDRI) w czasie rzeczywistym, najedź kursorem na okno 3D (Viewport), wciśnij klawisz `Z` i wybierz tryb **Rendered**.
4. Węzły efektu Bloom można prześledzić przechodząc do zakładki **Compositing**.
5. Aby wyrenderować obraz ponownie, wciśnij klawisz `F12`. Finalny efekt znajduje się również w pliku `swiatlo_08.png`.

## Trudności / refleksja

Znalezienie opcji glare na wersji 5.1.1