# Site de Raju Sinniah — photographe

Site statique, sans framework ni dépendance à installer. Il tourne sur
GitHub Pages tel quel. Les seuls outils sont trois scripts Python qui
préparent les images et régénèrent le HTML des séries.

---

## Ce qu'il reste à faire avant la mise en ligne publique

1. **Compléter `mentions-legales.html`** — tous les champs `[À COMPLÉTER]`.
   C'est une obligation légale en France pour un site professionnel.
4. **Ajouter une adresse e-mail** sur `contact.html`. Instagram seul fait
   perdre des demandes, et beaucoup d'entreprises n'écrivent pas en DM.

---

## Ajouter ou remplacer des photographies

Les photos vivent dans `photos/<série>/`, nommées comme dans `series.json`.

```
photos/
  humains/    humains-01.jpg, humains-02.jpg, …
  fragments/  fragments-01.jpg, …
  moments/    moments-01.jpg, …
```

Déposez les **originaux pleine résolution**, les scripts se chargent de la
réduction. Puis :

```bash
python3 tools/build-images.py    # produit img/<nom>-640|1200|1800|2400.webp
python3 tools/build-series.py    # réécrit humains/fragments/moments.html + l'accueil
```

Pour **ajouter** une photo, créez son entrée dans `series.json` avant de
lancer les scripts :

```json
{ "fichier": "humains-07", "alt": "Description de l'image", "pleine": true }
```

- `alt` décrit l'image pour les personnes non voyantes et pour les moteurs.
  Écrivez une vraie description, pas « photo 7 ».
- `pleine: true` affiche l'image sur toute la largeur. Sans cette clé, elle
  occupe une demi-colonne. Alternez pour garder du rythme.

> **Important.** `photos/` est exclu du dépôt par `.gitignore` — les
> originaux pleine résolution d'un photographe pèsent trop lourd pour
> GitHub. Seuls les dérivés WebP de `img/` sont versionnés. Les originaux
> n'existent donc que sur votre machine : gardez-en une sauvegarde
> ailleurs, le dépôt n'en est pas une.

### Qualité d'image

`tools/build-images.py` sort du WebP qualité 90 jusqu'à 2400 px de large.
Une photo n'est jamais agrandie, donc un original de 1400 px ne produit
que les largeurs inférieures. `build-series.py` élague alors les `srcset`
des largeurs absentes, ce qui évite les images cassées.
C'est volontairement généreux : sur le site d'un photographe, les images
sont le produit. Ne baissez ces réglages que si Raju le demande.

---

## Changer l'apparence

Tout est dans `style.css`, dans le bloc `:root` en haut du fichier.

```css
--noir:   #0E0B09;   /* fond, un noir chaud de chambre noire */
--ivoire: #F2EDE6;   /* texte */
--rouge:  #E04A4A;   /* unique couleur vive, repères de lecture */
```

Les contrastes ont été vérifiés : toutes les paires texte/fond dépassent
4,5:1, les contours porteurs d'information 3:1. Si vous changez une
couleur, revérifiez avec un outil de contraste avant de publier.

Les polices sont **Bodoni Moda** pour les titres et le nom, **Jost** pour
le texte courant, chargées depuis Google Fonts.

---

## Structure

```
index.html                 accueil
humains.html               ─┐
fragments.html              ├ générées par build-series.py, ne pas éditer à la main
moments.html               ─┘
prestations.html           prestations
contact.html               contact
mentions-legales.html      mentions légales
series.json                le portfolio : séries, fichiers, descriptions
style.css                  toute la mise en forme
script.js                  menu et visionneuse
tools/                     scripts de préparation
photos/                    originaux, non publiés tels quels
img/                       dérivés WebP, générés
```

> Les trois pages de séries sont **écrasées** à chaque `build-series.py`.
> Pour modifier leur structure, éditez le gabarit dans
> `tools/build-series.py`, pas les fichiers HTML.

---

## Vérifier le rendu en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

`python3 tools/captures.py index.html humains.html` produit des captures
mobile et bureau, pratique pour relire la mise en page.

---

## Publier

GitHub Pages sert la branche `main`. Un `git push` suffit, la mise en
ligne prend une à deux minutes. Pensez à vider le cache du navigateur
(Ctrl+Maj+R) avant de conclure que ça n'a pas marché.
