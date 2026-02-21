<template>
  <div class="admin-dashboard">
    <div class="header-section">
      <h1>Platform Administrator Overview</h1>
      <button @click="fetchData" class="btn btn-outline" :disabled="loading">
        ↻ Refresh Data
      </button>
    </div>

    <div v-if="loading" class="loading-state">Loading system analytics...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    
    <div v-else class="dashboard-content">
      <!-- Feature 13: Top-level Platform Stats -->
      <section class="kpi-grid">
        <div class="kpi-card">
          <h4>Total Users</h4>
          <span class="kpi-val">{{ overview.total_users }}</span>
        </div>
        <div class="kpi-card">
          <h4>Active Events</h4>
          <span class="kpi-val">{{ overview.total_events }}</span>
        </div>
        <div class="kpi-card">
          <h4>Total Registrations</h4>
          <span class="kpi-val">{{ overview.total_registrations }}</span>
        </div>
        <div class="kpi-card">
          <h4>Total Revenue</h4>
          <span class="kpi-val">₹{{ overview.total_revenue?.toLocaleString() }}</span>
        </div>
      </section>

      <!-- Charts Row 1 -->
      <div class="charts-row">
        <!-- Feature 17: Monthly Trend -->
        <div class="chart-wrapper">
          <MonthlyTrendChart :data="monthlyTrend" />
        </div>
        
        <!-- Feature 15: City Distribution -->
        <div class="chart-wrapper">
          <CityDistributionChart :data="cityData" />
        </div>
      </div>

      <!-- Feature 16: Fill Rates Table -->
      <FillRateTable :data="fillRates" />

      <!-- Feature 18: Organizer Leaderboard -->
      <section class="table-section mt-4">
        <h3>Top Organizers</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Organizer Name</th>
              <th>Total Events</th>
              <th>Registrations Generated</th>
              <th>Total Revenue</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(org, i) in topOrganizers" :key="org.organizer_id">
              <td>#{{ i + 1 }}</td>
              <td>{{ org.organizer_name }}</td>
              <td>{{ org.total_events }}</td>
              <td>{{ org.total_registrations }}</td>
              <td>₹{{ org.total_revenue.toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import MonthlyTrendChart from '../components/charts/MonthlyTrendChart.vue';
import CityDistributionChart from '../components/charts/CityDistributionChart.vue';
import FillRateTable from '../components/charts/FillRateTable.vue';

const authStore = useAuthStore();
const loading = ref(true);
const error = ref('');

// Data Refs
const overview = ref<any>({});
const monthlyTrend = ref<any[]>([]);
const cityData = ref<any[]>([]);
const fillRates = ref<any[]>([]);
const topOrganizers = ref<any[]>([]);

const fetchData = async () => {
  loading.value = true;
  error.value = '';
  try {
    const config = { headers: { Authorization: `Bearer ${authStore.token}` } };
    
    const [statsRes, trendRes, cityRes, fillRes, orgRes] = await Promise.all([
      axios.get('http://localhost:8000/api/admin/analytics', config),
      axios.get('http://localhost:8000/api/admin/monthly-trend', config),
      axios.get('http://localhost:8000/api/admin/city-distribution', config),
      axios.get('http://localhost:8000/api/admin/fill-rate', config),
      axios.get('http://localhost:8000/api/admin/organizer-performance', config)
    ]);

    overview.value = statsRes.data;
    monthlyTrend.value = trendRes.data;
    cityData.value = cityRes.data;
    fillRates.value = fillRes.data;
    topOrganizers.value = orgRes.data;

  } catch (err: any) {
    error.value = 'Failed to load admin analytics. ' + (err.response?.data?.message || '');
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchData());
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem 0;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-outline {
  padding: 0.5rem 1rem;
  background: transparent;
  border: 1px solid #00bcd4;
  color: #00bcd4;
  border-radius: 4px;
  cursor: pointer;
}
.btn-outline:hover { background: rgba(0, 188, 212, 0.1); }
.btn-outline:disabled { opacity: 0.5; }

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.kpi-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: center;
}

.kpi-card h4 {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
}

.kpi-val {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.charts-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.chart-wrapper {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.table-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.table-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #555;
}

.mt-4 { margin-top: 1.5rem; }
.error-message { color: #dc3545; background: #f8d7da; padding: 1rem; border-radius: 4px; }
.loading-state { text-align: center; font-size: 1.2rem; color: #666; padding: 2rem; }
</style>
