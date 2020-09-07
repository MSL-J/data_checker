<template>
  <div class="animated fadeIn">
    <div class="top-charts">
      <b-card header="전체 처리량">
        <div class="chart-wrapper" v-if="pieFetched">
          <pie-example chartId="chart-pie-01" />
        </div>
      </b-card>

      <b-card header="컬러별 보유량">
        <div class="chart-wrapper" v-if="barFetched">
          <bar-example chartId="chart-bar-01" />
        </div>
      </b-card>
    </div>

    <b-card header="처리량 변화">
      <div class="chart-wrapper" v-if="lineFetched">
        <line-example chartId="chart-line-01" />
      </div>
    </b-card>
  </div>
</template>

<style lang="scss">
.top-charts {
  display: flex;
  .card {
    canvas {
      max-height: 40vh;
    }
    &:first-of-type {
      margin-right: 15px;
      flex: 1;
    }

    &:last-of-type {
      flex: 2;
    }
  }
}
</style>

<script>
import BarExample from "../charts/BarExample";
import LineExample from "../charts/LineExample";
import PieExample from "../charts/PieExample";
import { state as S } from "@/store";
require("dotenv").config();

export default {
  name: "Dashboard",
  components: {
    BarExample,
    LineExample,
    PieExample,
  },

  data() {
    return {
      pieFetched: false,
      barFetched: false,
      lineFetched: false,
    };
  },

  created() {
    S.line.date = [];
    S.line.color = [];
    S.line.category = [];
    S.line.brand = [];
    fetch(`${process.env.VUE_APP_API}/piebarchart`)
      .then((res) => res.json())
      .then((res) => {
        console.log("piebarchart", res);
        let mapped = res.color.MAPPED
          ? res.color.MAPPED + res.color.CURRENT
          : res.color.CURRENT;
        S.pie.true = ((mapped * 100) / res.color.TOTAL).toFixed(2);
        S.pie.false = (
          ((res.color.TOTAL - mapped - res.color.NODATA) * 100) /
          res.color.TOTAL
        ).toFixed(2);
        S.pie.noColor = ((res.color.NODATA * 100) / res.color.TOTAL).toFixed(2);
        S.bar = res.color.MAPPED_RESULT;
      })
      .then(() => {
        this.pieFetched = true;
        this.barFetched = true;
      });

    fetch(`${process.env.VUE_APP_API}/linechart`)
      .then((res) => res.json())
      .then((res) => {
        console.log("linechart", res);
        for (let i in res) {
          console.log("line", res[i]);

          S.line.date.includes(res[i].date.split(" ")[0])
            ? ""
            : (S.line.date.unshift(res[i].date.split(" ")[0]),
              ["color", "category", "brand"].map((filter) => {
                if (res[i][filter]) {
                  let mapped = res[i][filter].MAPPED
                    ? res[i][filter].MAPPED + res[i][filter].CURRENT
                    : res[i][filter].CURRENT;
                  S.line[filter].unshift(
                    ((mapped * 100) / res[i][filter].TOTAL).toFixed(1)
                  );
                }
              }));
        }
      })
      .then(() => {
        console.log("thisisLine", S.line);
        this.lineFetched = true;
      });
  },
};
</script>
