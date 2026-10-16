#!/usr/bin/env python3
"""
Fabrique des images d'attente, le temps que les vraies photos arrivent.

Elles respectent les proportions et les noms attendus par series.json,
ce qui permet de juger la mise en page tout de suite. Dès que les
originaux sont déposés dans photos/, tools/build-images.py écrase ces
fichiers et ce script n'a plus lieu d'être lancé.

Usage : python3 tools/build-placeholders.py
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "img"
SORTIE.mkdir(exist_ok=True)

MANIFESTE = json.loads((RACINE / "series.json").read_text(encoding="utf-8"))
LARGEURS = [640, 1200, 1800]
PAPIER_CREUX = (239, 237, 232)
TRAIT = (188, 184, 176)
TEXTE = (120, 116, 110)


def police(taille: int):
    for chemin in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        if Path(chemin).exists():
            return ImageFont.truetype(chemin, taille)
    return ImageFont.load_default()


def fabriquer(nom: str, portrait: bool) -> None:
    for large in LARGEURS:
        haut = round(large * (3 / 2) if portrait else large * (2 / 3))
        im = Image.new("RGB", (large, haut), PAPIER_CREUX)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, large - 1, haut - 1), outline=TRAIT, width=2)
        # croix légère, repère de cadrage
        d.line((0, 0, large, haut), fill=TRAIT, width=1)
        d.line((large, 0, 0, haut), fill=TRAIT, width=1)

        f = police(max(14, large // 26))
        libelle = f"{nom}  ·  image d'attente"
        boite = d.textbbox((0, 0), libelle, font=f)
        d.rectangle(
            (
                (large - (boite[2] - boite[0])) / 2 - 18,
                (haut - (boite[3] - boite[1])) / 2 - 12,
                (large + (boite[2] - boite[0])) / 2 + 18,
                (haut + (boite[3] - boite[1])) / 2 + 14,
            ),
            fill=PAPIER_CREUX,
        )
        d.text(
            ((large - (boite[2] - boite[0])) / 2, (haut - (boite[3] - boite[1])) / 2),
            libelle,
            font=f,
            fill=TEXTE,
        )
        im.save(SORTIE / f"{nom}-{large}.webp", "WEBP", quality=72, method=6)


def main() -> None:
    n = 0
    for serie in MANIFESTE["series"]:
        for i, cliche in enumerate(serie["cliches"]):
            # on alterne paysage et portrait pour éprouver la mise en page
            fabriquer(cliche["fichier"], portrait=(i % 3 == 1))
            n += 1
    print(f"{n} images d'attente écrites dans img/ ({len(LARGEURS)} tailles chacune).")
    print("Elles seront remplacées dès le premier passage de build-images.py.")


if __name__ == "__main__":
    main()
