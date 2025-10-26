document.addEventListener("DOMContentLoaded", () => {
  const publicationsBtn = document.getElementById("publications-btn");
  const proposalsBtn = document.getElementById("proposals-btn");
  const sectionTitle = document.getElementById("section-title");
  const addBtn = document.getElementById("add-btn");
  const searchInput = document.getElementById('search-input');
  const searchBtn = document.getElementById('search-btn');
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
    const cardsInfo = document.querySelectorAll(".card .card-info");
    for (const cardInfo of cardsInfo) {
      if (cardInfo.querySelector(".status")) {
        const status = cardInfo.querySelector(".status");
        status.textContent = "Estado: " + cardInfo.parentElement.dataset.status;
      } else {
        const status = document.createElement("p");
        status.textContent = "Estado: " + cardInfo.parentElement.dataset.status;
        status.classList.add("status");
        cardInfo.appendChild(estado);
      }
    }
  }

  // Función de búsqueda
  function filterCards() {
    const query = searchInput.value.toLowerCase();
    const section = sectionTitle.textContent.toLowerCase();

    for (const card of cards) {
      const text = card.querySelector('.card-info').innerText.toLowerCase();
      const status = card.dataset.status.toLowerCase();

      let showCard = false;

      if (
        (section.includes('publicaciones') && status === 'aprobado') ||
        (section.includes('propuestas') && (status === 'pendiente' || status === 'rechazado'))
      ) {
        showCard = text.includes(query);
      }

      card.style.display = showCard ? 'block' : 'none';
    }
  }

  // Buscar al presionar el botón
  searchBtn.addEventListener('click', filterCards);

  // Búsqueda en tiempo real mientras se escribe
  searchInput.addEventListener('input', filterCards);
});
