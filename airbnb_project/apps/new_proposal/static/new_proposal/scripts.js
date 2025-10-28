document.addEventListener("DOMContentLoaded", () => {
  const typeField = document.getElementById("id_type");
  const subtypeField = document.getElementById("id_subtype");
  const locationFieldWrapper = document.getElementById("id_location").parentElement;
  const startDateWrapper = document.getElementById("id_start_date").parentElement;
  const endDateWrapper = document.getElementById("id_end_date").parentElement;
  const form = document.getElementById("proposal-form");

  form.addEventListener("submit", function (event) {
    setTimeout(() => {
      globalThis.location.href = "/my_publications/";
    }, 500);
  });

  const toast = document.getElementById("toast");
  if (toast) {
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3500);
  }

  function loadSubtypes(selectedType) {
    if (!selectedType) return;
    fetch(`/get-subtypes/?type=${selectedType}`)
      .then(response => response.json())
      .then(data => {
        subtypeField.innerHTML = ""; // limpiar
        data.subtypes.forEach(subtype => {
          const option = document.createElement("option");
          option.value = subtype;
          option.textContent = subtype;
          subtypeField.appendChild(option);
        });
      })
      .catch(error => console.error("Error cargando subtipos:", error));
  }

  typeField.addEventListener("change", function () {
    loadSubtypes(this.value);
  });

  if (typeField.value) {
    loadSubtypes(typeField.value);
  }
  
  function toggleFields() {
    const selectedType = typeField.value;
    if (selectedType === "Alojamiento") {
      locationFieldWrapper.style.display = "block";
      startDateWrapper.style.display = "block";
      endDateWrapper.style.display = "block";
    } else {
      locationFieldWrapper.style.display = "none";
      startDateWrapper.style.display = "none";
      endDateWrapper.style.display = "none";
    }
  }

  toggleFields();
  typeField.addEventListener("change", toggleFields);
});