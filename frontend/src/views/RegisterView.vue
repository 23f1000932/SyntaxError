<template>
  <div class="register-page">
    <div class="register-container">
      <h1>SyntaxError Sports</h1>
      <h2>Register</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input id="name" v-model="form.name" type="text" placeholder="Enter your full name" required />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="form.email" type="email" placeholder="Enter your email" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="form.password" type="password" placeholder="Enter your password" required />
        </div>
        <div class="form-group">
          <label for="role">Account Type</label>
          <select id="role" v-model="form.role">
            <option value="user">Participant</option>
            <option value="organizer">Event Organizer</option>
          </select>
        </div>

        <!-- Optional fields for Recommendations -->
        <div v-if="form.role === 'user'" class="optional-fields">
            <h4>Tell us your preferences (Optional)</h4>
            <div class="form-group">
              <label for="city">City</label>
              <input id="city" v-model="form.city" type="text" placeholder="e.g. Mumbai" />
            </div>
            <div class="form-group">
              <label for="budget">Budget Preference</label>
              <select id="budget" v-model="form.budget_preference">
                <option value="cheap">Cheap (< ₹500)</option>
                <option value="mid">Mid (₹500 - ₹2000)</option>
                <option value="premium">Premium (> ₹2000)</option>
              </select>
            </div>
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>
        <button type="submit" :disabled="loading" class="submit-button">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>
      <div class="login-link">
        <p>Already have an account? <router-link to="/login">Login here</router-link></p>
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
    error.value = err.response?.data?.message || authStore.error || 'Registration failed';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.register-container {
  background: white;
  padding: 3rem 2rem;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
}

.register-container h1 {
  text-align: center;
  color: #667eea;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.register-container h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 1.2rem;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.optional-fields {
    background: #f9f9f9;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    border: 1px dashed #ccc;
}

.optional-fields h4 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #666;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background-color: #fadbd8;
  border-radius: 4px;
}

.submit-button {
  padding: 0.75rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.submit-button:hover:not(:disabled) {
  background-color: #764ba2;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
