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
