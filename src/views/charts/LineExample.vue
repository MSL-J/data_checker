<script>
import { Line } from "vue-chartjs";
import { CustomTooltips } from "@coreui/coreui-plugin-chartjs-custom-tooltips";
import { hexToRgba } from "@coreui/coreui-pro/dist/js/coreui-utilities";
import { state as S } from "@/store";

export default {
  components: {
    hexToRgba,
    CustomTooltips,
  },
  extends: Line,
  mounted() {
    this.renderChart(
      {
        labels: S.line.date,
        datasets: [
          {
            label: "Color",
            fill: false,
            borderColor: "green",
            data: S.line.color,
          },
          {
            label: "Category",
            fill: false,
            borderColor: "red",
            data: S.line.category,
          },
          {
            label: "Brand",
            fill: false,
            borderColor: "blue",
            data: S.line.brand,
          },
        ],
      },
      {
        scales: {
          yAxes: [
            {
              ticks: {
                min: 0,
                max: 100,
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
          position: "nearest",
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
