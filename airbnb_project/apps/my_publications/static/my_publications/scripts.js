document.addEventListener("DOMContentLoaded", () => {
  const publicationsBtn = document.getElementById("publications-btn");
  const proposalsBtn = document.getElementById("proposals-btn");
  const sectionTitle = document.getElementById("section-title");
  const addBtn = document.getElementById("add-btn");

  addBtn.style.display = "none";

  // Función para mostrar publicaciones
  publicationsBtn.addEventListener("click", () => {
    sectionTitle.textContent = "Publicaciones";
    addBtn.style.display = "none";
    removeEstadoFromCards();
  });

  // Función para mostrar propuestas
  proposalsBtn.addEventListener("click", () => {
    sectionTitle.textContent = "Propuestas";
    addBtn.style.display = "inline-block";
    addEstadoToCards();
  });

  function addEstadoToCards() {
    const cards = document.querySelectorAll(".card .card-info");
    for (const cardInfo of cards) {
      if (!cardInfo.querySelector(".estado")) {
        const estado = document.createElement("p");
        estado.textContent = "Estado:";
        estado.classList.add("estado");
        cardInfo.appendChild(estado);
      }
    }
  }

  function removeEstadoFromCards() {
    const estados = document.querySelectorAll(".card .card-info .estado");
    for (const estado of estados) {
      estado.remove();
    }
  }
});
