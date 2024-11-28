<template>
  <div>
    <component :is="currentNavBar"></component>
    <router-view></router-view>
  </div>
</template>

<script>
import { computed } from "vue";
import { useAuthStore } from "./stores/AuthStore";
import NavBarShared from "./components/NavBarShared.vue";
import NavBarAdmin from "./components/NavBarAdmin.vue";
import NavBarCustomer from "./components/NavBarCustomer.vue";
import NavBarProfessional from "./components/NavBarProfessional.vue";

export default {
  components: {
    NavBarShared,
    NavBarAdmin,
    NavBarCustomer,
    NavBarProfessional,
  },
  setup() {
    const authStore = useAuthStore();

    const currentNavBar = computed(() => {
      if (localStorage.getItem("role")==null) {
        return "NavBarShared";
      }
      switch (localStorage.getItem("role")) {
        case "admin":
          return "NavBarAdmin";
        case "customer":
          return "NavBarCustomer";
        case "professional":
          return "NavBarProfessional";
        default:
          return "NavBarShared";
      }
    });

    return { currentNavBar };
  },
};
</script>
