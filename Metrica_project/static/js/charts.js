const ctx = document.getElementById("myChart");

const myChart = new Chart(ctx, {
  type: "horizontalBar",
  data: {
    labels: serverData.labels,
    datasets: [
      {
        data: serverData.data,
      },
    ],
  },
  options: {
    legend: { display: false },
  },
});
