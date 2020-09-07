import Vue from "vue";
import Router from "vue-router";

// Containers
const DefaultContainer = () => import("@/containers/DefaultContainer");

const CoreUIIcons = () => import("@/views/CoreUIIcons");

// Views - datachecker
const Dashboard = () => import("@/views/datachecker/Dashboard");
const DataChecker = () => import("@/views/datachecker/DataChecker");
const DataTable = () => import("@/views/datachecker/DataTable");
const DataSearch = () => import("@/views/datachecker/DataSearch");

// const Balaan = () => import('@/views/datachecker/PageBalaan')

// Views - Components
const Cards = () => import("@/views/base/Cards");
const Switches = () => import("@/views/base/Switches");
const Tabs = () => import("@/views/base/Tabs");
const Breadcrumbs = () => import("@/views/base/Breadcrumbs");
const Carousels = () => import("@/views/base/Carousels");
const Collapses = () => import("@/views/base/Collapses");
const Jumbotrons = () => import("@/views/base/Jumbotrons");
const ListGroups = () => import("@/views/base/ListGroups");
const Navs = () => import("@/views/base/Navs");
const Navbars = () => import("@/views/base/Navbars");
const Paginations = () => import("@/views/base/Paginations");
const Popovers = () => import("@/views/base/Popovers");
const ProgressBars = () => import("@/views/base/ProgressBars");
const Tooltips = () => import("@/views/base/Tooltips");

// Views - Forms
const BasicForms = () => import("@/views/BasicForms");

// Views - Pages
const Page404 = () => import("@/views/pages/Page404");
const Page500 = () => import("@/views/pages/Page500");
const Login = () => import("@/views/pages/Login");
const Register = () => import("@/views/pages/Register");

// Users
const Users = () => import("@/views/users/Users");
const User = () => import("@/views/users/User");

Vue.use(Router);

export default new Router({
  mode: "hash", // https://router.vuejs.org/api/#mode
  linkActiveClass: "open active",
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: "/",
      redirect: "/datachecker/dashboard",
      name: "Home",
      component: DefaultContainer,
      children: [
        {
          path: "datachecker",
          redirect: "/datachecker/dashboard",
          name: "datachecker",
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "dashboard",
              name: "Dashboard",
              component: Dashboard,
            },
            {
              path: "data-checker",
              name: "Data Checker",
              component: DataChecker,
            },
            {
              path: "data-table",
              name: "Data Table",
              component: DataTable,
            },
            {
              path: "data-search",
              name: "Data Search",
              component: DataSearch,
            },
          ],
        },

        {
          path: "users",
          meta: { label: "Users" },
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "",
              component: Users,
            },
            {
              path: ":id",
              meta: { label: "User Details" },
              name: "User",
              component: User,
            },
          ],
        },
        {
          path: "base",
          redirect: "/base/cards",
          name: "Base",
          component: {
            render(c) {
              return c("router-view");
            },
          },
          children: [
            {
              path: "breadcrumbs",
              name: "Breadcrumbs",
              component: Breadcrumbs,
            },
            {
              path: "cards",
              name: "Cards",
              component: Cards,
            },
            {
              path: "carousels",
              name: "Carousels",
              component: Carousels,
            },
            {
              path: "collapses",
              name: "Collapses",
              component: Collapses,
            },
            {
              path: "jumbotrons",
              name: "Jumbotrons",
              component: Jumbotrons,
            },
            {
              path: "list-groups",
              name: "List Groups",
              component: ListGroups,
            },
            {
              path: "navs",
              name: "Navs",
              component: Navs,
            },
            {
              path: "navbars",
              name: "Navbars",
              component: Navbars,
            },
            {
              path: "paginations",
              name: "Paginations",
              component: Paginations,
            },
            {
              path: "popovers",
              name: "Popovers",
              component: Popovers,
            },
            {
              path: "progress-bars",
              name: "Progress Bars",
              component: ProgressBars,
            },
            {
              path: "switches",
              name: "Switches",
              component: Switches,
            },
            {
              path: "tabs",
              name: "Tabs",
              component: Tabs,
            },
            {
              path: "tooltips",
              name: "Tooltips",
              component: Tooltips,
            },
          ],
        },
        {
          path: "basic-forms",
          name: "Basic Forms",
          component: BasicForms,
        },
        {
          path: "coreui-icons",
          name: "CoreUI Icons",
          component: CoreUIIcons,
        },
      ],
    },
    {
      path: "/pages",
      redirect: "/pages/404",
      name: "Pages",
      component: {
        render(c) {
          return c("router-view");
        },
      },
      children: [
        {
          path: "404",
          name: "Page404",
          component: Page404,
        },
        {
          path: "500",
          name: "Page500",
          component: Page500,
        },
        {
          path: "login",
          name: "Login",
          component: Login,
        },
        {
          path: "register",
          name: "Register",
          component: Register,
        },
      ],
    },
  ],
});
