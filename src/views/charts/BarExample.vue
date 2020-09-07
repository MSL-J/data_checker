<script>
import { Bar } from "vue-chartjs";
import { CustomTooltips } from "@coreui/coreui-plugin-chartjs-custom-tooltips";
import { state as S } from "@/store";

export default {
  extends: Bar,
  mounted() {
    // Overwriting base render method with actual data.
    this.renderChart(
      {
        labels: Object.keys(S.bar),
        datasets: [
          {
            label: "보유량",
            backgroundColor: Object.keys(S.bar),
            data: Object.values(S.bar),
            borderWidth: 1,
          },
        ],
      },
      {
        legend: {
          display: false,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                min: 0,
              },
            },
          ],
        },
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
          enabled: false,
          custom: CustomTooltips,
          intersect: true,
          mode: "index",
          position: "average",
          callbacks: {
            labelColor: function (tooltipItem, chart) {
              return {
                backgroundColor:
                  chart.data.datasets[tooltipItem.datasetIndex].backgroundColor,
              };
            },
          },
        },
      }
    );
  },
};
</script>
