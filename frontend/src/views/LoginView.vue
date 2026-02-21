<template>
  <div class="auth-container animate-fade-in">
    <div class="glass-card auth-card">
      <h2 class="text-2xl font-bold mb-6 text-center">Welcome Back</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label class="input-label">Email</label>
          <input 
            v-model="email" 
            type="email" 
            class="input-field" 
            placeholder="Enter your email" 
            required
          />
        </div>
        
        <div class="input-group">
          <label class="input-label">Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="input-field" 
            placeholder="Enter your password" 
            required
          />
        </div>
        
        <div v-if="error" class="error-msg mb-4">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary w-full" :disabled="authStore.isLoading">
          {{ authStore.isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <p class="text-center mt-6 text-secondary">
        Don't have an account? <router-link to="/register" class="text-primary hover-underline">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
  error.value = '';
  try {
    await authStore.login(email.value, password.value);
    
    // Spec 4.2 Routing Rule Implementation
    if (authStore.isAdmin) {
      router.push('/admin');
    } else if (authStore.isOrganizer) {
      router.push('/organizer');
    } else {
      router.push('/home');
    }
    
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Failed to login. Please try again.';
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.input-group { margin-bottom: 1.5rem; }
.input-label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
.input-field {
  width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;
}

.w-full { width: 100%; }
.mb-6 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mt-6 { margin-top: 1.5rem; }
.text-center { text-align: center; }
.text-2xl { font-size: 1.5rem; }
.font-bold { font-weight: 700; }
.text-secondary { color: #666; }
.text-primary { color: #00bcd4; text-decoration: none; }
.hover-underline:hover { text-decoration: underline; }
.btn { padding: 0.75rem; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
.btn-primary { background-color: #00bcd4; color: white; }
.btn-primary:disabled { opacity: 0.7; cursor: not-allowed; }

.error-msg {
  color: #dc3545;
  font-size: 0.9rem;
  background: rgba(220, 53, 69, 0.1);
  padding: 0.75rem;
  border-radius: 4px;
}
</style>
