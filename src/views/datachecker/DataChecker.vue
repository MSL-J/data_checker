<template>
  <div class="wrapper">
    <div class="animated fadeIn">
      <b-card header-tag="header" footer-tag="footer">
        <div slot="header" class="progressHeader">
          <b-form-group>
            <b-form-select
              id="basicSelect"
              :plain="true"
              :options="['color', 'category', 'brand']"
              v-on:change="selected"
              value="null"
            ></b-form-select>
          </b-form-group>
          <strong>진행률</strong>
        </div>

        <div class="noFilter" v-if="!which && !isDone">Please select a filter</div>

        <div v-if="which && !submitted && !isDone" class="modeSelect">
          <div class="selectSaveNMode">
            <strong>Save on DataBase?</strong>
            <b-form-group>
              <b-form-select
                id="basicSelect"
                :plain="true"
                :options="[`Yes please`, 'No thanks']"
                v-on:change="selectSave"
                value="null"
              ></b-form-select>
            </b-form-group>
          </div>
          <div class="selectSaveNMode">
            <strong>Mode?</strong>
            <b-form-group>
              <b-form-select
                id="basicSelect"
                :plain="true"
                :options="[`Test`, 'Dev', 'Real']"
                v-on:change="selectMode"
                value="null"
              ></b-form-select>
            </b-form-group>
          </div>
          <div class="buffer"></div>
          <b-button variant="success" v-on:click="submit">Start Mapping!</b-button>
        </div>

        <div
          class="noFilter"
          v-if="which && submitted && !isDone"
        >Mapping In Progress... Please wait</div>

        <div v-if="which && submitted && isDone">
          <div class="barNperc">
            <div class="bars">
              <b-progress
                :value="counter"
                :max="max"
                show-progress
                animated
                height="2rem"
                variant="success"
                :precision="1"
              ></b-progress>
            </div>
            <div class="perc">
              <span>{{ counter }}%</span>
            </div>
          </div>

          <div class="status">
            <strong>
              <i class="cui-circle-check icons font-2xl d-block mt-4"></i>
              <span>{{ status.done }}</span>
            </strong>
            <strong>
              <i class="cui-circle-x icons font-2xl d-block mt-4"></i>
              <span>{{ status.undone }}</span>
            </strong>
            <strong>
              <i class="cui-wrench icons font-2xl d-block mt-4"></i>
              <span>{{ status.needALook }}</span>
            </strong>
          </div>
        </div>
      </b-card>
    </div>

    <b-card header-tag="header" footer-tag="footer">
      <div slot="header">
        <strong>Data checker log</strong>
      </div>
      <div class="logSpace">
        <ul v-if="logFetched" class="withLog">
          <li v-for="(log, i) in logs" v-bind:key="i" class="eachLog">
            <strong>{{ log.date }}</strong> :
            <strong>{{ log.mode }}</strong> mode에서 실행되었습니다.
          </li>
        </ul>
        <div v-else class="withoutLog"></div>
      </div>
    </b-card>
  </div>
</template>

<style lang="scss">
.progressHeader {
  display: flex;
  align-items: center;
  width: 30%;
  fieldset {
    flex: 2;
    margin: 0;
  }
  strong {
    flex: 1;
    text-align: center;
  }
}

.modeSelect {
  display: flex;
  align-items: center;
  width: 90%;
  margin: 0 auto;
  .selectSaveNMode {
    flex: 1;
    margin-right: 1.5rem;
  }
  .buffer {
    flex: 0.5;
  }
  button {
    flex: 0.4;
    height: 70%;
  }
}

.barNperc {
  display: flex;
  .bars {
    flex: 8;
    .progress-bar {
      font-size: 18px;
    }
  }
  .perc {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    span {
      font-size: 25px;
      font-weight: bold;
    }
  }
}

.status {
  display: flex;
  width: 50%;
  justify-content: space-between;
  margin-top: 1rem;
  strong {
    display: flex;
    align-items: center;
    width: 33.33%;
    margin-right: 1rem;
    i {
      margin: 0 !important;
    }
    span {
      margin-left: 1rem;
      font-size: 17px;
    }
  }
}

.noFilter {
  text-align: center;
  font-weight: bold;
  font-size: 25px;
  padding: 15px 0;
}

.logSpace {
  height: 35vh;
  overflow: auto;
  .withLog {
    height: 100%;
    margin: 0;
    .eachLog {
      margin-bottom: 10px;
      font-size: 14px;
    }
  }
  .withoutLog {
    height: 100%;
  }
}
</style>

<script>
import { state as S } from "@/store";
require("dotenv").config();

export default {
  data() {
    return {
      which: "",
      whetherSave: null,
      whichMode: "",
      submitted: false,
      isDone: false,
      logFetched: false,
      logs: [],
      counter: 20,
      max: 100,
      status: {
        done: 0,
        undone: 0,
        needALook: 0,
      },
    };
  },
  methods: {
    selected(which) {
      console.log(which);
      this.which = which;
      this.whichMode = "";
      this.submitted = false;
      this.isDone = false;
    },

    selectSave(which) {
      console.log(which);
      if (which == "Yes please") {
        this.whetherSave = true;
      } else {
        this.whetherSave = false;
      }
    },

    selectMode(which) {
      console.log(which);
      this.whichMode = which.toLowerCase();
      console.log(this.whichMode);
    },

    submit() {
      this.submitted = true;
      console.log(this.whichMode);
      console.log(process.env.VUE_APP_API);
      fetch(`${process.env.VUE_APP_API}/newmapping`, {
        method: "POST",
        headers: {
          "Access-Control-Allow-Origin": "http://localhost:8080",
          Accept: "application/json",
          "Content-Type": "application/json",
          mode: "cors",
        },
        body: JSON.stringify({
          save: this.whetherSave,
          mode: this.whichMode,
        }),
      })
        .then((res) => res.json())
        .then((res) => {
          console.log(res);
          S.check[`${this.which}`] = (
            (res[`${this.which}`].CURRENT * 100) /
            res[`${this.which}`].TOTAL
          ).toFixed(1);
          this.status.done = res[0][`${this.which}`].CURRENT.toLocaleString();
          this.status.undone = (
            res[`${this.which}`].TOTAL -
            res[`${this.which}`].CURRENT -
            res[`${this.which}`].NODATA
          ).toLocaleString();
          this.status.needALook = res[0][
            `${this.which}`
          ].NODATA.toLocaleString();
        })
        .then(() => {
          this.counter = Number(S.check[`${this.which}`]);
          this.isDone = true;
        })
        .then(() => {
          this.getLog();
        });
    },
    getLog() {
      this.logs = [];
      fetch(`${process.env.VUE_APP_API}/check`)
        .then((res) => res.json())
        .then((res) => {
          for (let i in res) {
            this.logs.unshift({
              date: res[i][`date`],
              mode: res[i][`mode`],
            });
          }
        })
        .then(() => {
          this.logFetched = true;
        });
    },
  },

  mounted() {
    this.getLog();
  },
  beforeDestroy() {},
};
</script>
