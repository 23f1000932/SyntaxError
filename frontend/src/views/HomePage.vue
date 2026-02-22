<template>
  <div class="home-page animate-corp">
    <header class="hero-v3">
      <div class="container text-center animate-corp">
        <span class="badge-corp">Discover &amp; Register</span>
        <h1 class="hero-main-title delay-100">
          Find Your Next <span class="text-gradient">Sports Event.</span>
        </h1>
        <p class="hero-description delay-200">
          Browse upcoming tournaments, register instantly, and track your participation — all in one place.
        </p>

        <div v-if="authStore.isAuthenticated && authStore.isUser" class="hero-personalized-track mt-8 animate-corp delay-300">
           <RecommendationRow title="Recommended for You" :limit="4" />
        </div>
      </div>
    </header>

    <section class="section-spacer">
      <div class="container">
        <div class="section-header-flex mb-10 animate-corp">
          <div class="header-text">
            <h2 class="section-title-large">Browse Events</h2>
            <p class="section-subtitle">Find and join the latest sports events near you.</p>
          </div>
          <div class="search-luxury-wrapper input-stack">
            <label class="label-muted mb-2">Architectural Search</label>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Search by title, category, or bio-region..."
              class="input-corp"
            />
          </div>

          <div class="filter-luxury-wrapper input-stack">
            <label class="label-muted mb-2">Budget Bracket</label>
            <select v-model="budgetFilter" class="input-corp">
              <option value="all">All Brackets</option>
              <option value="cheap">Standard (< ₹500)</option>
              <option value="mid">Mid-Tier (₹500 - ₹2000)</option>
              <option value="premium">Elite Suite (> ₹2000)</option>
            </select>
          </div>
        </div>

        <div v-if="loading" class="loading-corp py-12">
          <div class="pulse-loader mx-auto mb-6"></div>
          <span class="text-dim">Fetching events...</span>
        </div>

        <div v-else-if="error" class="error-corp card-premium text-center py-12">
          <h3 class="mb-4">Failed to load</h3>
          <p class="text-dim mb-6">{{ error }}</p>
          <button @click="fetchEvents" class="btn-corp btn-corp-primary justify-center">Try Again</button>
        </div>

        <div v-else class="events-grid-premium animate-corp delay-100">
          <EventCard 
            v-for="event in filteredEvents" 
            :key="event.id" 
            :event="event" 
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import EventCard from '../components/EventCard.vue';
import RecommendationRow from '../components/RecommendationRow.vue';
import { useAuthStore } from '../stores/auth';

const events = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const searchQuery = ref('');
const budgetFilter = ref('all');
const authStore = useAuthStore();

const fetchEvents = async () => {
  loading.value = true;
  error.value = null;
  try {
    const config = authStore.token ? {
        headers: { Authorization: `Bearer ${authStore.token}` }
    } : {};
    
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
    const response = await axios.get(`${baseUrl}/events`, config);
    events.value = response.data;
  } catch (err: any) {
    console.error('Error fetching events:', err);
    error.value = 'Service unavailable. Please verify connectivity.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchEvents();
});

const filteredEvents = computed(() => {
  let result = events.value;
  
  if (budgetFilter.value !== 'all') {
    result = result.filter(e => e.price_tier === budgetFilter.value);
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(event => 
      event.title.toLowerCase().includes(query) ||
      event.sport_category.toLowerCase().includes(query) ||
      (event.venue_city && event.venue_city.toLowerCase().includes(query))
    );
  }
  
  return result;
});
</script>

<style scoped>
.home-page {
  padding-top: var(--nav-height);
}

.hero-main-title {
  margin-bottom: 1.5rem;
}

.hero-description {
  margin-bottom: 2rem;
}

.section-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.search-luxury-wrapper {
  flex: 1;
  min-width: 200px;
}

.filter-luxury-wrapper {
  width: 200px;
}

.loading-corp {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

@media (max-width: 1024px) {
  .section-header-flex {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-luxury-wrapper,
  .filter-luxury-wrapper {
    width: 100%;
  }
}
</style>


