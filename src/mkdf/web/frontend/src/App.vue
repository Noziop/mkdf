<template>
  <div id="app">
    <nav class="navbar">
      <h1>{{ appName }}</h1>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      appName: 'Fullstack App'
    }
  }
}
</script>

<style>
.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem;
}
</style>
