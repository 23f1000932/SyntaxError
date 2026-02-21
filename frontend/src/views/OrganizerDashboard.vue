<template>
  <div class="organizer-dashboard">
    <div class="header-section">
      <h1>Organizer Dashboard</h1>
      <button @click="$router.push('/organizer/create')" class="btn btn-primary">+ Create New Event</button>
    </div>

    <div v-if="loading" class="loading-state">Loading dashboard...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    
    <div v-else class="dashboard-content">
        <!-- Feature 11: Ticket Sales Summary Table -->
        <section class="dashboard-section">
            <h2>Your Events Overview</h2>
            <div class="table-container">
                <table class="data-table">
                <thead>
                    <tr>
                    <th>Event Title</th>
                    <th>Date</th>
                    <th>City</th>
                    <th>Registrations</th>
                    <th>Remaining</th>
                    <th>Revenue (₹)</th>
                    <th>Performance</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="event in events" :key="event.event_id">
                    <td>{{ event.title }}</td>
                    <td>{{ new Date(event.event_date).toLocaleDateString() }}</td>
                    <td>{{ event.venue_city }}</td>
                    <td>{{ event.registrations }}</td>
                    <td>{{ event.seats_remaining }}</td>
                    <td>₹{{ event.revenue }}</td>
                    <td><span class="badge" :class="event.performance_label.toLowerCase()">{{ event.performance_label }}</span></td>
                    </tr>
                    <tr v-if="events.length === 0">
                    <td colspan="7" class="text-center">No active events found. Create one!</td>
                    </tr>
                </tbody>
                </table>
            </div>
        </section>

        <!-- Feature 10 & 12: Charts -->
        <div class="charts-grid" v-if="events.length > 0">
            <!-- Registration Trend Chart -->
            <section class="dashboard-section chart-card">
                <h2>Registration Trend</h2>
                <div class="event-selector">
                    <label>Select Event: </label>
                    <select v-model="selectedEventId" @change="fetchTrendData">
                        <option v-for="event in events" :key="event.event_id" :value="event.event_id">
                            {{ event.title }}
                        </option>
                    </select>
                </div>
                <div v-if="loadingTrend" class="text-center mt-2">Loading chart...</div>
                <RegistrationTrend v-else :data="trendData" />
            </section>

            <!-- Sport Category Insights Chart -->
            <section class="dashboard-section chart-card">
                <h2>Registrations by Sport</h2>
                <CategoryBarChart :data="categoryData" />
            </section>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import RegistrationTrend from '../components/charts/RegistrationTrend.vue';
import CategoryBarChart from '../components/charts/CategoryBarChart.vue';

const authStore = useAuthStore();
const loading = ref(true);
const loadingTrend = ref(false);
const error = ref('');

const events = ref<any[]>([]);
const categoryData = ref<any[]>([]);
const trendData = ref<any[]>([]);
const selectedEventId = ref<number | null>(null);

const fetchDashboardData = async () => {
    loading.value = true;
    error.value = '';
    try {
        const config = { headers: { Authorization: `Bearer ${authStore.token}` } };
        
        // Parallel fetch for Dashboard KPIs and Category Insights
        const [dashRes, catRes] = await Promise.all([
            axios.get('http://localhost:8000/api/organizer/dashboard', config),
            axios.get('http://localhost:8000/api/organizer/category-insight', config)
        ]);

        events.value = dashRes.data;
        categoryData.value = catRes.data;

        if (events.value.length > 0) {
            selectedEventId.value = events.value[0].event_id;
            await fetchTrendData();
        }

    } catch (err: any) {
        error.value = 'Failed to load dashboard data. ' + (err.response?.data?.message || '');
    } finally {
        loading.value = false;
    }
};

const fetchTrendData = async () => {
    if (!selectedEventId.value) return;
    loadingTrend.value = true;
    try {
        const config = { headers: { Authorization: `Bearer ${authStore.token}` } };
        const res = await axios.get(`http://localhost:8000/api/organizer/trend/${selectedEventId.value}`, config);
        trendData.value = res.data;
    } catch (err) {
        console.error("Failed to load trend", err);
    } finally {
        loadingTrend.value = false;
    }
};

onMounted(() => {
    fetchDashboardData();
});
</script>

<style scoped>
.organizer-dashboard {
  padding: 2rem 0;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

.btn-primary {
  background-color: #00bcd4;
  color: white;
}

.dashboard-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.dashboard-section h2 {
    margin-bottom: 1rem;
    font-size: 1.25rem;
    color: #333;
    border-bottom: 2px solid #eee;
    padding-bottom: 0.5rem;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #555;
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}
.badge.high { background: #d4edda; color: #155724; }
.badge.medium { background: #fff3cd; color: #856404; }
.badge.low { background: #f8d7da; color: #721c24; }

.charts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.chart-card {
    margin-bottom: 0;
}

.event-selector {
    margin-bottom: 1rem;
}

.event-selector select {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ddd;
}

.mt-2 { margin-top: 0.5rem; }
.text-center { text-align: center; }
.error-message { color: #dc3545; background: #f8d7da; padding: 1rem; border-radius: 4px; }
.loading-state { text-align: center; font-size: 1.2rem; color: #666; padding: 2rem; }
</style>
