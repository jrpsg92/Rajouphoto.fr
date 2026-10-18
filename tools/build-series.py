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

LARGEURS = [640, 1200, 1800, 2400]

LIENS = [
    ("index.html", "Accueil"),
    ("humains.html", "Humains"),
    ("fragments.html", "Fragments"),
    ("moments.html", "Moments"),
    ("prestations.html", "Prestations"),
    ("contact.html", "Contact"),
]


def jeu(fichier: str, sizes: str) -> str:
    """srcset limité aux tailles réellement présentes dans img/."""
    presentes = [l for l in LARGEURS if (RACINE / "img" / f"{fichier}-{l}.webp").exists()]
    if not presentes:
        raise SystemExit(
            f"Aucune image pour « {fichier} ». Lancez d'abord tools/build-images.py."
        )
    srcset = ", ".join(f"img/{fichier}-{l}.webp {l}w" for l in presentes)
    return (f'src="img/{fichier}-{presentes[0]}.webp" srcset="{srcset}"\n'
            f'               sizes="{sizes}"')


def tete(titre: str, description: str, page: str, og: str) -> str:
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
<meta property="og:image" content="{BASE}/img/{og}-1200.webp">
<meta property="og:url" content="{BASE}/{page}">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E0B09">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="saut-contenu" href="#contenu">Aller au contenu</a>"""


def entete(actif: str) -> str:
    items = "\n".join(
        f'      <li><a href="{h}"{" aria-current=\"page\"" if h == actif else ""}>{t}</a></li>'
        for h, t in LIENS
    )
    return f"""<header class="entete" data-entete>
  <div class="enveloppe entete__rangee">
    <a class="signature" href="index.html">{SITE['nom']}</a>
    <button class="bascule" data-bascule aria-expanded="false" aria-controls="menu">
      <span class="bascule__traits" aria-hidden="true"></span>
      <span data-libelle>Menu</span>
    </button>
  </div>
</header>

<nav class="nav" id="menu" data-nav aria-label="Navigation principale">
  <ul>
{items}
  </ul>
</nav>"""


def pied() -> str:
    liens = "\n".join(
        f'        <li><a href="{h}">{t}</a></li>' for h, t in LIENS[1:]
    ) + '\n        <li><a href="mentions-legales.html">Mentions légales</a></li>'
    return f"""<footer class="pied">
  <div class="enveloppe">
    <div class="pied__rangee">
      <div>
        <p class="pied__nom didone">{SITE['nom']}</p>
        <p>{SITE['base']}, et partout où le projet se trouve.</p>
        <p><a href="{SITE['instagram']}" rel="noopener">Instagram</a></p>
      </div>
      <ul>
{liens}
      </ul>
    </div>
    <p class="pied__mention">© 2026 {SITE['nom']}. Toutes les photographies sont protégées.</p>
  </div>
</footer>

<script src="script.js" defer></script>
</body>
</html>
"""


def page_serie(serie: dict) -> str:
    vignettes = "\n".join(
        f'        <figure class="cliche">\n'
        f'          <button type="button" data-cliche>\n'
        f'            <img {jeu(c["fichier"], "(min-width: 52rem) 31vw, 47vw")}\n'
        f'               alt="{c["alt"]}" loading="lazy">\n'
        f"          </button>\n"
        f"        </figure>"
        for c in serie["cliches"]
    )
    titre = f"{serie['titre']} — {SITE['nom']}"
    return f"""{tete(titre, serie['resume'], serie['cle'] + '.html', serie['couverture'])}

{entete(serie['cle'] + '.html')}

<main id="contenu">
  <section class="section" style="padding-top:clamp(7rem,16vh,11rem)">
    <div class="enveloppe">
      <div class="section__chapeau">
        <p class="repere">Série</p>
        <h1>{serie['titre']}</h1>
        <p style="margin-top:1.2rem;color:var(--ivoire-doux)">{serie['resume']}</p>
      </div>

      <div class="planche">
{vignettes}
      </div>
    </div>
  </section>
</main>

<dialog class="visionneuse" data-visionneuse aria-label="Photographie agrandie">
  <img src="" alt="">
  <div class="visionneuse__barre">
    <button class="visionneuse__bouton" data-prec type="button" aria-label="Précédente">←</button>
    <button class="visionneuse__bouton" data-fermer type="button" aria-label="Fermer">✕</button>
    <button class="visionneuse__bouton" data-suiv type="button" aria-label="Suivante">→</button>
  </div>
  <p class="hors-ecran" data-rang aria-live="polite"></p>
</dialog>

{pied()}"""


def apercu() -> str:
    blocs = []
    for s in SERIES:
        blocs.append(
            f'        <a class="serie" href="{s["cle"]}.html">\n'
            f'          <div class="serie__cadre">\n'
            f'            <img {jeu(s["couverture"], "(min-width: 52rem) 31vw, 100vw")}\n'
            f'               alt="{s["titre"]}, {s["resume"].rstrip(".").lower()}" loading="lazy">\n'
            f"          </div>\n"
            f'          <div class="serie__pied">\n'
            f'            <h3>{s["titre"]}</h3>\n'
            f'            <span class="serie__nombre">{len(s["cliches"]):02d}</span>\n'
            f"          </div>\n"
            f"        </a>"
        )
    return '      <div class="series">\n' + "\n".join(blocs) + "\n      </div>"


def elaguer_srcset() -> None:
    """Retire des srcset les largeurs qui n'existent pas dans img/.

    Toutes les photos n'ont pas la même définition d'origine, et on
    n'agrandit jamais : une page écrite à la main peut donc réclamer un
    fichier absent, et le navigateur affiche une image cassée. Ce passage
    est le garde-fou.
    """
    corriges = 0
    for page in sorted(RACINE.glob("*.html")):
        texte = page.read_text(encoding="utf-8")
        avant = texte

        def nettoyer(m: re.Match) -> str:
            gardees = []
            for bout in m.group(1).split(","):
                bout = bout.strip()
                if not bout:
                    continue
                chemin = bout.split()[0]
                if (RACINE / chemin).exists():
                    gardees.append(bout)
            return f'srcset="{", ".join(gardees)}"'

        texte = re.sub(r'srcset="([^"]+)"', nettoyer, texte)

        # Un src qui pointe vers un fichier absent est remplacé par la plus
        # grande largeur réellement disponible pour cette photo.
        def rabattre(m: re.Match) -> str:
            chemin = m.group(1)
            if (RACINE / chemin).exists():
                return m.group(0)
            souche = re.sub(r"-\d+\.webp$", "", chemin)
            dispo = sorted(RACINE.glob(f"{souche}-*.webp"),
                           key=lambda p: int(p.stem.rsplit("-", 1)[1]))
            if not dispo:
                raise SystemExit(f"{page.name} : aucune image pour {chemin}")
            return f'src="{dispo[-1].relative_to(RACINE)}"'

        texte = re.sub(r'src="(img/[^"]+\.webp)"', rabattre, texte)

        if texte != avant:
            page.write_text(texte, encoding="utf-8")
            corriges += 1
    if corriges:
        print(f"  {corriges} page(s) : srcset élagué des largeurs absentes")


def main() -> None:
    for s in SERIES:
        (RACINE / f"{s['cle']}.html").write_text(page_serie(s), encoding="utf-8")
        print(f"  {s['cle']}.html écrite ({len(s['cliches'])} photographies)")

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
    elaguer_srcset()


if __name__ == "__main__":
    main()
