<template>
  <div class="register-page">
    <div class="luxury-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
      <div class="aura-blob aura-3"></div>
    </div>

    <div class="container auth-wrapper">
      <div class="card-premium auth-card animate-corp">
        <div class="auth-header mb-10 text-center">
          <span class="badge-corp">Profile Initialization</span>
          <h1 class="hero-title-small mt-4">Join SyntaxError</h1>
          <p class="text-dim mt-2">Create your elite sports operative account.</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="auth-form-grid">
          <div class="input-stack">
            <label class="label-muted">Full Legal Name</label>
            <input v-model="form.name" type="text" class="input-corp" placeholder="Operative Name" required />
          </div>
          
          <div class="input-stack">
            <label class="label-muted">Interface Address (Email)</label>
            <input v-model="form.email" type="email" class="input-corp" placeholder="name@syntax.error" required />
          </div>
          
          <div class="input-stack">
            <label class="label-muted">Access Key (Password)</label>
            <input v-model="form.password" type="password" class="input-corp" placeholder="••••••••" required />
          </div>
          
          <div class="input-stack">
            <label class="label-muted">System Role</label>
            <select v-model="form.role" class="input-corp">
              <option value="user">Participant / Operative</option>
              <option value="organizer">Event Vendor / Architect</option>
            </select>
          </div>

          <!-- Profile Preferences -->
          <div v-if="form.role === 'user'" class="preferences-panel mt-6 animate-corp">
              <div class="panel-divider mb-8"></div>
              <p class="label-muted mb-6">Bio-Regional Preferences</p>
              
              <div class="input-stack">
                <label class="label-muted">Primary City</label>
                <input v-model="form.city" type="text" class="input-corp" placeholder="e.g. Mumbai" />
              </div>
              <div class="input-stack mt-6">
                <label class="label-muted">Tier Preference</label>
                <select v-model="form.budget_preference" class="input-corp">
                  <option value="cheap">Standard (< ₹500)</option>
                  <option value="mid">Mid-Tier (₹500 - ₹2000)</option>
                  <option value="premium">Elite Suite (> ₹2000)</option>
                </select>
              </div>
          </div>

          <div v-if="error" class="error-panel-inline mt-6 animate-corp">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            <span>{{ error }}</span>
          </div>
          
          <button type="submit" :disabled="loading" class="btn-corp btn-corp-primary w-full mt-8">
            {{ loading ? 'Initializing...' : 'Finalize Registration' }}
          </button>
        </form>
        
        <div class="auth-footer mt-12 text-center pt-8 border-top">
          <p class="text-dim">Existing profile? <router-link to="/login" class="link-corp">Return to Terminal</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const loading = ref(false);
const error = ref('');

const form = ref({
  name: '',
  email: '',
  password: '',
  role: 'user',
  city: '',
  budget_preference: 'mid',
  preferred_sports: [] as string[]
});

const handleRegister = async () => {
  loading.value = true;
  error.value = '';

  try {
    await authStore.register(form.value);
    
    if (authStore.isAdmin) {
      router.push('/admin');
    } else if (authStore.isOrganizer) {
      router.push('/organizer');
    } else {
      router.push('/home');
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || authStore.error || 'Identity initialization failed.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  padding: 80px 0 40px;
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.auth-card {
  width: 100%;
  max-width: 480px;
  padding: 2.5rem;
}

.hero-title-small {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.15;
}

.error-panel-inline {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #ff5555;
  font-size: 0.85rem;
  padding: 1rem;
  background: rgba(255, 85, 85, 0.05);
  border: 1px solid rgba(255, 85, 85, 0.1);
  border-radius: var(--radius-sm);
}

.panel-divider {
  height: 1px;
  background: var(--border-subtle);
}

.link-corp {
  color: var(--brand-primary);
  text-decoration: none;
  font-weight: 700;
  transition: var(--transition-fast);
}

.link-corp:hover {
  filter: brightness(1.2);
  text-decoration: underline;
}

.border-top {
  border-top: 1px solid var(--border-subtle);
}

@media (max-width: 640px) {
  .auth-card {
    padding: 2.5rem;
  }
}
</style>
