<!-- src/components/NavBarAdmin.vue -->
<template>
    <nav>
      <ul>
        <li class="navbar-item"><router-link to="/dashboard">Dashboard</router-link></li>
        <li class="navbar-item"><router-link to="/administrator">Administrator</router-link></li>
        <li class="navbar-item"><router-link ><button @click="export">Export CSV</button></router-link></li>
        <li class="navbar-item"><button @click="logout">Logout</button></li>
      </ul>
    </nav>
  </template>
  
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
 
 
 </style>
    