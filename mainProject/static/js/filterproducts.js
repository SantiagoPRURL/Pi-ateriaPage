window.onload = function () {
  const btnSearch = document.getElementById("btn-search");

  document.addEventListener("click", async (event) => {
    event.preventDefault();

    if (event.target == btnSearch) {
      console.log("Se realizo el click");

      console.log(document.getElementById("search").value);

      const data = { search: document.getElementById("search").value };

      const response = await fetch("/market-search/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const dataResponse = await response.json();

      console.log(dataResponse)

      console.log(dataResponse.results)
      const resultsR = dataResponse.results;

      let imagen = 1;

      const dataarray = resultsR.forEach((value, key) => {
        console.log(value.image_url);
        imagen = value.image_url;
      });
      const img = document.createElement("img");
      img.src = imagen || "default_image.png";
      img.width = 500;
      img.height = 400;
      document.body.appendChild(img);
    }
  });
};
