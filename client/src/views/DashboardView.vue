<template>
    <div>
      <h1>Welcome</h1>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from '../stores/AuthStore';
  
  export default {
    setup() {
      const authStore = useAuthStore();
  
      const logout = () => {
        authStore.logout();
        this.$router.push('/');
      };
  
      return { logout, authStore };
    },
  };
  </script>
  