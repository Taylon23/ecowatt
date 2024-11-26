  // Obtendo os dados do atributo data-dados
  const graficoDadosDiv = document.getElementById('grafico-dados');
  const dadosGrafico = JSON.parse(document.getElementById('dados_grafico').textContent);

  // Cores customizadas para cada barra
  const cores = [
    'rgba(75, 192, 192, 0.2)', // Meta Gasto Mensal
    'rgba(153, 102, 255, 0.2)', // Meta Consumo Mensal
    'rgba(255, 159, 64, 0.2)', // Consumo Atual
    'rgba(255, 99, 132, 0.2)', // Custo Atual
    'rgba(54, 162, 235, 0.2)', // Diferença kWh
    'rgba(255, 205, 86, 0.2)'  // Diferença Custo
  ];

  // Configurando o gráfico
  const ctx = document.getElementById('graficoPlano').getContext('2d');
  const graficoPlano = new Chart(ctx, {
    type: 'bar', // Tipo do gráfico
    data: {
      labels: dadosGrafico.categorias, // Categorias no eixo Y
      datasets: [{
        label: 'Valores do Plano', // Label único para o conjunto de dados
        data: dadosGrafico.valores, // Valores no eixo X
        backgroundColor: cores, // Cores customizadas para cada barra
        borderColor: cores.map(cor => cor.replace('0.2', '1')), // Cor de borda para cada barra
        borderWidth: 1 // Largura da borda
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
        tooltip: {
          enabled: true,
        },
        datalabels: {
          anchor: 'end', // Posiciona os rótulos no final das barras (em cima)
          align: 'start', // Alinha o texto no início (acima da barra)
          color: 'black', // Cor do texto
          font: {
            weight: 'bold', // Peso da fonte para destaque
          },
          formatter: (value) => value.toFixed(2) // Formatação para exibir os valores
        }
      },
      scales: {
        x: {
          beginAtZero: true
        },
        y: {
          beginAtZero: true
        }
      }
    },
    plugins: [ChartDataLabels] // Ativando o plugin para exibir os rótulos
  });