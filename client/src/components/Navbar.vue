<template>
  <nav>
    <ul v-if="type === 'admin'">
      <li><router-link to="/admin/dashboard">Dashboard</router-link></li>
      <li><router-link to="/admin/statistics">Statistics</router-link></li>
      <li><router-link to="/admin/export-csv">Export CSV</router-link></li>
    </ul>

    <ul v-if="type === 'customer'">
      <li><router-link to="/customer/new-work">New Work</router-link></li>
      <li><router-link to="/customer/my-work">My Work</router-link></li>
      <li><router-link to="/customer/profile">Profile</router-link></li>
    </ul>

    <ul v-if="type === 'professional'">
      <li><router-link to="/professional/discover">Discover</router-link></li>
      <li><router-link to="/professional/your-work">Your Work</router-link></li>
      <li><router-link to="/professional/profile">Profile</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
  props: {
    type: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped></style>
