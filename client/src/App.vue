<script>
import Navbar from './components/Navbar.vue'

export default {
  name: "App",
  data() {
    return {role: this.$store.state.auth.role}
  },
  components: {
    Navbar
  }
}
</script>

<template>
  <div>
    <Navbar type="admin" v-if="role==='admin'" />

    <div class="container p-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>
</style>