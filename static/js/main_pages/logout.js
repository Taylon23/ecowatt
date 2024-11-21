function confirmLogout() {
    // Exibe uma mensagem de confirmação
    const userConfirmed = confirm("Você tem certeza que deseja encerrar a sessão?");
    
    // Se o usuário confirmar, envia o formulário
    if (userConfirmed) {
      document.getElementById("logout-form").submit();
    }
  }