<!-- src/components/NavBarShared.vue -->
<template> <nav class="navbar"> <ul class="navbar-list"> <li class="navbar-item"><router-link to="/login">Login</router-link></li> <li class="navbar-item"><router-link to="/">Register</router-link></li> </ul> </nav> </template>
<script>
import { useAuthStore } from '../stores/AuthStore';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const logout = () => {
      localStorage.clear();

      authStore.logout();

      router.push('/login');
    };

    return {
      logout
    };
  },
};
</script> 

<style scoped>

.navbar-item a {
  background-color: #ddd;
  color: black;
  text-decoration: none;
  font-weight:bolder;}


.navbar-item a:hover {
  background-color: #ddd;
  color: rgb(59, 36, 36);
  text-decoration: none;
  font-weight: bold;
  font-size: 20px;
}
</style>
