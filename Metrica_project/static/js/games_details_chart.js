const ctx = document.getElementById("gamesDetailsChart");
const { labels, data } = serverData.gamesDetailsChart;

const colors = [
  "rgba(255, 99, 132, 0.2)",
  "rgba(54, 162, 235, 0.2)",
  "rgba(255, 206, 86, 0.2)",
  "rgba(75, 192, 192, 0.2)",
  "rgba(153, 102, 255, 0.2)",
  "rgba(255, 159, 64, 0.2)",
];

console.log(serverData);

const gamesDetailsChart = new Chart(ctx, {
  type: "horizontalBar",
  data: {
    labels,
    datasets: [
      {
        data,
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        barPercentage: 0.95,
        categoryPercentage: 1,
      },
    ],
  },
  options: {
    legend: false,
    scales: {
      xAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  },
});
