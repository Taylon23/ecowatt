document.getElementById("id_cep").addEventListener("blur", function () {
  const cep = this.value.replace(/\D/g, "");
  if (cep.length === 8) {
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
      .then((response) => response.json())
      .then((data) => {
        if (!data.erro) {
          document.getElementById("id_endereco").value = data.logradouro;
          document.getElementById("id_cidade").value = data.localidade;
          document.getElementById("id_estado").value = data.uf;
        } else {
          alert("CEP não encontrado.");
        }
      })
      .catch((error) => {
        console.error("Erro ao consultar CEP:", error);
      });
  }
});
