document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("proposal-form").addEventListener("submit", function (event) {
    // Si quieres hacer validaciones o mostrar un mensaje antes
    setTimeout(function () {
      globalThis.location.href = "/my_publications/"; // URL destino
    }, 500); // Espera 0.5s antes de redirigir
  });

  window.onload = function () {
    let toast = document.getElementById("toast");
    toast.classList.add("show");
    setTimeout(function () {
      toast.classList.remove("show");
    }, 3500);
  };
});
