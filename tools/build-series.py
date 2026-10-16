#!/usr/bin/env python3
"""
Écrit les pages de séries et l'aperçu de l'accueil à partir de series.json.

Le HTML est produit en dur, pas chargé en JavaScript : les images restent
visibles sans JS et indexables par les moteurs.

Usage : python3 tools/build-series.py
"""
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MANIFESTE = json.loads((RACINE / "series.json").read_text(encoding="utf-8"))
SITE = MANIFESTE["site"]
SERIES = MANIFESTE["series"]
BASE = "https://jrpsg92.github.io/Rajouphoto.fr"

LARGEURS_DISPO = [640, 1200, 1800, 2400]


def jeu(fichier: str, sizes: str) -> str:
    """srcset limité aux tailles réellement présentes dans img/."""
    presentes = [l for l in LARGEURS_DISPO if (RACINE / "img" / f"{fichier}-{l}.webp").exists()]
    if not presentes:
        raise SystemExit(
            f"Aucune image pour « {fichier} ». Lancez d'abord "
            "tools/build-placeholders.py ou tools/build-images.py."
        )
    srcset = ", ".join(f"img/{fichier}-{l}.webp {l}w" for l in presentes)
    return (f'src="img/{fichier}-{presentes[0]}.webp" srcset="{srcset}"\n'
            f'               sizes="{sizes}"')


def entete(actif: str) -> str:
    liens = [
        ("index.html", "Accueil"),
        ("humains.html", "Humains"),
        ("fragments.html", "Fragments"),
        ("moments.html", "Moments"),
        ("travailler-ensemble.html", "Travailler ensemble"),
        ("contact.html", "Contact"),
    ]
    items = "\n".join(
        f'        <li><a href="{h}"{" aria-current=\"page\"" if h == actif else ""}>{t}</a></li>'
        for h, t in liens
    )
    return f"""<header class="entete">
  <div class="enveloppe entete__rangee">
    <a class="signature" href="index.html">
      {SITE['nom']}
      <span>{SITE['metier']}</span>
    </a>
    <button class="bascule" data-bascule aria-expanded="false" aria-controls="menu" hidden>
      <span class="bascule__traits" aria-hidden="true"></span> Menu
    </button>
    <nav class="nav" id="menu" data-nav aria-label="Navigation principale">
      <ul>
{items}
      </ul>
    </nav>
  </div>
</header>"""


def pied() -> str:
    return f"""<footer class="pied">
  <div class="enveloppe">
    <div class="pied__rangee">
      <div>
        <p>{SITE['nom']}, photographe depuis {SITE['depuis']}.</p>
        <p>Basé en {SITE['base']}, je me déplace dans {SITE['zone'][0].lower() + SITE['zone'][1:]}.</p>
        <p><a href="{SITE['instagram']}" rel="noopener">Instagram</a></p>
      </div>
      <ul>
        <li><a href="humains.html">Humains</a></li>
        <li><a href="fragments.html">Fragments</a></li>
        <li><a href="moments.html">Moments</a></li>
        <li><a href="travailler-ensemble.html">Travailler ensemble</a></li>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="mentions-legales.html">Mentions légales</a></li>
      </ul>
    </div>
    <p class="pied__mention">© 2026 {SITE['nom']}. Toutes les photographies sont protégées.</p>
  </div>
</footer>"""


def tete(titre: str, description: str, page: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{BASE}/{page}">

<meta property="og:type" content="website">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{BASE}/{page}">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F7F6F3">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="saut-contenu" href="#contenu">Aller au contenu</a>"""


def page_serie(serie: dict) -> str:
    planches = []
    for c in serie["cliches"]:
        # Planche contact : toutes les vignettes ont le même cadre, la photo
        # s'ouvre en grand dans la visionneuse.
        sizes = "(min-width: 52rem) 31vw, 47vw"
        planches.append(
            f'        <figure class="cliche">\n'
            f'          <button type="button" data-cliche>\n'
            f'            <img {jeu(c["fichier"], sizes)}\n'
            f'               alt="{c["alt"]}" loading="lazy">\n'
            f"          </button>\n"
            f"        </figure>"
        )

    titre = f"{serie['titre']} — {SITE['nom']}"
    desc = serie["resume"]
    return f"""{tete(titre, desc, serie['cle'] + '.html')}

{entete(serie['cle'] + '.html')}

<main id="contenu">
  <section class="section">
    <div class="enveloppe">
      <div class="section__chapeau colonne">
        <h1>{serie['titre']}</h1>
        <p>{serie['resume']}</p>
      </div>

      <div class="planche">
{chr(10).join(planches)}
      </div>
    </div>
  </section>

  <section class="section section--creuse">
    <div class="enveloppe">
      <div class="colonne">
        <h2>Un projet en tête&nbsp;?</h2>
        <p>Portraits, mariages, anniversaires, images de marque. Dites-moi ce que
           vous préparez, je vous dis comment je m'y prendrais.</p>
        <p style="margin-top:1.75rem"><a class="action" href="contact.html">Me contacter</a></p>
      </div>
    </div>
  </section>
</main>

<dialog class="visionneuse" data-visionneuse aria-label="Photographie agrandie">
  <img src="" alt="">
  <div class="visionneuse__barre">
    <button class="visionneuse__bouton" data-prec type="button" aria-label="Photographie précédente">‹</button>
    <button class="visionneuse__bouton" data-fermer type="button" aria-label="Fermer">✕</button>
    <button class="visionneuse__bouton" data-suiv type="button" aria-label="Photographie suivante">›</button>
  </div>
  <p class="hors-ecran" data-rang aria-live="polite"></p>
</dialog>

{pied()}

<script src="script.js" defer></script>
</body>
</html>
"""


def apercu() -> str:
    blocs = []
    for s in SERIES:
        blocs.append(
            f'        <a class="serie" href="{s["cle"]}.html">\n'
            f'          <div class="serie__cadre">\n'
            f'            <img {jeu(s["couverture"], "(min-width: 52rem) 31vw, 100vw")}\n'
            f'               alt="{s["titre"]} — {s["resume"][:60]}" loading="lazy">\n'
            f"          </div>\n"
            f'          <div class="serie__pied">\n'
            f'            <h2>{s["titre"]}</h2>\n'
            f'            <span class="serie__nombre">{len(s["cliches"])} photographies</span>\n'
            f"          </div>\n"
            f'          <p style="margin-top:.9rem;color:var(--encre-doux)">{s["resume"]}</p>\n'
            f"        </a>"
        )
    return '      <div class="series">\n' + "\n".join(blocs) + "\n      </div>"


def main() -> None:
    for s in SERIES:
        cible = RACINE / f"{s['cle']}.html"
        cible.write_text(page_serie(s), encoding="utf-8")
        print(f"  {cible.name} écrite ({len(s['cliches'])} photographies)")

    index = RACINE / "index.html"
    texte = index.read_text(encoding="utf-8")
    motif = re.compile(r"(<!-- series:debut -->).*?(<!-- series:fin -->)", re.S)
    if not motif.search(texte):
        raise SystemExit("Marqueurs « series » introuvables dans index.html")
    index.write_text(
        motif.sub(lambda m: f"{m.group(1)}\n{apercu()}\n      {m.group(2)}", texte),
        encoding="utf-8",
    )
    print("  index.html : aperçu des séries régénéré")


if __name__ == "__main__":
    main()
