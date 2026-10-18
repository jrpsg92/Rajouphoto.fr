/* Raju Sinniah — comportements partagés.
   Tout est optionnel : sans JS, les pages et les photographies
   restent accessibles. */
(function () {
  "use strict";

  /* --- Volet de navigation ---------------------------------------------- */
  var bascule = document.querySelector("[data-bascule]");
  var nav = document.querySelector("[data-nav]");
  var libelle = document.querySelector("[data-libelle]");

  if (bascule && nav) {
    nav.dataset.ouvert = "false";

    function basculer(ouvrir) {
      bascule.setAttribute("aria-expanded", String(ouvrir));
      nav.dataset.ouvert = String(ouvrir);
      if (libelle) libelle.textContent = ouvrir ? "Fermer" : "Menu";
      // Empêche la page de défiler derrière le volet.
      document.body.style.overflow = ouvrir ? "hidden" : "";
    }

    bascule.addEventListener("click", function () {
      basculer(bascule.getAttribute("aria-expanded") !== "true");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && bascule.getAttribute("aria-expanded") === "true") {
        basculer(false);
        bascule.focus();
      }
    });
  }

  /* --- Fond de l'en-tête au défilement ----------------------------------- */
  var entete = document.querySelector("[data-entete]");
  if (entete) {
    var poser = function () {
      entete.dataset.pose = String(window.scrollY > 40);
    };
    poser();
    window.addEventListener("scroll", poser, { passive: true });
  }

  /* --- Apparition au défilement ------------------------------------------ */
  /* Les éléments montent quand ils entrent dans le cadre. Rien n'est caché
     tant que le script n'a pas pris la main, donc une page sans JavaScript
     reste entièrement lisible. */
  var aVoir = Array.prototype.slice.call(document.querySelectorAll("[data-apparait]"));
  var sobre = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (aVoir.length && "IntersectionObserver" in window && !sobre) {
    var veille = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.dataset.vu = "true";
        veille.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: .08 });

    aVoir.forEach(function (el) { veille.observe(el); });
  } else {
    aVoir.forEach(function (el) { el.dataset.vu = "true"; });
  }

  /* --- Étiquette qui suit le curseur -------------------------------------- */
  var planche = document.querySelector(".planche");
  var pointeurFin = window.matchMedia("(pointer: fine)").matches;

  if (planche && pointeurFin && !sobre) {
    var suiveur = document.createElement("div");
    suiveur.className = "suiveur";
    suiveur.setAttribute("aria-hidden", "true");
    suiveur.textContent = "Agrandir";
    document.body.appendChild(suiveur);

    var x = 0, y = 0, cx = 0, cy = 0, anime = false;

    function glisser() {
      // Léger retard sur le pointeur, pour que le repère ait du poids.
      cx += (x - cx) * .18;
      cy += (y - cy) * .18;
      suiveur.style.translate = cx + "px " + cy + "px";
      if (anime) requestAnimationFrame(glisser);
    }

    planche.addEventListener("pointerenter", function () {
      suiveur.dataset.actif = "true";
      if (!anime) { anime = true; requestAnimationFrame(glisser); }
    });
    planche.addEventListener("pointerleave", function () {
      suiveur.dataset.actif = "false";
      anime = false;
    });
    planche.addEventListener("pointermove", function (e) {
      x = e.clientX; y = e.clientY;
    });
  }

  /* --- Visionneuse ------------------------------------------------------- */
  var boutons = Array.prototype.slice.call(document.querySelectorAll("[data-cliche]"));
  var boite = document.querySelector("[data-visionneuse]");

  if (!boutons.length || !boite || typeof boite.showModal !== "function") return;

  var affichee = boite.querySelector("img");
  var position = 0;

  function montrer(i) {
    position = (i + boutons.length) % boutons.length;
    var source = boutons[position].querySelector("img");
    // currentSrc donne la taille réellement choisie par le navigateur
    affichee.src = source.currentSrc || source.src;
    affichee.alt = source.alt;
    boite.querySelector("[data-rang]").textContent =
      position + 1 + " sur " + boutons.length;
  }

  boutons.forEach(function (b, i) {
    b.addEventListener("click", function () {
      montrer(i);
      boite.showModal();
    });
  });

  boite.querySelector("[data-prec]").addEventListener("click", function () { montrer(position - 1); });
  boite.querySelector("[data-suiv]").addEventListener("click", function () { montrer(position + 1); });
  boite.querySelector("[data-fermer]").addEventListener("click", function () { boite.close(); });

  boite.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { e.preventDefault(); montrer(position - 1); }
    if (e.key === "ArrowRight") { e.preventDefault(); montrer(position + 1); }
  });

  boite.addEventListener("click", function (e) {
    if (e.target === boite) boite.close();
  });
})();
