<script>
import { Pie } from "vue-chartjs";
import { state as S } from "@/store";

export default {
  extends: Pie,
  mounted() {
    this.renderChart(
      {
        labels: ["Not mapped", "Color Unknown", "Mapped"],
        datasets: [
          {
            backgroundColor: ["gold", "#DD1B16", "#41B883"],
            data: [S.pie.false, S.pie.noColor, S.pie.true]
          }
        ]
      },
      { responsive: true, maintainAspectRatio: false }
    );
  }
};
</script>
