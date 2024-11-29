<!-- src/components/NavBarProfessional.vue -->
<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <li class="navbar-item"><router-link to="/discover">WELCOME PROFESSIONAL</router-link></li>
      <li class="navbar-item"><router-link to="/discover">Discover</router-link></li>
      <li class="navbar-item"><router-link to="/your_works">Your Works</router-link></li>
      <li class="navbar-item"><router-link to="/professional_profile">Profile</router-link></li>
      <li class="navbar-item"><button @click="logout">Logout</button></li>
    </ul>
  </nav>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const logout = () => {
      localStorage.clear();
      router.push('/login').then(() => {
        router.go(0);
      });
    };

    return {
      logout
    };
  },
};
</script>
<style scoped>
.navbar {
background-color: #008000; /* Green background */

top: 0;
width: 100%;
height: 50px; /* Fixed height */
}

.navbar-list {
list-style-type: none;
margin: 0;
padding: 0;
display: flex; /* Use flexbox for horizontal layout */
justify-content: center; /* Center items horizontally */
align-items: center; /* Center items vertically */
height: 100%; /* Full height of navbar */
}

.navbar-item {
margin: 0 10px; /* Space between items */
}

.navbar-item a, .navbar-item button {
color: white;
text-decoration: none;
background: none;
border: none;
cursor: pointer;
padding: 10px 15px;
transition: background-color 0.3s ease;
}

.navbar-item a:hover, .navbar-item button:hover {
background-color: rgba(255, 255, 255, 0.2); /* Subtle hover effect */
color: white;
}

.navbar-item button {
font-size: inherit;
font-family: inherit;
}
</style>

  