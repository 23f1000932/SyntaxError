<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="nav-logo">SyntaxError</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/events" class="nav-link">Events</router-link>
          
          <template v-if="authStore.token">
            <router-link to="/profile" class="nav-link">Dashboard</router-link>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link">Login</router-link>
            <router-link to="/register" class="btn btn-primary btn-sm ml-4">Register</router-link>
          </template>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>

    <ChatbotWidget />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';
import ChatbotWidget from './components/ChatbotWidget.vue';

const authStore = useAuthStore();

onMounted(() => {
  authStore.initializeAuth();
});
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 2rem;
}

.btn-sm {
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
}

.ml-4 {
  margin-left: 1rem;
}
</style>
