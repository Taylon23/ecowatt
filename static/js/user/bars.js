// Adiciona um evento de clique ao ícone de engrenagem
document.getElementById("bars-icon").addEventListener("click", function () {
  var submenu = document.getElementById("submenu");
  if (submenu.style.display === "block") {
    submenu.style.display = "none"; // Esconde o submenu
  } else {
    submenu.style.display = "block"; // Mostra o submenu
  }
});

// Fecha o submenu ao clicar fora dele
document.addEventListener("click", function (event) {
  var cogContainer = document.querySelector(".cog-container");
  var submenu = document.getElementById("submenu");
  if (!cogContainer.contains(event.target)) {
    submenu.style.display = "none"; // Esconde o submenu
  }
});
