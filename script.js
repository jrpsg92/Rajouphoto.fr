/* Raju Sinniah — comportements partagés.
   Tout est optionnel : sans JS, la navigation et les photographies
   restent accessibles. */
(function () {
  "use strict";

  /* --- Menu ------------------------------------------------------------- */
  var bascule = document.querySelector("[data-bascule]");
  var nav = document.querySelector("[data-nav]");

  if (bascule && nav) {
    bascule.hidden = false;
    nav.dataset.ouvert = "false";
    bascule.setAttribute("aria-expanded", "false");

    bascule.addEventListener("click", function () {
      var ouvert = bascule.getAttribute("aria-expanded") === "true";
      bascule.setAttribute("aria-expanded", String(!ouvert));
      nav.dataset.ouvert = String(!ouvert);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && bascule.getAttribute("aria-expanded") === "true") {
        bascule.setAttribute("aria-expanded", "false");
        nav.dataset.ouvert = "false";
        bascule.focus();
      }
    });
  }

  /* --- Visionneuse ------------------------------------------------------ */
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
