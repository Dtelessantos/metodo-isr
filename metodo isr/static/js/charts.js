document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('transactionsChart').getContext('2d');
    
    fetch('/dashboard_data')
      .then(response => response.json())
      .then(data => {
        var chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Total Investido', 'Total de Retorno', 'Lucro'],
            datasets: [{
              label: 'Valores',
              data: data,
              backgroundColor: ['#007bff', '#28a745', '#ffc107']
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false, // Para garantir que o gráfico use o espaço disponível
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      });
  });
  