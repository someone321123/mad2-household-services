<!-- src/components/NavBarProfessional.vue -->
<template>
    <nav>
      <ul>
        <li><router-link to="/discover">Discover</router-link></li>
        <li><router-link to="/your-works">Your Works</router-link></li>
        <li><router-link to="/professional-profile">Profile</router-link></li>
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
  