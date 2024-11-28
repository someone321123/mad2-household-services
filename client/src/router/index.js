import { createRouter, createWebHistory } from "vue-router";

// Vue router docs: https://router.vuejs.org/guide/
export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "register",
      component: () => import("../views/register.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/login.vue"),
    },
    {
      path: "/administrator",
      name: "administrator",
      component: () => import("../views/administrator.vue"),
      
    },
    {
      path: "/admin_dashboard",
      name: "admin_dashboard",
      component: () => import("../views/admin_dashboard.vue"),
    },
    {
      path: "/my_works",
      name: "my_works",
      component: () => import("../views/my_works.vue"),
    },
    {
      path: "/new_work",
      name: "new_work",
      component: () => import("../views/new_work.vue"),
    },
    {
      path: "/customer_profile",
      name: "customer_profile",
      component: () => import("../views/customer_profile.vue"),
    },
    {
      path: "/discover",
      name: "discover",
      component: () => import("../views/discover.vue"),
    },
    {
      path: "/your_works",
      name: "your_works",
      component: () => import("../views/your_works.vue"),
    },
    {
      path: "/professional_profile",
      name: "professional_profile",
      component: () => import("../views/professional_profile.vue"),
    },
  ],
});

