<script>
import NavBarShared from './components/NavBarShared.vue';

export default {
  name: "App"
}
</script>

<template>
  <div>
    <div class="container p-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>
</style>