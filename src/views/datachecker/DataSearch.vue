<template>
  <div class="searchContainer">
    <header>
      <h1>BALAAN</h1>
      <div></div>
    </header>
    <main>
      <aside>Nav</aside>
      <article>
        <ul>
          <li v-for="item in items" v-bind:key="item._id">
            <div class="img"></div>
            <div class="info">
              <p>{{ item.brand_name }}</p>
              <p>{{ item.category }}</p>
              <p>{{ item.price.toLocaleString() }}</p>
            </div>
          </li>
        </ul>
      </article>
    </main>
  </div>
</template>

<style lang="scss">
.searchContainer {
  header {
    text-align: center;
    border-bottom: 1px solid grey;
  }
  main {
    display: flex;
    aside {
      flex: 1;
    }
    article {
      flex: 3;
      ul {
        display: flex;
        flex-wrap: wrap;
        list-style-type: none;
        li {
          margin: 0px 10px 30px 0px;
          width: 210px;
          height: 386px;
          .img {
            height: 60%;
          }
          .info {
            height: 40%;
          }
        }
      }
    }
  }
}
</style>

<script>
export default {
  data() {
    return {
      items: [
        {
          brand_name: "OFF WHITE",
          category: "반팔티",
          price: 250000
        },
        {
          brand_name: "OFF WHITE",
          category: "반팔티",
          price: 250000
        },
        {
          brand_name: "OFF WHITE",
          category: "반팔티",
          price: 250000
        },
        {
          brand_name: "OFF WHITE",
          category: "반팔티",
          price: 250000
        },
        {
          brand_name: "OFF WHITE",
          category: "반팔티",
          price: 250000
        },
        {
          brand_name: "OFF WHITE",
          category: "반팔티",
          price: 250000
        }
      ]
    };
  }
};
</script>
