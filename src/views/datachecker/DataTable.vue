<template>
  <div class="animated">
    <b-card>
      <b-card-header>
        <i class="icon-menu mr-1"></i>
        <strong>Data Table</strong>
      </b-card-header>
      <b-card-body>
        <div class="selectNsave">
          <b-form-group>
            <b-form-select
              id="basicSelect"
              :plain="true"
              :options="['Color', 'Category', 'Brand']"
              value="Color"
              v-on:change="(e) => whichToShow(e)"
            ></b-form-select>
          </b-form-group>
          <b-button variant="success" v-on:click="setChange">Save Changes</b-button>
        </div>

        <v-client-table
          :columns="columns"
          :data="data"
          :options="options"
          :theme="theme"
          id="dataTable"
        >
          <b-form-select
            slot="main_color"
            slot-scope="props"
            id="basicSelect"
            :plain="true"
            :options="defaultColors"
            :value="props.row.main_color"
            v-on:change="(e) => mainColorChanged(props.row._id, e)"
          ></b-form-select>
          <div
            slot="color_kor"
            slot-scope="{ row, update, setEditing, isEditing, column }"
            class="valueWrapper"
          >
            <span
              class="orgValue"
              @click="setEditing(true), whichOne(row._id, column)"
              v-if="
                !isEditing() ||
                whichRowEdit !== row._id ||
                whichColumnEdit !== column
              "
            >{{ row.color_kor }}</span>
            <span
              v-if="
                isEditing() &&
                whichRowEdit === row._id &&
                whichColumnEdit === column
              "
              class="selectable"
            >
              <input type="text" v-model="row.color_kor" />
              <button
                type="button"
                @click="
                  update(row.color_kor);
                  setEditing(false);
                  mainKorChanged(row._id, row.color_kor);
                "
              >Submit</button>
            </span>
          </div>
          <div
            slot="color_value"
            slot-scope="{ row, update, setEditing, isEditing, column }"
            class="valueWrapper"
          >
            <span
              @click="setEditing(true), whichOne(row._id, column)"
              class="orgValue"
              v-if="
                !isEditing() ||
                whichRowEdit !== row._id ||
                whichColumnEdit !== column
              "
            >{{ row.color_value }}</span>
            <span
              v-if="
                isEditing() &&
                whichRowEdit === row._id &&
                whichColumnEdit === column
              "
              class="selectable"
            >
              <input type="text" v-model="row.color_value" />
              <button
                type="button"
                @click="
                  update(row.color_value);
                  setEditing(false);
                  mainEngChanged(row._id, row.color_kor);
                "
              >Submit</button>
            </span>
          </div>
          <a slot="Edit" slot-scope="props" class="fa fa-edit" :href="edit(props.row.id)">Delete</a>
        </v-client-table>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import Vue from "vue";
import { ClientTable, Event } from "vue-tables-2";
import { state as S } from "@/store";
import select from "./select";
require("dotenv").config();

Vue.use(ClientTable);

export default {
  name: "DataTable",
  components: {
    ClientTable,
    Event,
  },
  methods: {
    whichOne(rowId, columnId) {
      this.whichRowEdit = rowId;
      this.whichColumnEdit = columnId;
    },
    whichToShow(e) {
      console.log(e);
      this.dataFetched = false;
      switch (e) {
        case "Color":
          this.showColor();
          break;
        case "Category":
          this.showCategory();
          break;
      }
    },
    showColor() {
      console.log("this", process.env);
      fetch(`${process.env.VUE_APP_API}/datatable/color`)
        .then((res) => res.json())
        .then((res) => {
          this.data = res;
          this.columns = ["main_color", "color_kor", "color_value", "edit"];
          this.options.headings = {
            main_color: "Main Color",
            color_kor: "KOR (click to update)",
            color_value: "ENG (click to update)",
          };
          this.options.editableColumns = ["color_kor", "color_value"];
          this.options.sortable = ["main_color"];
          this.options.filterable = ["main_color", "color_kor", "color_value"];
          for (let i in res) {
            if (!this.defaultColors.includes(res[i]["main_color"]))
              this.defaultColors.unshift(res[i]["main_color"]);
          }
        })
        .then(() => {
          this.dataFetched = true;
        });
    },
    showCategory() {
      console.log("this", process.env);
      fetch(`${process.env.VUE_APP_API}/datatable/category`)
        .then((res) => res.json())
        .then((res) => {
          this.data = res;
          this.columns = [
            "shop_id",
            "original_category",
            "balaan_category",
            "edit",
          ];
          this.options.headings = {
            main_color: "Shop Id",
            color_kor: "Original Category",
            color_value: "Balaan Category",
          };
          this.options.sortable = ["shop_id", "balaan_category"];
          this.options.filterable = [
            "shop_id",
            "original_category",
            "balaan_category",
          ];
        })
        .then(() => {
          this.dataFetched = true;
        });
    },
    setChange() {
      console.log(this.toChange);
      fetch(`${process.env.VUE_APP_API}/newcolor`, {
        method: "POST",
        body: JSON.stringify(this.toChange),
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });
      this.toChange = [];
    },
    mainColorChanged(rowId, newColor) {
      console.log(rowId, newColor);
      console.log(this.toChange);
      this.toChange.push({
        id: rowId,
        main_color: newColor,
      });
    },
    async mainKorChanged(rowId, newColor) {
      console.log(rowId, newColor);
      console.log(this.toChange);
      await this.toChange.push({
        id: rowId,
        color_kor: newColor,
      });
      this.setChange();
    },
    async mainEngChanged(rowId, newColor) {
      console.log(rowId, newColor);
      console.log(this.toChange);
      await this.toChange.push({
        id: rowId,
        color_value: newColor,
      });
      this.setChange();
    },
  },
  data: function () {
    return {
      whichRowEdit: null,
      whichColumnEdit: null,
      dataFetched: false,
      toChange: [],
      columns: [],
      defaultColors: [],
      data: null,
      options: {
        headings: {},
        sortable: [],
        filterable: [],
        editableColumns: [],
        sortIcon: {
          base: "fa",
          up: "fa-sort-asc",
          down: "fa-sort-desc",
          is: "fa-sort",
        },

        pagination: {
          chunk: 5,
          edge: false,
          nav: "scroll",
        },
      },
      useVuex: false,
      theme: "bootstrap4",
      template: "default",
    };
  },
  created() {
    this.dataFetched = false;
    this.showColor();
  },
};
</script>

<style lang="scss">
.selectNsave {
  display: flex;
  justify-content: space-between;
  width: 95%;
  margin: 0 auto;
  .form-group {
    width: 30%;
  }
  button {
    margin-bottom: 1rem;
  }
}

#dataTable {
  width: 95%;
  margin: 0 auto;

  .valueWrapper {
    .orgValue {
      cursor: pointer;
    }
  }

  .selectable {
    display: flex;
    justify-content: space-between;
    button {
      border-radius: 8px;
      border: none;
      background-color: mediumseagreen;
      color: white;
    }
  }

  .VuePagination {
    text-align: center;
    justify-content: center;
  }

  .vue-title {
    text-align: center;
    margin-bottom: 10px;
  }

  .VueTables__search-field {
    display: flex;
  }
  .VueTables__search-field input {
    margin-left: 0.25rem;
  }

  .VueTables__limit-field {
    display: flex;
  }

  .VueTables__limit-field select {
    margin-left: 0.25rem !important;
  }

  .VueTables__table th {
    text-align: center;
  }

  .VueTables__table td {
    width: 30%;
  }
  .VueTables__table td:hover span.glyphicon-edit {
    visibility: visible !important;
  }
}
</style>
