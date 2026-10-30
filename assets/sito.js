// Ars Docendi — sito pubblico: menu, comparsa allo scorrimento, contatori.
// Senza JavaScript la pagina resta completa: i numeri sono già scritti nel markup.
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  var testata = document.querySelector('.testata');
  var bottone = document.querySelector('.pulsante-menu');
  if (testata && bottone) {
    bottone.addEventListener('click', function () {
      var aperto = testata.classList.toggle('aperta');
      bottone.setAttribute('aria-expanded', aperto ? 'true' : 'false');
    });
  }

  var fermo = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var formato = new Intl.NumberFormat('it-IT');

  function conta(el) {
    var fine = parseInt(el.getAttribute('data-valore'), 10);
    var suffisso = el.getAttribute('data-suffisso') || '';
    var t0 = performance.now(), durata = 1600;
    function passo(ora) {
      var p = Math.min(1, (ora - t0) / durata);
      el.textContent = formato.format(Math.round(fine * (1 - Math.pow(1 - p, 3)))) + suffisso;
      if (p < 1) requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
  }

  if (!fermo && 'IntersectionObserver' in window) {
    var osservatore = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (!v.isIntersecting) return;
        osservatore.unobserve(v.target);
        if (v.target.hasAttribute('data-valore')) conta(v.target);
        else v.target.classList.add('visibile');
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('[data-compari], [data-valore]').forEach(function (el) { osservatore.observe(el); });
  } else {
    document.querySelectorAll('[data-compari]').forEach(function (el) { el.classList.add('visibile'); });
  }

})();
