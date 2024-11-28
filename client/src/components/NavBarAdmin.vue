<!-- src/components/NavBarAdmin.vue -->
<template>
    <nav>
      <ul>
        <li><router-link to="/dashboard">Dashboard</router-link></li>
        <li><router-link to="/extract-csv">Extract CSV</router-link></li>
        <li><button @click="logout">Logout</button></li>
      </ul>
    </nav>
  </template>
  
  <script>
  import { useAuthStore } from '../stores/AuthStore';
  
  export default {
    setup() {
      const authStore = useAuthStore();
      const logout = () => authStore.logout();
      return { logout };
    },
  };
  </script>
  