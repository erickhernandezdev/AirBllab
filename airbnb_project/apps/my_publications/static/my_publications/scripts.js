document.addEventListener("DOMContentLoaded", () => {
  const publicationsBtn = document.getElementById("publications-btn");
  const proposalsBtn = document.getElementById("proposals-btn");
  const sectionTitle = document.getElementById("section-title");
  const addBtn = document.getElementById("add-btn");
  const cards = document.querySelectorAll('.card');

  addBtn.style.display = "none";

  // Función para mostrar publicaciones
  publicationsBtn.addEventListener("click", () => {
    sectionTitle.textContent = "Publicaciones";
    addBtn.style.display = "none";
    for (const card of cards) {
      if (card.dataset.status === 'Aprobado') {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    }
  });

  // Función para mostrar propuestas
  proposalsBtn.addEventListener("click", () => {
    sectionTitle.textContent = "Propuestas";
    addBtn.style.display = "inline-block";
    addEstadoToCards();
    for (const card of cards) {
      if (card.dataset.status === 'Pendiente' || card.dataset.status === 'Rechazado') {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    }
  });

  window.onload = () => {
    for (const card of cards) {
      if (card.dataset.status === 'Aprobado') {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    }
  };

  addBtn.addEventListener("click", () => {
    globalThis.location.href = "/new_proposal/";
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
});
