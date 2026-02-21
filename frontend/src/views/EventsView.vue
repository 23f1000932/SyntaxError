<template>
  <div class="events-view animate-fade-in">
    <div class="page-header">
      <h1 class="page-title">Discover <span class="text-gradient-alt">Events</span></h1>
      <p class="page-subtitle">Find your next challenge. Filter by category or search for specific events.</p>
    </div>

    <div class="search-filters-container glass-card mb-8">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="input-field" 
          placeholder="Search for events, cities, or keywords..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" class="btn btn-primary ml-2">Search</button>
      </div>

      <div class="filters">
        <button 
          v-for="cat in categories" 
          :key="cat"
          @click="selectCategory(cat)"
          class="badge"
          :class="selectedCategory === cat ? 'badge-primary' : 'badge-outline'"
        >
          {{ cat || 'All Categories' }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-state text-center py-12">
      <p>Loading events...</p>
    </div>
    
    <div v-else-if="events.length === 0" class="empty-state text-center py-12 glass-card">
      <h3 class="text-xl mb-2">No events found</h3>
      <p class="text-secondary">Try adjusting your filters or search query.</p>
      <button @click="clearFilters" class="btn btn-outline mt-4">Clear Filters</button>
    </div>
    
    <div v-else class="event-grid">
      <EventCard 
        v-for="(event, index) in events" 
        :key="event.id" 
        :event="event" 
        class="animate-fade-in"
        :style="`animation-delay: ${(index % 10) * 50}ms`"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import api from '../services/api';
import EventCard from '../components/EventCard.vue';

const events = ref<any[]>([]);
const loading = ref(true);
const searchQuery = ref('');
const selectedCategory = ref('');

const categories = ['', 'Football', 'Cricket', 'Basketball', 'Tennis', 'Badminton', 'Running', 'eSports'];

const fetchEvents = async () => {
  loading.value = true;
  try {
    // Determine the endpoint to call based on filters
    let url = '/events';
    const params = new URLSearchParams();
    
    if (searchQuery.value) {
      params.append('search', searchQuery.value);
    }
    
    if (selectedCategory.value) {
      params.append('category', selectedCategory.value);
    }
    
    const queryString = params.toString();
    if (queryString) {
      url += `?${queryString}`;
    }

    const response = await api.get(url);
    // Note: Depends on if pagination is implemented in the backend response format or if it returns an array
    events.value = response.data.events || response.data || [];
  } catch (err) {
    console.error('Failed to load events:', err);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  fetchEvents();
};

const selectCategory = (cat: string) => {
  selectedCategory.value = cat;
  fetchEvents();
};

const clearFilters = () => {
  searchQuery.value = '';
  selectedCategory.value = '';
  fetchEvents();
};

onMounted(() => {
  fetchEvents();
});
</script>

<style scoped>
.mb-8 { margin-bottom: 2rem; }
.ml-2 { margin-left: 0.5rem; }
.mt-4 { margin-top: 1rem; }
.mb-2 { margin-bottom: 0.5rem; }
.py-12 { padding-top: 3rem; padding-bottom: 3rem; }
.text-center { text-align: center; }
.text-xl { font-size: 1.25rem; font-weight: 600; }
.text-secondary { color: var(--text-secondary); }

.search-filters-container {
  padding: 1.5rem;
}

.search-box {
  display: flex;
  margin-bottom: 1.5rem;
}

.search-box .input-field {
  margin-bottom: 0;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.filters .badge {
  cursor: pointer;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  transition: all var(--transition-fast);
}

.filters .badge:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.1);
}

.filters .badge-primary:hover {
  background: rgba(0, 229, 255, 0.2);
}

.event-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}
</style>
