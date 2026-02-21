<template>
  <div class="home-page">
    <div class="header-section">
      <h1>Discover Sports Events</h1>
      
      <div class="search-bar">
        <!-- Future Algolia Search Integration here -->
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search by event title, sport, or city..."
          class="search-input"
        />
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <p>Loading events...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchEvents" class="btn btn-primary">Try Again</button>
    </div>

    <div v-else-if="filteredEvents.length === 0" class="empty-state">
      <p>No events found matching your criteria.</p>
    </div>

    <div v-else class="events-grid">
      <EventCard 
        v-for="event in filteredEvents" 
        :key="event.id" 
        :event="event" 
      />
    </div>

    <!-- Future RecommendationRow Integration here -->
    
    <!-- Future ChatbotWidget Integration here -->

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import EventCard from '../components/EventCard.vue';
import { useAuthStore } from '../stores/auth';

const events = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const searchQuery = ref('');
const authStore = useAuthStore();

const fetchEvents = async () => {
  loading.value = true;
  error.value = null;
  try {
    const config = authStore.token ? {
        headers: { Authorization: `Bearer ${authStore.token}` }
    } : {};
    
    // Calls the recommended endpoint which returns events sorted by preference
    const response = await axios.get('http://localhost:8000/api/events', config);
    events.value = response.data;
  } catch (err: any) {
    console.error('Error fetching events:', err);
    error.value = 'Failed to load events. Please try again later.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchEvents();
});

const filteredEvents = computed(() => {
  if (!searchQuery.value) return events.value;
  
  const query = searchQuery.value.toLowerCase();
  return events.value.filter(event => 
    event.title.toLowerCase().includes(query) ||
    event.sport_category.toLowerCase().includes(query) ||
    (event.venue_city && event.venue_city.toLowerCase().includes(query))
  );
});
</script>

<style scoped>
.home-page {
  padding: 2rem 0;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.header-section h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.search-bar {
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  border: 2px solid #e0e0e0;
  border-radius: 50px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.search-input:focus {
  border-color: #00bcd4;
  box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.1);
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.error-state {
  color: #dc3545;
}

.error-state p {
  margin-bottom: 1rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #00bcd4;
  color: white;
}

.btn-primary:hover {
  background-color: #009eb3;
}
</style>
