<!-- src/components/NavBarShared.vue -->
<template>
  <nav>
    <ul>
      <li><router-link to="/">Login</router-link></li>
      <li><router-link to="/register">Register</router-link></li>
    </ul>
  </nav>
</template>
<script>
export default {
  name: "NavbarShared",
  
}
</script>