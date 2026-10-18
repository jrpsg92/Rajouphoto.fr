#!/usr/bin/env python3
"""
Prépare les images du site à partir des originaux.

Réglages pensés pour un photographe : largeurs jusqu'à 2400 px et
qualité 90. Les fichiers pèsent plus lourd que sur un site vitrine
ordinaire, et c'est voulu — les images sont le produit.

Arborescence attendue :
    photos/humains/humains-01.jpg
    photos/fragments/fragments-01.jpg
    photos/moments/moments-01.jpg

Sortie : img/<nom>-<largeur>.webp

Usage : python3 tools/build-images.py
"""
from pathlib import Path

from PIL import Image, ImageOps

RACINE = Path(__file__).resolve().parent.parent
SOURCES = RACINE / "photos"  # les sous-dossiers de séries, plus la racine
SORTIE = RACINE / "img"
SORTIE.mkdir(exist_ok=True)

# 136 photographies : trois largeurs suffisent, et la qualité reste
# haute pour la vue agrandie. Au-delà, le dépôt devient ingérable.
LARGEURS = [480, 1000, 1700]
QUALITE = 84
EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}


def exporter(src: Path) -> int:
    """Écrit les déclinaisons d'une photo, sans jamais agrandir l'original."""
    produits = 0
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        for large in LARGEURS:
            if large > im.width and produits:
                break  # au moins une taille, jamais d'agrandissement ensuite
            l = min(large, im.width)
            h = round(im.height * l / im.width)
            cible = SORTIE / f"{src.stem}-{large}.webp"
            im.resize((l, h), Image.LANCZOS).save(
                cible, "WEBP", quality=QUALITE, method=6
            )
            produits += 1
            print(f"  {cible.name:<28} {cible.stat().st_size / 1024:7.0f} Ko")
    return produits


def main() -> None:
    if not SOURCES.exists():
        raise SystemExit(
            f"Dossier introuvable : {SOURCES}\n"
            "Créez photos/humains, photos/fragments et photos/moments, "
            "puis déposez-y les originaux."
        )

    trouvees = 0
    racine = sorted(p for p in SOURCES.iterdir()
                    if p.is_file() and p.suffix.lower() in EXTENSIONS)
    if racine:
        print("portrait :")
        for src in racine:
            exporter(src)
            trouvees += 1

    for dossier in sorted(p for p in SOURCES.iterdir() if p.is_dir()):
        images = sorted(
            p for p in dossier.iterdir() if p.suffix.lower() in EXTENSIONS
        )
        if not images:
            continue
        print(f"{dossier.name} :")
        for src in images:
            exporter(src)
            trouvees += 1

    if not trouvees:
        print("Aucune photo trouvée dans photos/. Rien à faire.")
        return

    total = sum(f.stat().st_size for f in SORTIE.glob("*.webp"))
    print(f"\n{trouvees} photos traitées, {total / 1024 / 1024:.1f} Mo de dérivés.")


if __name__ == "__main__":
    main()
