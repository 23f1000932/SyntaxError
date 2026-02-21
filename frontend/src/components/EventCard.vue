<template>
  <div class="glass-card event-card">
    <div class="event-image-placeholder">
      <div v-if="event.sport_category === 'Football'" class="sport-icon">⚽</div>
      <div v-else-if="event.sport_category === 'Cricket'" class="sport-icon">🏏</div>
      <div v-else-if="event.sport_category === 'Basketball'" class="sport-icon">🏀</div>
      <div v-else-if="event.sport_category === 'Tennis'" class="sport-icon">🎾</div>
      <div v-else class="sport-icon">🏆</div>
    </div>
    <div class="event-content">
      <div class="event-header">
        <span class="badge badge-primary">{{ event.sport_category }}</span>
        <span v-if="event.price_tier === 'cheap'" class="badge badge-success">₹</span>
        <span v-else-if="event.price_tier === 'mid'" class="badge badge-success">₹₹</span>
        <span v-else-if="event.price_tier === 'premium'" class="badge badge-success">₹₹₹</span>
      </div>
      <h3 class="event-title">{{ event.title }}</h3>
      <p class="event-location">📍 {{ event.venue_city }}</p>
      <p class="event-date">📅 {{ formattedDate }}</p>
      <div class="event-footer">
        <span class="event-price">₹{{ event.price }}</span>
        <router-link :to="`/events/${event.id}`" class="btn btn-outline btn-sm">View Details</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  event: Object as () => any
});

const formattedDate = computed(() => {
  if (!props.event.event_date) return 'TBA';
  const date = new Date(props.event.event_date);
  return date.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
});
</script>

<style scoped>
.event-card {
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.event-image-placeholder {
  height: 160px;
  background: linear-gradient(135deg, var(--bg-tertiary), #2a2a35);
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--glass-border);
}

.sport-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.event-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.event-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.event-title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #fff;
}

.event-location, .event-date {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.event-footer {
  margin-top: auto;
  padding-top: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.event-price {
  font-weight: 700;
  font-size: 1.2rem;
  color: var(--accent-primary);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}
</style>
