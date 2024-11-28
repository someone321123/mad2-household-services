<!-- src/components/NavBarCustomer.vue -->
<template>
    <nav>
      <ul>
        <li><router-link to="/my-works">My Works</router-link></li>
        <li><router-link to="/my-offers">My Offers</router-link></li>
        <li><router-link to="/customer-profile">Profile</router-link></li>
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
  