// Selecionando o ícone do hambúrguer e o menu móvel
const hamburgerIcon = document.getElementById('hamburger-icon');
const mobileNav = document.getElementById('mobile-nav');

// Função para alternar o menu
hamburgerIcon.addEventListener('click', function (event) {
  // Previne a propagação do clique para o documento
  event.stopPropagation();
  mobileNav.classList.toggle('active');
});

// Função para fechar o menu se clicar fora dele
document.addEventListener('click', function (event) {
  // Verifica se o clique foi fora do menu hamburguer e do próprio menu
  if (!mobileNav.contains(event.target) && !hamburgerIcon.contains(event.target)) {
    mobileNav.classList.remove('active');
  }
});
