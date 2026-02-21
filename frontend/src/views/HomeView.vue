<template>
  <div class="home-view">
    <section class="hero text-center animate-fade-in">
      <h1 class="hero-title"><span class="text-gradient">SyntaxError</span> Sports</h1>
      <p class="hero-subtitle">Discover and register for the best sports events happening around you. Join a community of passionate athletes.</p>
      
      <div class="hero-actions mt-4">
        <router-link to="/events" class="btn btn-primary">Browse Events</router-link>
        <router-link v-if="!authStore.token" to="/register" class="btn btn-outline ml-4">Join Now</router-link>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <h2 class="section-title">Recommended for You</h2>
        <router-link to="/events" class="btn btn-ghost">View All</router-link>
      </div>

      <div v-if="loading" class="loading-state text-center">
        <p>Loading events...</p>
      </div>
      
      <div v-else-if="events.length === 0" class="empty-state text-center">
        <p>No events found. Check back later!</p>
      </div>
      
      <div v-else class="event-grid">
        <EventCard 
          v-for="(event, index) in events.slice(0, 3)" 
          :key="event.id" 
          :event="event" 
          class="animate-fade-in"
          :style="`animation-delay: ${index * 100}ms`"
        />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';
import EventCard from '../components/EventCard.vue';

const authStore = useAuthStore();
const events = ref<any[]>([]);
const loading = ref(true);

const fetchRecommendedEvents = async () => {
  loading.value = true;
  try {
    const response = await api.get('/events');
    events.value = response.data;
  } catch (err) {
    console.error('Failed to load events:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRecommendedEvents();
});
</script>

<style scoped>
.hero {
  padding: 6rem 0;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
}

.section {
  padding: 4rem 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2rem;
}

.event-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.text-center { text-align: center; }
.mt-4 { margin-top: 1.5rem; }
.ml-4 { margin-left: 1rem; }
.loading-state, .empty-state { padding: 4rem 0; color: var(--text-secondary); }
</style>
