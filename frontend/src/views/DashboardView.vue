<template>
  <div class="dashboard-view animate-fade-in" v-if="user">
    <div class="page-header">
      <h1 class="page-title">Hello, <span class="text-gradient">{{ user.name }}</span></h1>
      <p class="page-subtitle">Role: <span class="badge badge-primary">{{ user.role.toUpperCase() }}</span></p>
      <button @click="logout" class="btn btn-outline btn-sm mt-4">Logout</button>
    </div>

    <!-- ADMIN DASHBOARD -->
    <div v-if="user.role === 'admin'" class="admin-dashboard">
      <h2 class="text-2xl font-bold mb-4">Platform Overview</h2>
      <div v-if="adminStats" class="stats-grid">
        <div class="glass-card stat-card">
          <p class="stat-label">Total Users</p>
          <p class="stat-value text-gradient">{{ adminStats.total_users }}</p>
        </div>
        <div class="glass-card stat-card">
          <p class="stat-label">Total Events</p>
          <p class="stat-value text-gradient-alt">{{ adminStats.total_events }}</p>
        </div>
        <div class="glass-card stat-card">
          <p class="stat-label">Registrations</p>
          <p class="stat-value">{{ adminStats.total_registrations }}</p>
        </div>
        <div class="glass-card stat-card">
          <p class="stat-label">Revenue (₹)</p>
          <p class="stat-value text-success">₹{{ adminStats.total_revenue }}</p>
        </div>
      </div>
      <div v-else-if="loading" class="text-secondary mt-4">Loading stats...</div>
    </div>

    <!-- ORGANIZER DASHBOARD -->
    <div v-else-if="user.role === 'organizer'" class="organizer-dashboard">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Your Events</h2>
        <!-- Form could go here / modal to add event in real app -->
        <button class="btn btn-primary" @click="alert('Create event feature to be fully implemented')">+ Create Event</button>
      </div>
      
      <div v-if="loading" class="text-secondary">Loading your events...</div>
      <div v-else-if="orgEvents.length === 0" class="glass-card text-center py-8">
        <p class="text-secondary">You haven't created any events yet.</p>
      </div>
      
      <div v-else class="org-events-grid">
        <div v-for="evt in orgEvents" :key="evt.event_id" class="glass-card list-card flex justify-between items-center">
          <div>
            <h3 class="text-lg font-bold">{{ evt.title }}</h3>
            <p class="text-sm text-secondary">Registrations: {{ evt.registrations }} | Seats Left: {{ evt.seats_remaining }}</p>
          </div>
          <div class="text-right">
            <p class="text-success font-bold">₹{{ evt.revenue }}</p>
            <span class="badge" :class="evt.performance === 'HIGH' ? 'badge-success' : 'badge-outline'">{{ evt.performance }} Performance</span>
          </div>
        </div>
      </div>
    </div>

    <!-- USER DASHBOARD -->
    <div v-else class="user-dashboard">
      <h2 class="text-2xl font-bold mb-6">My Registrations</h2>
      
      <div v-if="loading" class="text-secondary">Loading registrations...</div>
      <div v-else-if="userRegistrations.length === 0" class="glass-card text-center py-8">
        <p class="text-secondary mb-4">You haven't registered for any events yet.</p>
        <router-link to="/events" class="btn btn-primary">Discover Events</router-link>
      </div>
      
      <div v-else class="user-events-grid">
        <div v-for="reg in userRegistrations" :key="reg.id" class="glass-card list-card">
          <div class="flex justify-between mb-4">
            <h3 class="text-lg font-bold">{{ reg.event.title }}</h3>
            <span class="badge" :class="reg.status === 'confirmed' ? 'badge-success' : 'badge-outline'">{{ reg.status.toUpperCase() }}</span>
          </div>
          <p class="text-sm text-secondary mb-1">Date: {{ new Date(reg.event.event_date).toLocaleDateString() }}</p>
          <p class="text-sm text-secondary mb-4">Location: {{ reg.event.venue_city }}</p>
          
          <div class="flex gap-2">
            <router-link :to="`/events/${reg.event.id}`" class="btn btn-outline btn-sm">View Event</router-link>
            <button v-if="reg.status === 'confirmed'" @click="cancelRegistration(reg.id)" class="btn btn-ghost btn-sm text-error hover-bg-error">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();
const user = computed(() => authStore.user);

const loading = ref(false);

// Admin state
const adminStats = ref<any>(null);

// Organizer state
const orgEvents = ref<any[]>([]);

// User state
const userRegistrations = ref<any[]>([]);

const loadDashboardData = async () => {
  if (!user.value) return;
  loading.value = true;
  try {
    if (user.value.role === 'admin') {
      const res = await api.get('/admin/stats');
      adminStats.value = res.data;
    } else if (user.value.role === 'organizer') {
      const res = await api.get('/organizer/dashboard');
      orgEvents.value = res.data;
    } else {
      const res = await api.get('/registrations');
      // Assume API returns an array or object containing registrations
      userRegistrations.value = res.data.registrations || res.data;
    }
  } catch (err) {
    console.error('Error loading dashboard data', err);
  } finally {
    loading.value = false;
  }
};

const cancelRegistration = async (id: number) => {
  if(!confirm('Are you sure you want to cancel this registration?')) return;
  try {
    await api.delete(`/registrations/${id}`);
    alert('Registration cancelled successfully.');
    loadDashboardData();
  } catch (err: any) {
    alert(err.response?.data?.message || 'Failed to cancel registration');
  }
}

const logout = () => {
  authStore.logout();
  router.push('/login');
};

onMounted(() => {
  if (!user.value) {
    router.push('/login');
  } else {
    loadDashboardData();
  }
});
</script>

<style scoped>
.mb-6 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mt-4 { margin-top: 1rem; }
.py-8 { padding-top: 2rem; padding-bottom: 2rem; }
.px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
.text-center { text-align: center; }
.text-right { text-align: right; }

.flex { display: flex; }
.justify-between { justify-content: space-between; }
.items-center { align-items: center; }
.gap-2 { gap: 0.5rem; }

.text-secondary { color: var(--text-secondary); }
.text-success { color: var(--success); font-weight: bold; }
.text-error { color: var(--error); }
.text-sm { font-size: 0.875rem; }
.text-lg { font-size: 1.125rem; }
.text-2xl { font-size: 1.5rem; }
.font-bold { font-weight: 700; }

.hover-bg-error:hover {
  background: rgba(255, 23, 68, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  text-align: center;
  padding: 2rem 1rem;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1;
}

.list-card {
  margin-bottom: 1rem;
  padding: 1.5rem;
}

.org-events-grid, .user-events-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}
</style>
