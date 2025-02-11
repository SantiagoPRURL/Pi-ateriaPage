document.addEventListener("DOMContentLoaded", () => {
  console.log("Iniciando...");

  const searchInput = document.getElementById("search");
  const btnSearch = document.getElementById("btn-search");
  const btnNext = document.getElementById("next-button");
  const btnPrevious = document.getElementById("prev-button");

  // Obtener parámetros de la URL
  const params = new URLSearchParams(window.location.search);
  const searchParam = params.get("search");
  const pageParam = params.get("page");

  // Verificar si la URL es "/market-search/" sin parámetros
  if (!searchParam && !pageParam) {
    btnNext.hidden = true;
    btnPrevious.hidden = true;
  } else {
    btnNext.hidden = false;
    btnPrevious.hidden = false;
  }

  btnSearch.addEventListener("click", () => {
    const searchTerm = searchInput.value.trim();
    if (searchTerm) {
      window.location.href = `/market-search/?search=${encodeURIComponent(
        searchTerm
      )}&page=1`;
    }
  });

  if (searchParam) {
    searchInput.value = searchParam;
    searchInput.hidden = true;
    btnSearch.hidden = true;
    fetchProducts(searchParam, pageParam || 1);
  }
});

async function fetchProducts(search, page) {
  try {
    const btnNext = document.getElementById("next-button");
    const btnPrevious = document.getElementById("prev-button");
    const resultsHeader = document.getElementById("results-header");

    const response = await fetch(
      `/market-search/api/?search=${encodeURIComponent(search)}&page=${page}`
    );
    const data = await response.json();

    if (!data.next) {
      btnNext.disabled = true;
    }

    if (!data.previous) {
      btnPrevious.disabled = true;
    }

    resultsHeader.innerHTML = `Resultados para "${search}"`;

    document.addEventListener("click", (event1) => {
      if (event1.target == btnNext) {
        if (data.next) {
          const url = new URL(data.next);
          const paramsAux = new URLSearchParams(url.search);
          const searchParamAux = paramsAux.get("search");
          const pageParamAux = paramsAux.get("page");

          if (searchParamAux) {
            window.location.href = `/market-search/?search=${encodeURIComponent(
              searchParamAux
            )}&page=${pageParamAux}`;
          }
        }
      }
    });

    document.addEventListener("click", (event2) => {
      if (event2.target == btnPrevious) {
        if (data.previous) {
          const url = new URL(data.previous);
          const paramsAux = new URLSearchParams(url.search);
          const searchParamAux = paramsAux.get("search");
          const pageParamAux = paramsAux.get("page") || 1;

          if (searchParamAux) {
            window.location.href = `/market-search/?search=${encodeURIComponent(
              searchParamAux
            )}&page=${pageParamAux}`;
          }
        }
      }
    });

    if (response.ok) {
      updateProducts(data.results);
    } else {
      alert("No se encontraron productos.");
    }
  } catch (error) {
    console.error("Error al obtener productos:", error);
  }
}

function updateProducts(products) {
  const container = document.getElementById("product-container");

  container.innerHTML = "";

  products.forEach((product) => {
    const div = document.createElement("div");

    div.innerHTML = ` 
            <img src="${product.image_url || "default_image.png"}" width="200">
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p> $ ${product.price}</p>
        `;
    container.appendChild(div);
  });
}
