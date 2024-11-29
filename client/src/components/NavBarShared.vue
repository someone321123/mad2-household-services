<!-- src/components/NavBarShared.vue -->
<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <li class="navbar-item"><router-link to="/login">HOUSEHOLD SERVICES APP</router-link></li>
      <li class="navbar-item"><router-link to="/login">Login</router-link></li>
      <li class="navbar-item"><router-link to="/">Register</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: #008000; /* Green background */
  
  
  top: 0;
  width: 100%;
  height: 50px; /* Decreased height */
}

.navbar-list {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* Ensure items are centered vertically */
}

.navbar-item {
  padding: 0 20px; /* Adjusted padding to fit decreased height */
}

.navbar-item a {
  color: white;
  text-align: center;
  padding: 14px 20px;
  text-decoration: none;
  display: block;
}

.navbar-item a:hover {
  background-color: white; /* White buttons on hover */
  color: black;
}
</style>

