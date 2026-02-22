<template>
  <div id="app">
    <div class="luxury-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
      <div class="aura-blob aura-3"></div>
    </div>
    <nav class="navbar-premium glass-container" :class="{ 'scrolled': isScrolled }">
      <div class="container navbar-inner">
        <router-link to="/" class="navbar-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="color: var(--brand-primary)"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>
          <span>SYNTAX<span class="text-gradient">ERROR</span></span>
        </router-link>
        
        <div class="navbar-links">
          <!-- Unauthenticated Links -->
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/" class="nav-link-corp">Home</router-link>
            <router-link to="/login" class="nav-link-corp">Login</router-link>
            <router-link to="/register" class="btn-corp btn-corp-primary">
              Sign Up
            </router-link>
          </template>

          <!-- Authenticated Links -->
          <template v-else>
            <router-link 
              v-if="authStore.isUser" 
              to="/home" 
              class="nav-link-corp"
            >
              Browse Events
            </router-link>

            <router-link 
              v-if="authStore.isOrganizer" 
              to="/organizer" 
              class="nav-link-corp"
            >
              My Dashboard
            </router-link>

            <router-link 
              v-if="authStore.isAdmin" 
              to="/admin" 
              class="nav-link-corp"
            >
              Admin
            </router-link>

            <button @click="handleLogout" class="btn-corp btn-corp-outline">
              Logout
            </button>
          </template>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>

    <ChatbotWidget v-if="authStore.isAuthenticated" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from './stores/auth';
import ChatbotWidget from './components/ChatbotWidget.vue';

const router = useRouter();
const authStore = useAuthStore();
const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

onMounted(() => {
  authStore.initializeAuth();
  window.addEventListener('scroll', handleScroll);
});

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};
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
}

.navbar-premium {
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

.navbar-premium.scrolled {
  background: rgba(0, 0, 0, 0.85);
  box-shadow: 0 4px 30px rgba(0,0,0,0.5);
}

@media (max-width: 768px) {
  .navbar-links {
    display: none;
  }
}
</style>
